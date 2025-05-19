from fastapi import Path, Depends
from sqlalchemy.orm import Session

from core import get_current_user, get_db
from exeptions import AdminAccessRequired, ProjectPermissionError
from models import ProjectMember, User


def ensure_user_is_admin(user: User = Depends(get_current_user)):
    if user.role.name != "admin":
        raise AdminAccessRequired("Admin access required")


def verify_user_in_project_or_admin(
    project_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = (
        db.query(ProjectMember)
        .filter_by(user_id=current_user.id, project_id=project_id)
        .first()
    )

    if not membership:
        raise ProjectPermissionError(project_id=project_id)


def ensure_user_is_project_member_or_raise(db: Session, project_id: int, user_id: int):
    membership = (
        db.query(ProjectMember)
        .filter_by(user_id=user_id, project_id=project_id)
        .first()
    )
    if not membership:
        raise ProjectPermissionError(project_id=project_id)
