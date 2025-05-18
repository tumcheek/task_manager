from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

from models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    owned_tasks: Mapped[List["Task"]] = relationship(
        back_populates="owner", foreign_keys="[Task.owner_id]"
    )
    assigned_tasks: Mapped[List["Task"]] = relationship(
        back_populates="owner", foreign_keys="[Task.assignee_id]"
    )
    tags: Mapped[List["Tag"]] = relationship(back_populates="owner")
    projects = relationship("ProjectMember", back_populates="user")
    role = relationship("Role", back_populates="users")
