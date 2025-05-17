import logging

from fastapi import Request
from fastapi.responses import JSONResponse


from services.exeptions import TaskNotFoundError

logger = logging.getLogger(__name__)


def task_not_found_exception_handler(request: Request, exc: TaskNotFoundError):
    logger.warning(
        f"Task not found: ID={exc.task_id} during {request.method} {request.url}"
    )
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Task with ID {exc.task_id} was not found.",
            "task_id": exc.task_id,
        },
    )
