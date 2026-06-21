from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.project import Project
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate, ProjectDetail
from app.schemas.task import Task as TaskSchema
from app.services.auth_service import get_current_active_user
from app.services.project_service import (
    create_project,
    get_projects_for_user,
    get_project_detail,
    update_project,
    delete_project,
    check_project_access,
    get_project_or_404,
)

router = APIRouter()


@router.get("", response_model=List[ProjectSchema])
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    projects = get_projects_for_user(db, current_user, skip=skip, limit=limit)
    return projects


@router.post("", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_project(db, project_data, current_user)


@router.get("/{project_id}", response_model=ProjectDetail)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    project = get_project_detail(db, project_id, current_user)
    task_count = len(project.tasks)
    return ProjectDetail(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
        created_at=project.created_at,
        updated_at=project.updated_at,
        members=project.members,
        task_count=task_count,
    )


@router.put("/{project_id}", response_model=ProjectSchema)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return update_project(db, project_id, project_data, current_user)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    delete_project(db, project_id, current_user)


@router.get("/{project_id}/tasks", response_model=List[TaskSchema])
def list_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    project = get_project_detail(db, project_id, current_user)
    return project.tasks