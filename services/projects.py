from typing import Type

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Project, ProjectMember
from schemas.projects import ProjectCreate
from exeptions import ProjectNotFoundError


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
    return project


def get_user_projects(db: Session, user_id: int) -> list[Type[Project]]:
    stmt = select(Project).where(
        Project.id.in_(
            select(ProjectMember.project_id).where(ProjectMember.user_id == user_id)
        )
    )
    return db.execute(stmt).scalars().all()


def get_all_projects(db: Session, offset: int = 0, limit: int = 5,) -> list[Type[Project]]:
    projects = db.query(Project).limit(limit).offset(offset).all()
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


def add_user_to_project(db: Session, project_id: int, user_id: int):
    exists = (
        db.query(ProjectMember)
        .filter_by(project_id=project_id, user_id=user_id)
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="User is already a member")

    membership = ProjectMember(project_id=project_id, user_id=user_id)
    db.add(membership)
    db.commit()
    return membership
