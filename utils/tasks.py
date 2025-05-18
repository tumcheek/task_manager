from sqlalchemy.orm import Session

from exeptions import TaskNotFoundError
from models import Task


def get_project_task(db: Session, project_id: int, task_id: int) -> Task:
    task = db.query(Task).filter_by(id=task_id, project_id=project_id).first()
    if not task:
        raise TaskNotFoundError(task_id=task_id)
    return task
