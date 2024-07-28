from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from models.task import TaskStatus, TaskPriority


class Task(BaseModel):
    task_id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: str
    created_at: str
    updated_at: str


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


