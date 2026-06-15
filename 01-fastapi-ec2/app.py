"""
AWS Lab — Mini Project 01
FastAPI app deployed on EC2.
A small but real API: info, health check, system metadata, and a calculator.
"""

from datetime import datetime
import platform
import socket
import crud

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# create the FasAPI App

app = FastAPI(title="AWS Lab - Fast API on EC2", description="Mini project", version="1.0.0")

START_TIME = datetime.now()


# GET /  — service info (root endpoint)

@app.get("/")
def root():
    return{
        "service": "aws-lab-fastapi",
        "version": "1.0.0",
        "message": "Hello from AWS! Try /health, /system, or POST /calc"
    }

@app.get("/health")
def health():
    now = datetime.now()
    uptime_seconds = (now - START_TIME).total_seconds()
    return {
        "status": "healthy",
        "started_at": START_TIME.isoformat(),
        "uptime_seconds": round(uptime_seconds, 2),
    }
@app.get("/system")
def system_info():
    return{
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_release": platform.release(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
        "current_time": datetime.now().isoformat(),
    }
class CalcRequest(BaseModel):
    operation: str   # "add", "subtract", "multiply", "divide"
    a: float
    b: float


@app.post("/calc")
def calculate(req: CalcRequest):
  
    if req.operation == "add":
        result = req.a + req.b
    elif req.operation == "subtract":
        result = req.a - req.b
    elif req.operation == "multiply":
        result = req.a * req.b
    elif req.operation == "divide":
        if req.b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = req.a / req.b
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown operation '{req.operation}'. Use add/subtract/multiply/divide.",
        )

    return {
        "operation": req.operation,
        "a": req.a,
        "b": req.b,
        "result": result,
    }

@app.get("/greet/{name}")
def greet_person(name:str):
    return{
        "message": f"Hello, {name}",
        "length": len(name),
    }
@app.get("/search")
def search(q: str = "", limit: int = 10):
    return{
        "query_received": q,
        "limit_received": limit,
        "meesage": f"you searched for '{q}' with limit '{limit}'",
    }

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
        new_user = crud.create_user(user.name, user.email, user.password)
        return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    user = crud.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return user
    


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):

    updated_user_data = crud.update_user(user_id, updated_user.name, updated_user.email, updated_user.password)
    if updated_user_data is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return updated_user_data

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    deleted = crud.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return {"message": f"User {user_id} deleted successfully"}
