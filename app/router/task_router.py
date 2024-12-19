from fastapi import APIRouter
from controller.TaskController import TaskController
from model.Task import Task


router = APIRouter()

@router.get("/")
async def get_all_task():
    return await TaskController.get_all_task()

@router.get("/{task_id}")
async def get_task_by_id(task_id: int):
    return await TaskController.get_task_by_id(task_id=task_id)

@router.post("/")
async def add_task(task: Task):
    return await TaskController.add_task(task=task)

@router.put("/")
async def update_task(task: Task):
    return await TaskController.update_task(task=task)

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    return await TaskController.delete_task(task_id=task_id)