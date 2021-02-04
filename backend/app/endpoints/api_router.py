from fastapi import APIRouter

from . import user, login, health, category, product, shopping_list

api_router = APIRouter()

api_router.include_router(login.router, tags=['login'])
api_router.include_router(health.router, prefix='/health', tags=['health checks'])
api_router.include_router(user.router, prefix='/users', tags=['users'])
api_router.include_router(category.router, prefix='/categories', tags=['categories'])
api_router.include_router(product.router, prefix='/products', tags=['products'])
api_router.include_router(shopping_list.router, prefix='/lists', tags=['lists'])
