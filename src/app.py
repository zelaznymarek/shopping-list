from fastapi import FastAPI

from src.routes import category

app = FastAPI()
app.include_router(category.router)
