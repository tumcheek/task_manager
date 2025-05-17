from datetime import datetime
import enum

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Enum, DateTime, ForeignKey

from models.base import Base
from models.tag import task_tag_association_table


class TaskStatus(enum.Enum):
    TO_DO = "to do"
    ON_HOLD = "on hold"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.TO_DO
    )
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    owner: Mapped["User"] = relationship(back_populates="tasks")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=task_tag_association_table,
        back_populates="tasks",
        cascade="all, delete",
    )
