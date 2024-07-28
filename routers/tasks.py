from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.database import get_db
from core.auth import get_current_user
from services.exeptions import TaskNotFoundError
from services.tasks import get_user_tasks_list, create_task, update_task, delete_task
from shemas.task import TaskCreate
from shemas.user import User


router = APIRouter()


@router.get("/tasks/")
def get_user_tasks(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    tasks = get_user_tasks_list(db, current_user.id)
    return tasks


@router.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_user_task(task_form: TaskCreate, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    try:
        task = create_task(db, task_form, current_user.id)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.statement)
    return task


@router.put("/tasks/{task_id}/", status_code=status.HTTP_201_CREATED)
def update_user_task(task_id,
                     task_form: TaskCreate,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)) -> TaskCreate:
    try:
        task = update_task(db, task_form, task_id,  current_user.id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return TaskCreate.from_orm(task)


@router.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_task(task_id,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)):
    try:
        delete_task(db, task_id,  current_user.id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
