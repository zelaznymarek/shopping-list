from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/health')
async def health_check():
    return {'alive': 'True'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
