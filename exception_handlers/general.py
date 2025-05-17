import logging
import uuid

from fastapi import Request
from fastapi.responses import JSONResponse
from sentry_sdk import capture_exception


logger = logging.getLogger(__name__)


def general_exception_handler(request: Request, exc: Exception):
    capture_exception(exc)
    error_id = str(uuid.uuid4())
    logger.error(
        f"Unhandled exception [{error_id}] during {request.method} "
        f"{request.url}:\n{exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected server error occurred. Please try again later.",
            "error_id": error_id,
        },
    )
