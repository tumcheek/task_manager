from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Task, Tag
from services.exeptions import (TaskNotFoundError, TagNotFoundError,
                                TagNotAssociatedError, TagAlreadyExistsError)
from schemas import tags


def get_user_tags(db: Session, user_id: int) -> List[Tag]:
    return db.query(Tag).filter(Tag.owner_id == user_id).all()


def create_tag_for_task(db: Session,
                        task_id: int,
                        tag_data: tags.Tag,
                        user_id: int) -> Tag:
    db_task = db.query(Task).filter(
        Task.id == task_id, Task.owner_id == user_id).first()
    if not db_task:
        raise TaskNotFoundError(f"Task with id {task_id} not found")

    new_tag = Tag(**tag_data.dict(), owner_id=user_id)
    db.add(new_tag)
    db.flush()

    db_task.tags.append(new_tag)

    try:
        db.commit()
        db.refresh(new_tag)
    except IntegrityError:
        db.rollback()
        raise TagAlreadyExistsError(
            "Tag with this title already exists for this user"
        )

    return new_tag


def get_task_tags(db: Session, task_id: int, user_id: int) -> List[Tag]:
    task = db.query(Task).filter(
        Task.id == task_id, Task.owner_id == user_id
    ).first()
    if not task:
        raise TaskNotFoundError(f"Task with id {task_id} not found")
    return task.tags


def delete_tag_from_task(db: Session,
                         task_id: int,
                         tag_id: int,
                         user_id: int) -> None:
    task = db.query(Task).filter(
        Task.id == task_id, Task.owner_id == user_id
    ).first()
    if not task:
        raise TaskNotFoundError(f"Task with id {task_id} not found")

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise TagNotFoundError(f"Tag with id {tag_id} not found")

    if tag not in task.tags:
        raise TagNotAssociatedError(
            f"Tag with id {tag_id} is not associated "
            f"with task with id {task_id}"
        )

    task.tags.remove(tag)
    db.commit()
