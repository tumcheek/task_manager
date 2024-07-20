from fastapi import APIRouter, FastAPI

from routers import auth

api_router = APIRouter()
api_router.include_router(auth.router)

app = FastAPI()


app.include_router(api_router)
