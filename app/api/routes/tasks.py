from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate
from app.services.auth_service import get_current_active_user
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)

router = APIRouter()


@router.get("", response_model=List[TaskSchema])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    project_id: Optional[int] = Query(None),
    assignee_id: Optional[int] = Query(None),
    completed: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_tasks(
        db,
        current_user,
        skip=skip,
        limit=limit,
        project_id=project_id,
        assignee_id=assignee_id,
        completed=completed,
    )


@router.post("", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_task(db, task_data, current_user)


@router.get("/{task_id}", response_model=TaskSchema)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_task(db, task_id, current_user)


@router.put("/{task_id}", response_model=TaskSchema)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return update_task(db, task_id, task_data, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    delete_task(db, task_id, current_user)