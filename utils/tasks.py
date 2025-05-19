from sqlalchemy.orm import Session

from exeptions import TaskNotFoundError
from models import Task


def get_project_task(db: Session, task_id: int, project_id: int, **kwargs) -> Task:
    filters = {k: v for k, v in kwargs.items() if v is not None}
    task = db.query(Task).filter_by(id=task_id, project_id=project_id, **filters).first()
    if not task:
        raise TaskNotFoundError(task_id=task_id)
    return task
