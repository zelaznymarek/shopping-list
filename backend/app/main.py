from fastapi import FastAPI
import uvicorn

from app.routers import health


app = FastAPI()

app.include_router(health.router, prefix='/health', tags=['health checks'])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
