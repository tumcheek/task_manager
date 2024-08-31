from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Task
from services.exeptions import TaskNotFoundError
from schemas.task import TaskCreate


def get_user_tasks_list(db: Session, user_id: int) -> List[Task]:
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    return tasks


def get_user_task_detail(db: Session, user_id: int, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not task:
        raise TaskNotFoundError()
    return task


def create_task(db: Session, task_info: TaskCreate, user_id: int) -> Task:
    task_data = task_info.dict()
    task = Task(**task_data, owner_id=user_id)
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(statement="Data integrity violation. Please check your input and try again.",
                             params=e.params,
                             orig=e.orig
                             )

    return task


def update_task(db: Session, task_info: TaskCreate, task_id: int, user_id: int) -> Task:
    task_data = task_info.dict()
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id)
    if not task.first():
        raise TaskNotFoundError()
    task.update(task_data)
    db.commit()
    updated_task = db.query(Task).filter(Task.id == task_id).first()
    return updated_task


def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id)
    if not task.first():
        raise TaskNotFoundError()
    task.delete()
    db.commit()
    return True
