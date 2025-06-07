from typing import List, Tuple

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from dependencies.permissions import ensure_user_is_project_member_or_raise
from exeptions import TaskNotFoundError
from models import Task

from schemas.task import TaskCreate, TaskFilterParams, TaskRole, SortOrder
from utils import get_project_task


def get_user_project_tasks_list(
    db: Session,
    user_id: int,
    project_id: int,
    filters: TaskFilterParams,
    offset: int = 0,
    limit: int = 5,
) -> Tuple[List[Task], int]:

    if filters.role == TaskRole.ASSIGNEE:
        query = db.query(Task).filter(Task.assignee_id == user_id, Task.project_id == project_id)
    else:
        query = db.query(Task).filter(Task.owner_id == user_id, Task.project_id == project_id)

    filter_data = filters.dict(exclude_unset=True, exclude_none=True, exclude={"sort_by", "sort_order", "role"})
    for field_name, value in filter_data.items():
        if hasattr(Task, field_name):
            query = query.filter(getattr(Task, field_name) == value)

    sort_column = getattr(Task, filters.sort_by)
    sort_direction = desc if filters.sort_order == SortOrder.DESC else asc
    query = query.order_by(sort_direction(sort_column))
    total = query.count()
    return query.offset(offset).limit(limit).all(), total


def get_project_task_detail(
    db: Session, task_id: int, project_id: int
) -> Task:
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id, Task.project_id == project_id
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
    db: Session, task_info: TaskCreate, task_id: int, project_id: int, user_id: int | None = None
) -> Task | None:
    task_data = task_info.dict()
    if user_id is not None:
        get_project_task(db, task_id, project_id, owner_id=user_id)
    else:
        get_project_task(db, task_id, project_id)

    query = db.query(Task).filter(Task.id == task_id, Task.project_id == project_id)
    query.update(task_data)
    db.commit()
    updated_task = db.query(Task).filter(Task.id == task_id).first()
    return updated_task


def delete_task(db: Session, task_id: int, project_id: int, user_id: int | None = None) -> None:
    if user_id is not None:
        get_project_task(db, task_id, project_id, owner_id=user_id)
    else:
        get_project_task(db, task_id, project_id)
    db.query(Task).filter_by(id=task_id, project_id=project_id).delete()
    db.commit()


def assign_task(db: Session, project_id: int, task_id: int, user_id: int) -> Task:
    task = get_project_task(db, task_id, project_id)
    ensure_user_is_project_member_or_raise(db, project_id, user_id)

    task.assigned_to_id = user_id
    db.commit()
    db.refresh(task)
    return task
