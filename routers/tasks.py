from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.database import get_db
from core.auth import get_current_user
from services.tasks import (get_user_tasks_list, create_task, update_task,
                            delete_task, get_user_task_detail)
from schemas.task import TaskCreate, Task
from schemas.user import User


router = APIRouter(tags=["tasks"])


@router.get("/tasks/")
def get_user_tasks(current_user: Annotated[User, Depends(get_current_user)],
                   db: Session = Depends(get_db)):
    """
    Retrieve all tasks for the currently authenticated user.

    Returns a list of tasks that belong to the user identified by the
    access token. Requires authentication.

    Args:
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.

    Returns:
        List[Task]: A list of tasks owned by the authenticated user.
    """
    tasks = get_user_tasks_list(db, current_user.id)
    return tasks


@router.get("/tasks/{task_id}/")
def get_user_task(task_id: int,
                  current_user: Annotated[User, Depends(get_current_user)],
                  db: Session = Depends(get_db)) -> Task:
    """
    Retrieve details of a specific task belonging to the authenticated user.

    Fetches and returns information about a single task, identified by its ID,
    if it belongs to the currently authenticated user. Requires authentication.

    Args:
        task_id (int): The ID of the task to retrieve.
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.

    Returns:
        Task: The task data mapped to a response schema.

    Raises:
        HTTPException:
            - 404 if the task is not found or does not belong to the user.
    """
    task = get_user_task_detail(db, current_user.id, task_id)
    return Task.from_orm(task)


@router.post("/tasks/", status_code=status.HTTP_201_CREATED)
def create_user_task(task_form: TaskCreate,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)) -> Task:
    """
    Create a new task for the currently authenticated user.

    Accepts task input data and creates a new task associated with the user.
    Returns the created task. Requires authentication.

    Args:
        task_form (TaskCreate): The data required to create a new task.
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.

    Returns:
        Task: The newly created task.

    Raises:
        HTTPException:
            - 400 if a database integrity error occurs during task creation.
    """
    try:
        task = create_task(db, task_form, current_user.id)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.statement)
    return Task.from_orm(task)


@router.put("/tasks/{task_id}/", status_code=status.HTTP_200_OK)
def update_user_task(task_id: int,
                     task_form: TaskCreate,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)) -> Task:

    """
    Update an existing task for the currently authenticated user.

    Updates the task with the provided ID using the new data from the user.
    The task must belong to the currently authenticated user. Requires authentication.

    Args:
        task_id (int): The ID of the task to be updated.
        task_form (TaskCreate): The updated task data.
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.

    Returns:
        TaskCreate: The updated task data.

    Raises:
        HTTPException:
            - 404 if the task is not found or does not belong to the user.
    """

    task = update_task(db, task_form, task_id,  current_user.id)
    return Task.from_orm(task)


@router.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_task(task_id: int,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)):
    """
    Delete a task belonging to the currently authenticated user.

    Removes the task with the given ID if it exists and belongs to the user.
    Requires authentication.

    Args:
        task_id (int): The ID of the task to be deleted.
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.

    Returns:
        None

    Raises:
        HTTPException:
            - 404 if the task is not found or does not belong to the user.
    """

    delete_task(db, task_id,  current_user.id)
