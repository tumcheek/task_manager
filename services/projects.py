from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Project, ProjectMember
from schemas.projects import ProjectCreate
from services.exeptions import ProjectNotFoundError


def create_project(db: Session, project: ProjectCreate):
    project = Project(**project.dict())
    try:
        db.add(project)
        db.commit()
        db.refresh(project)
    except IntegrityError as e:
        db.rollback()
        raise IntegrityError(
            statement="Data integrity violation. "
            "Please check your input "
            "and try again.",
            params=e.params,
            orig=e.orig,
        )


def get_user_projects(db: Session, user_id: int) -> list[Type[Project]]:
    user_projects_id = (
        db.query(ProjectMember.project_id)
        .filter(ProjectMember.user_id == user_id)
        .all()
    )
    projects = db.query(Project).filter(Project.id.in_(user_projects_id)).all()
    return projects


def get_all_projects(db: Session) -> list[Type[Project]]:
    projects = db.query(Project).all()
    return projects


def update_project(
    db: Session,
    project_info: ProjectCreate,
    project_id: int,
) -> Project | None:
    project_data = project_info.dict()
    project = db.query(Project).filter(Project.id == project_id)
    if not project.first():
        raise ProjectNotFoundError(project_id)
    project.update(project_data)
    db.commit()
    updated_project = db.query(Project).filter(Project.id == project_id).first()
    return updated_project


def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ProjectNotFoundError(project_id)

    db.delete(project)
    db.commit()
