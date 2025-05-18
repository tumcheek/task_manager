from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import APIRouter, FastAPI

from core import SENTRY_DSN, PROFILING, LOGGING_CONFIG
from core.database import SESSION
from exception_handlers import (
    general_exception_handler,
    task_not_found_exception_handler,
    tag_not_found_exception_handler,
    tag_not_associated_error_handler,
    tag_already_exists_error_handler,
)
from middleware import LoggingMiddleware, profile_request
from routers import auth, tasks, tags, projects
from seeds import seed_roles
from services.exeptions import (
    TaskNotFoundError,
    TagNotFoundError,
    TagNotAssociatedError,
    TagAlreadyExistsError,
)
import sentry_sdk


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = SESSION()
    try:
        seed_roles(session)
    finally:
        session.close()
    yield


dictConfig(LOGGING_CONFIG)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tasks.router)
api_router.include_router(tags.router)
api_router.include_router(projects.router)

sentry_sdk.init(dsn=SENTRY_DSN, environment="development")

app = FastAPI(title="Task manager", lifespan=lifespan)


app.include_router(api_router, prefix="/api/v1")
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(TaskNotFoundError, task_not_found_exception_handler)
app.add_exception_handler(TagNotFoundError, tag_not_found_exception_handler)
app.add_exception_handler(TagNotAssociatedError, tag_not_associated_error_handler)
app.add_exception_handler(TagAlreadyExistsError, tag_already_exists_error_handler)

app.add_middleware(LoggingMiddleware)

if PROFILING and PROFILING.isdigit() and bool(int(PROFILING)):
    app.middleware("http")(profile_request)
