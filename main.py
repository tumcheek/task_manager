from fastapi import APIRouter, FastAPI

from routers import auth, tasks, tags

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tasks.router)
api_router.include_router(tags.router)

app = FastAPI()


app.include_router(api_router)
