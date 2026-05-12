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