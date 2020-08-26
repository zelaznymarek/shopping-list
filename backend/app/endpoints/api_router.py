from fastapi import APIRouter

from . import user, login, health

api_router = APIRouter()

api_router.include_router(login.router, tags=['login'])
api_router.include_router(health.router, prefix='/health', tags=['health checks'])
api_router.include_router(user.router, prefix='/users', tags=['users'])
