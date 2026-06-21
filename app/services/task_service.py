from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.project_service import check_project_access, get_project_or_404


def get_task_or_404(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


def create_task(
    db: Session, task_data: TaskCreate, current_user: User
) -> Task:
    # If task belongs to a project, verify user has access
    if task_data.project_id:
        project = get_project_or_404(db, task_data.project_id)
        check_project_access(project, current_user)

    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        project_id=task_data.project_id,
        assignee_id=task_data.assignee_id,
        owner_id=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    completed: Optional[bool] = None,
) -> list[Task]:
    query = db.query(Task)

    # Filter by project if specified
    if project_id is not None:
        project = get_project_or_404(db, project_id)
        check_project_access(project, current_user)
        query = query.filter(Task.project_id == project_id)
    else:
        # Show tasks owned by user or assigned to user
        query = query.filter(
            (Task.owner_id == current_user.id) | (Task.assignee_id == current_user.id)
        )

    if assignee_id is not None:
        query = query.filter(Task.assignee_id == assignee_id)
    if completed is not None:
        query = query.filter(Task.completed == completed)

    tasks = query.offset(skip).limit(limit).all()
    return tasks


def get_task(db: Session, task_id: int, current_user: User) -> Task:
    task = get_task_or_404(db, task_id)

    # Check access: owner, assignee, or project member
    if task.owner_id == current_user.id or task.assignee_id == current_user.id:
        return task

    if task.project_id:
        project = get_project_or_404(db, task.project_id)
        check_project_access(project, current_user)
        return task

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions to view this task",
    )


def update_task(
    db: Session, task_id: int, task_data: TaskUpdate, current_user: User
) -> Task:
    task = get_task_or_404(db, task_id)

    # Only owner or assignee can update
    if task.owner_id != current_user.id and task.assignee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this task",
        )

    update_data = task_data.model_dump(exclude_unset=True)

    # If changing project, verify access to new project
    if "project_id" in update_data and update_data["project_id"] is not None:
        project = get_project_or_404(db, update_data["project_id"])
        check_project_access(project, current_user)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, current_user: User) -> None:
    task = get_task_or_404(db, task_id)

    if task.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this task",
        )

    db.delete(task)
    db.commit()