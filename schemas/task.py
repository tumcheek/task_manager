from datetime import datetime
from enum import Enum
from typing import Optional, List, Literal

from pydantic import BaseModel, ConfigDict, Field

from models.task import TaskStatus, TaskPriority


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str | None
    owner_id: int
    assignee_id: int | None
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
    assignee_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TaskSortField(str, Enum):
    CREATED_AT = "created_at"
    PRIORITY = "priority"
    TITLE = "title"
    STATUS = "status"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class TaskRole(str, Enum):
    OWNER = "owner"
    ASSIGNEE = "assignee"


class TaskFilterParams(BaseModel):
    role: TaskRole = Field(TaskRole.OWNER, description="Filter tasks by user role (owner or assignee)")
    sort_by: TaskSortField = Field(
        TaskSortField.CREATED_AT, description="Field to sort by"
    )
    sort_order: SortOrder = Field(
        SortOrder.ASC, description="Sort order: ascending or descending"
    )
    status: Optional[TaskStatus] = Field(None, description="Filter by task status")
    priority: Optional[TaskPriority] = Field(None, description="Filter by priority level")

