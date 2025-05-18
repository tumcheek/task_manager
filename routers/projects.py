from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from core import get_current_user, get_db
from models import User
from schemas.projects import ProjectCreate, ProjectInfo
from services.projects import (
    create_project,
    get_user_projects,
    get_all_projects,
    update_project,
    delete_project,
)

router = APIRouter(tags=["projects"])


@router.post("/projects/", response_model=ProjectInfo)
def add_project(
    project_form: ProjectCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    if current_user.role.name != "admin":
        # TODO: Write custom error
        raise PermissionError("User is not allowed to create projects")
    project_instance = create_project(db, project_form)
    return ProjectInfo.from_orm(project_instance)


@router.get("/projects/my/", response_model=list[ProjectInfo])
def list_user_projects(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    projects = get_user_projects(db, current_user.id)
    return projects


@router.get("/projects/", response_model=list[ProjectInfo])
def list_all_projects(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    if current_user.role.name != "admin":
        # TODO: Write custom error
        raise PermissionError("User is not allowed to create projects")
    projects = get_all_projects(db)
    return projects


@router.put("/projects/{project_id}", response_model=ProjectInfo)
def edit_project(
    project_id: int,
    project_form: ProjectCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):

    if current_user.role.name != "admin":
        # TODO: Write custom error
        raise PermissionError("User is not allowed to update projects")
    return update_project(db, project_form, project_id)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    if current_user.role.name != "admin":
        raise PermissionError("User is not allowed to delete projects")
    delete_project(db, project_id)
