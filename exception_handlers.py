import logging
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse
from sentry_sdk import capture_exception

from services.exeptions import TaskNotFoundError, TagNotFoundError, TagNotAssociatedError, TagAlreadyExistsError

logger = logging.getLogger(__name__)


def general_exception_handler(request: Request, exc: Exception):
    capture_exception(exc)
    error_id = str(uuid.uuid4())
    logger.error(
        f"Unhandled exception [{error_id}] during {request.method} {request.url}:\n{exc}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected server error occurred. Please try again later.",
            "error_id": error_id
        },
    )


def task_not_found_exception_handler(request: Request, exc: TaskNotFoundError):
    logger.warning(f"Task not found: ID={exc.task_id} during {request.method} {request.url}")
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Task with ID {exc.task_id} was not found.",
            "task_id": exc.task_id
        }
    )


def tag_not_found_exception_handler(request: Request, exc: TagNotFoundError):
    logger.warning(f"Tag not found: ID={exc.tag_id} during {request.method} {request.url}")
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Tag with ID {exc.tag_id} was not found.",
            "tag_id": exc.tag_id
        }
    )


def tag_not_associated_error_handler(request: Request, exc: TagNotAssociatedError):
    error_id = str(uuid.uuid4())
    logger.warning(f"Tag with ID {exc.tag_id} is not associated with task with ID {exc.task_id} during {request.method} {request.url}")
    return JSONResponse(
        status_code=400,
        content={
            "message": str(exc),
            "error_id": error_id
        }
    )


def tag_already_exists_error_handler(request: Request, exc: TagAlreadyExistsError):
    error_id = str(uuid.uuid4())
    logger.warning(exc)
    return JSONResponse(
        status_code=400,
        content={
            "message": str(exc),
            "error_id": error_id
        }
    )
