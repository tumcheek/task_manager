from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from models.task import TaskStatus, TaskPriority


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str | None
    owner_id: int
    due_date: datetime | None
    project_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedTasks(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    tasks: List[Task]
