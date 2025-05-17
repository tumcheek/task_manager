from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from models.task import TaskStatus, TaskPriority


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    status: str
    priority: str | None
    owner_id: int
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class PaginatedTasks(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    tasks: List[Task]
