from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


task_tag_association_table = Table(
    'task_tag_association',
    Base.metadata,
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
    Column('task_id', ForeignKey('tasks.id'), primary_key=True)
)


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=datetime.now
                                                 )
    updated_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=datetime.now,
                                                 onupdate=datetime.now
                                                 )

    owner: Mapped["User"] = relationship(back_populates="tags")
    tasks: Mapped[list["Task"]] = relationship(
        secondary=task_tag_association_table,
        back_populates="tags"
    )
