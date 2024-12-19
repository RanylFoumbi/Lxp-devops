import uvicorn
import os
from fastapi import FastAPI
from router.task_router import router

app = FastAPI()
app.include_router(router, prefix="/tasks")

@app.get("/")
async def read_root():
    return {"Welcome To": "Task API"}

if __name__ == "__main__":
    host = '0.0.0.0'
    port = int(os.getenv('API_PORT', 8000))   
    uvicorn.run(app, host=host, port=port)