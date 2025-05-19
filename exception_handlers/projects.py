from fastapi import Request
from fastapi.responses import JSONResponse

from exeptions import ProjectPermissionError, ProjectNotFoundError


def project_permission_exception_handler(
    request: Request, exc: ProjectPermissionError
) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": str(exc)})


def project_not_found_exception_handler(
    request: Request, exc: ProjectNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})
