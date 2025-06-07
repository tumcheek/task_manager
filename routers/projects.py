from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core import get_current_user, get_db
from dependencies.permissions import (
    ensure_user_is_admin,
    verify_user_in_project_or_admin,
)

from models import User, Project
from schemas.pagination import PaginatedResponse, PaginationParams
from schemas.projects import ProjectCreate, ProjectInfo, AddMemberInput
from services.projects import (
    create_project,
    get_user_projects,
    get_all_projects,
    update_project,
    delete_project,
    add_user_to_project,
)

from services.tasks import (
    get_user_project_tasks_list,
    create_task,
    update_task,
    delete_task,
    get_project_task_detail
)
from schemas.task import TaskCreate, Task, TaskFilterParams

router = APIRouter(tags=["projects"])


@router.post(
    "/projects/",
    response_model=ProjectInfo,
    dependencies=[Depends(ensure_user_is_admin)],
)
def add_project(
    project_form: ProjectCreate,
    db: Session = Depends(get_db),
):
    project_instance = create_project(db, project_form)
    return ProjectInfo.from_orm(project_instance)


@router.get("/projects/my/", response_model=list[ProjectInfo])
def list_user_projects(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    projects = get_user_projects(db, current_user.id)
    return projects


@router.get(
    "/projects/",
    response_model=PaginatedResponse[ProjectInfo],
    dependencies=[Depends(ensure_user_is_admin)],
)
def list_all_projects(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
):
    offset = (pagination.page - 1) * pagination.page_size
    projects = get_all_projects(db, offset, pagination.page_size)
    base_query = db.query(Project)
    total = base_query.count()
    return PaginatedResponse.create(
        items=projects,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size
    )


@router.put(
    "/projects/{project_id}",
    response_model=ProjectInfo,
    dependencies=[Depends(ensure_user_is_admin)],
)
def edit_project(
    project_id: int,
    project_form: ProjectCreate,
    db: Session = Depends(get_db),
):
    return update_project(db, project_form, project_id)


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(ensure_user_is_admin)],
)
def remove_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    delete_project(db, project_id)

@router.post("/projects/{project_id}/members", status_code=status.HTTP_201_CREATED, dependencies=[Depends(ensure_user_is_admin)])
def add_member_to_project(
    project_id: int,
    payload: AddMemberInput,
    db: Session = Depends(get_db),
):
    add_user_to_project(db, project_id, payload.user_id)
    return payload


@router.get(
    "/projects/{project_id}/tasks/",
    dependencies=[Depends(verify_user_in_project_or_admin)],
)
def get_user_project_tasks(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    filters: TaskFilterParams = Depends()
) -> PaginatedResponse[Task]:
    """
    Retrieve all project tasks for the currently authenticated user.

    Returns a list of tasks that belong to the user identified by the
    access token and particular project. Requires authentication.

    Args:
        project_id (int): The project ID.
        current_user (User): The currently authenticated user.
        db (Session): The database session dependency.
        pagination (PaginationParams): A pagination params object.
        filters (TaskFilterParams): A filters object.

    Returns:
        PaginatedResponse[Task]: A paginated list of user's owned tasks.
    """
    offset = (pagination.page - 1) * pagination.page_size
    tasks, total = get_user_project_tasks_list(db, current_user.id, project_id, filters,
                                               offset, pagination.page_size)

    return PaginatedResponse.create(
        items=tasks,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size
    )


@router.get(
    "/projects/{project_id}/tasks/{task_id}/",
    dependencies=[Depends(verify_user_in_project_or_admin), Depends(get_current_user)],
)
def get_project_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
) -> Task:
    """
    Retrieve details of a specific task belonging to the authenticated user
    and particular project.

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
    task = get_project_task_detail(db, task_id, project_id)
    return Task.from_orm(task)


@router.post(
    "/projects/{project_id}/tasks/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_user_in_project_or_admin)],
)
def create_project_task(
    project_id: int,
    task_form: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> Task:
    """
    Create a new task for the currently authenticated user and particular project.

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
        task = create_task(db, task_form, current_user.id, project_id)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.statement)
    return Task.from_orm(task)


@router.put(
    "/projects/{project_id}/tasks/{task_id}/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_in_project_or_admin)],
)
def update_project_task(
    project_id: int,
    task_id: int,
    task_form: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> TaskCreate:
    """
    Update an existing task for the currently authenticated user
    and particular project.

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

    if current_user.role.name != 'admin':
        task = update_task(db, task_form, task_id, project_id, current_user.id)
    else:
        task = update_task(db, task_form, task_id, project_id)
    return Task.from_orm(task)


@router.delete(
    "/projects/{project_id}/tasks/{task_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_user_in_project_or_admin)],
)
def delete_user_task(
    project_id: int,
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """
    Delete a task belonging to the currently authenticated user and
    particular project.

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
    if current_user.role.name != 'admin':
        delete_task(db, task_id, project_id, current_user.id)
    else:
        delete_task(db, task_id, project_id)

