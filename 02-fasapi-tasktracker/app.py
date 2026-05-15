from pydantic import BaseModel
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()
task_db = []

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime

class TaskUpdate(BaseModel):
    
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    

@app.post("/tasks", response_model= TaskResponse)
def create_task(tasks: TaskCreate):
    task = {
        "id": len(task_db)+1,
    "title": tasks.title,
    "description": tasks.description,
    "status": tasks.status, 
    "created_at": datetime.now()
    }
    task_db.append(task)
    return task
    
@app.get("/tasks", response_model= List[TaskResponse])
def all_tasks():
    return task_db

@app.get("/tasks/{task_id}", response_model= TaskResponse)
def get_task_by_id(task_id: int):
    for task in task_db:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail=f"Task with task id '{task_id} not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in task_db:
        if task["id"] == task_id:
            task_db.remove(task)
            return f"Task with  task id {task_id} deleted successfully"

    raise HTTPException(status_code=404,detail=f"Task with task id '{task_id}' not found")

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, update_task: TaskUpdate):
    for task in task_db:
        if task["id"] == task_id:
            if update_task.title is not None:
                task["title"] = update_task.title
            if update_task.description is not None:
                task["description"] = update_task.description
            if update_task.status is not None:
                task["status"] = update_task.status
            return task
    raise HTTPException(status_code=404,detail=f"Task with task id '{task_id}' not found")
    