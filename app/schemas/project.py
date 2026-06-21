from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    member_ids: list[int] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    member_ids: Optional[list[int]] = None


class ProjectMember(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class ProjectInDBBase(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Project(ProjectInDBBase):
    members: list[ProjectMember] = []


class ProjectDetail(Project):
    task_count: int = 0