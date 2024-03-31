from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import asyncio

app = FastAPI()

# uvicorn main:app - ввести в терминале для запуска веб-сервера, ctrl+c в терминале для остановки
# зависимости в requirements.txt


class Task(BaseModel):
    duration: int


tasks = {}


async def task_worker(task_id: str, duration: int):
    await asyncio.sleep(duration)
    tasks[task_id] = "done"


# задача создается при получении POST запроса с json вида {"duration": 50}
# в ответ возвращается IВ, под которым задача "выполняется"
@app.post("/task", response_model=dict)
async def create_task(task: Task):
    task_id = str(uuid.uuid4())
    tasks[task_id] = "running"
    asyncio.create_task(task_worker(task_id, task.duration))
    return {"task_id": task_id}


# get запрос на этот маршрут возвращает текущий статус задачи (running/done/not found)
@app.get("/task/{task_id}", response_model=dict)
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": tasks[task_id]}


# здесь можно увидеть словарь во всеми текущими задачами
@app.get("/tasks", response_model=dict)
async def get_all_tasks():
    return tasks
