from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.database import get_db
from core.auth import get_current_user
from services.exeptions import TaskNotFoundError
from services.tasks import get_user_tasks_list, create_task, update_task, delete_task, get_user_task_detail
from schemas.task import TaskCreate, Task
from schemas.user import User


router = APIRouter(tags=["tasks"])


@router.get("/tasks/")
def get_user_tasks(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    tasks = get_user_tasks_list(db, current_user.id)
    return tasks


@router.get("/tasks/{task_id}/")
def get_user_task(task_id: int,
                  current_user: Annotated[User, Depends(get_current_user)],
                  db: Session = Depends(get_db)) -> Task:
    try:
        task = get_user_task_detail(db, current_user.id, task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Task.from_orm(task)


@router.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_user_task(task_form: TaskCreate,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)) -> Task:
    try:
        task = create_task(db, task_form, current_user.id)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.statement)
    return Task.from_orm(task)


@router.put("/tasks/{task_id}/", status_code=status.HTTP_201_CREATED)
def update_user_task(task_id: int,
                     task_form: TaskCreate,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)) -> TaskCreate:
    try:
        task = update_task(db, task_form, task_id,  current_user.id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Task.from_orm(task)


@router.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_task(task_id: int,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)) :
    try:
        delete_task(db, task_id,  current_user.id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
