"""
AWS Lab — Mini Project 01
FastAPI app deployed on EC2.
A small but real API: info, health check, system metadata, and a calculator.
"""

from datetime import datetime
import platform
import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# create the FasAPI App

app = FastAPI(title="AWS Lab - Fast API on EC2", description="Mini project", version="1.0.0")

START_TIME = datetime.now()
users_db = []

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
    new_id = len(users_db) + 1
    user_record = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "password": user.password,}

    users_db.append(user_record)
    print(user_record)
    return user_record

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    for user in users_db:
        if user['id'] == user_id:
            return user
    raise HTTPException(
        status_code=404,
        detail=f"User with id {user_id} not found",
    )



@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserUpdate):

    for user in users_db:
        if user["id"] == user_id:
            if updated_user.name is not None:
                user["name"] = updated_user.name
            if updated_user.email is not None:
                user["email"] = updated_user.email
            if updated_user.password is not None:
                user["password"] = updated_user.password
            return user
    raise HTTPException(status_code= 404, detail=f"user with id {user_id} not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            users_db.remove(user)
            return{"message: user with id '{user_id}' is removed "}
    raise HTTPException (status_code=404, detail=f"USER WITH {user_id} not found")
        
