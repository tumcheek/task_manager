from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[List["Task"]] = relationship(back_populates="owner")
    tags: Mapped[List["Tag"]] = relationship(back_populates="owner")
