from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from dependencies.permissions import ensure_user_is_project_member_or_raise
from exeptions import TaskNotFoundError
from models import Task

from schemas.task import TaskCreate
from utils import get_project_task


def get_user_tasks_list(
    db: Session,
    user_id: int,
    project_id: int,
    offset: int = 0,
    limit: int = 5,
) -> List[Task]:
    tasks = (
        db.query(Task)
        .filter(Task.owner_id == user_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return tasks


def get_user_task_detail(
    db: Session, user_id: int, task_id: int, project_id: int
) -> Task:
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id, Task.owner_id == user_id, Task.project_id == project_id
        )
        .first()
    )
    if not task:
        raise TaskNotFoundError(task_id)
    return task


def create_task(
    db: Session, task_info: TaskCreate, user_id: int, project_id: int
) -> Task:
    task_data = task_info.dict()
    task = Task(**task_data, owner_id=user_id, project_id=project_id)
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(
            statement="Data integrity violation. "
            "Please check your input "
            "and try again.",
            params=e.params,
            orig=e.orig,
        )

    return task


def update_task(
    db: Session, task_info: TaskCreate, task_id: int, user_id: int, project_id: int
) -> Task | None:
    task_data = task_info.dict()
    task = get_project_task(db, project_id, task_id)
    task.update(task_data)
    db.commit()
    updated_task = db.query(Task).filter(Task.id == task_id).first()
    return updated_task


def delete_task(db: Session, task_id: int, user_id: int, project_id: int) -> None:
    task = get_project_task(db, project_id, task_id)
    task.delete()
    db.commit()


def assign_task(db: Session, project_id: int, task_id: int, user_id: int) -> Task:
    task = get_project_task(db, project_id, task_id)
    ensure_user_is_project_member_or_raise(db, project_id, user_id)

    task.assigned_to_id = user_id
    db.commit()
    db.refresh(task)
    return task
