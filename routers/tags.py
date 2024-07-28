from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from core.database import get_db
from models import User
from services.exeptions import TaskNotFoundError, TagNotAssociatedError, TagNotFoundError, TagAlreadyExistsError
from shemas.tags import Tag

from services import tags
from .auth import get_current_user

router = APIRouter(tags=['tags'])


@router.get("/user/tags/", response_model=List[Tag])
def get_user_tags(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return tags.get_user_tags(db, current_user.id)


@router.post("/tasks/{task_id}", response_model=Tag)
def create_tag_for_task(
    task_id: int,
    tag: Tag,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):

    try:
        return tags.create_tag_for_task(db, task_id, tag, current_user.id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except TagAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists")


@router.get("/tasks/{task_id}", response_model=List[Tag])
def get_task_tags(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    try:
        return tags.get_task_tags(db, task_id, current_user.id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.delete("/tasks/{task_id}/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag_from_task(
    task_id: int,
    tag_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    try:
        tags.delete_tag_from_task(db, task_id, tag_id, current_user.id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except TagNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    except TagNotAssociatedError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag is not associated with this task")
    return {"detail": "Tag removed from task successfully"}