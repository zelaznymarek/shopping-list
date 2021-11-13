import uvicorn
from app.endpoints.api_router import api_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
