from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.project import Project, project_members
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


def check_project_access(project: Project, current_user: User) -> None:
    """Check if user is owner or member of the project."""
    if project.owner_id == current_user.id:
        return
    if current_user in project.members:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not a member of this project",
    )


def create_project(
    db: Session, project_data: ProjectCreate, current_user: User
) -> Project:
    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id,
    )
    db.add(project)
    db.flush()

    # Add owner as a member automatically
    project.members.append(current_user)

    # Add specified members
    if project_data.member_ids:
        members = (
            db.query(User)
            .filter(User.id.in_(project_data.member_ids))
            .all()
        )
        for member in members:
            if member.id != current_user.id:
                project.members.append(member)

    db.commit()
    db.refresh(project)
    return project


def get_projects_for_user(
    db: Session, current_user: User, skip: int = 0, limit: int = 100
) -> list[Project]:
    # Projects where user is owner or member
    projects = (
        db.query(Project)
        .filter(
            (Project.owner_id == current_user.id)
            | (Project.members.any(User.id == current_user.id))
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return projects


def get_project_detail(db: Session, project_id: int, current_user: User) -> Project:
    project = get_project_or_404(db, project_id)
    check_project_access(project, current_user)
    return project


def update_project(
    db: Session, project_id: int, project_data: ProjectUpdate, current_user: User
) -> Project:
    project = get_project_or_404(db, project_id)

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can update the project",
        )

    update_data = project_data.model_dump(exclude_unset=True)
    member_ids = update_data.pop("member_ids", None)

    for field, value in update_data.items():
        setattr(project, field, value)

    if member_ids is not None:
        # Clear existing members and re-add
        project.members = []
        project.members.append(current_user)  # Owner always a member
        if member_ids:
            members = (
                db.query(User)
                .filter(User.id.in_(member_ids))
                .all()
            )
            for member in members:
                if member.id != current_user.id:
                    project.members.append(member)

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int, current_user: User) -> None:
    project = get_project_or_404(db, project_id)

    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can delete the project",
        )

    db.delete(project)
    db.commit()