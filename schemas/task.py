from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.task import TaskStatus, TaskPriority


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    status: str
    priority: str
    owner_id: int
    due_date: datetime
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


