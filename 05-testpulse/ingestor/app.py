from datetime import datetime, timezone
from uuid import uuid4
from http import HTTPStatus

from fastapi import FastAPI, status
from models import TestRunRequest, TestRunResponse

app = FastAPI(
    title="TestPulse Ingestor", 
    version="0.1.0", 
    description="Receives test results from CI pipelines"
    )
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/results/json", status_code=status.HTTP_202_ACCEPTED, response_model=TestRunResponse)
def create_test_run(test_run: TestRunRequest):
    new_id=uuid4()
    current_time=datetime.now(timezone.utc)
    test_count=len(test_run.tests)
    
    return TestRunResponse(
        status="accepted",
        ingestion_id=new_id,
        received_at=current_time,
        test_count=test_count,
        source_format="json")
    
    



