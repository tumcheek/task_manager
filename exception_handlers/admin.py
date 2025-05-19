from fastapi import Request
from fastapi.responses import JSONResponse

from exeptions import AdminAccessRequired


def admin_access_required(request: Request, exc: AdminAccessRequired):
    return JSONResponse(status_code=403, content={"message": str(exc)})
