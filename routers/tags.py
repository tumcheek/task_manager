from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from core.database import get_db
from models import User
from services.exeptions import (TaskNotFoundError, TagNotAssociatedError,
                                TagNotFoundError, TagAlreadyExistsError)
from schemas.tags import Tag, TagCreate

from services import tags
from .auth import get_current_user

router = APIRouter(tags=['tags'])


@router.get("/user/tags/", response_model=List[Tag])
def get_user_tags(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Retrieve tags associated with the currently authenticated user.

    Fetches and returns a list of tags that belong to the user identified
    by the access token. Requires authentication.

    Args:
        current_user (User): The currently authenticated user, provided via dependency.
        db (Session): The database session dependency.

    Returns:
        List[Tag]: A list of tags belonging to the authenticated user.
    """
    return tags.get_user_tags(db, current_user.id)


@router.post("/tasks/{task_id}", response_model=Tag)
def create_tag_for_task(
    task_id: int,
    tag: TagCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Create a new tag for a specific task.

    Adds a new tag to the task with the given ID, belonging to the currently
    authenticated user. If the task does not exist or the tag already exists,
    an appropriate error is returned.

    Args:
        task_id (int): The ID of the task to which the tag will be added.
        tag (TagCreate): The tag data to be created.
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.

    Returns:
        Tag: The newly created tag associated with the task.

    Raises:
        HTTPException:
            - 404 if the task is not found.
            - 400 if the tag already exists for the task.
    """
    try:
        return tags.create_tag_for_task(db, task_id, tag, current_user.id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    except TagAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Tag already exists")


@router.get("/tasks/{task_id}", response_model=List[Tag])
def get_task_tags(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
     Retrieve all tags associated with a specific task.

     Returns a list of tags linked to the given task, if the task belongs to the
     currently authenticated user. Requires authentication.

     Args:
         task_id (int): The ID of the task whose tags are to be retrieved.
         current_user (User): The currently authenticated user.
         db (Session): The database session dependency.

     Returns:
         List[Tag]: A list of tags associated with the specified task.

     Raises:
         HTTPException:
             - 404 if the task is not found or does not belong to the user.
     """
    try:
        return tags.get_task_tags(db, task_id, current_user.id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")


@router.delete("/tasks/{task_id}/{tag_id}",
               status_code=status.HTTP_200_OK)
def delete_tag_from_task(
    task_id: int,
    tag_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """
    Remove a tag from a specific task.

    Deletes the association between a tag and a task for the currently authenticated
    user. This does not delete the tag itself, only its link to the task.

    Args:
        task_id (int): The ID of the task from which the tag will be removed.
        tag_id (int): The ID of the tag to be removed.
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.

    Returns:
        dict: A success message indicating that the tag was removed.

    Raises:
        HTTPException:
            - 404 if the task is not found.
            - 404 if the tag is not found.
            - 400 if the tag is not associated with the specified task.
    """
    try:
        tags.delete_tag_from_task(db, task_id, tag_id, current_user.id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    except TagNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tag not found")
    except TagNotAssociatedError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Tag is not associated with this task")
    return {"detail": "Tag removed from task successfully"}
