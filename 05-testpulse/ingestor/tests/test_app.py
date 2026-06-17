import os
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "ca-central-1"
from fastapi.testclient import TestClient
from moto import mock_aws
import json, boto3
from app import app


client = TestClient(app)

def test_health_return_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@mock_aws
def test_post_results_json_returns_202_on_valid_payload():
    s3_client = boto3.client('s3', region_name=os.environ["AWS_DEFAULT_REGION"])
    s3_client.create_bucket(Bucket="harita-testpulse-raw-2026", CreateBucketConfiguration={"LocationConstraint": "ca-central-1"})

    sqs_client = boto3.client('sqs', region_name=os.environ["AWS_DEFAULT_REGION"])
    sqs_client.create_queue(QueueName="harita-testpulse-ingestion-queue")

    payload = {
    "team": "callmetoremind",
    "project": "backend-service",
    "commit_sha": "abc1234567890abcdef1234567890abcdef12345",
    "branch": "main",
    "ci_run_id": "ci-run-2026-06-17-001",
    "timestamp": "2026-06-17T14:30:00Z",
    "tests": [
        {
            "name": "testCreateReminder",
            "status": "pass",
            "duration_ms": 142,
            "critical": False
        }
    ]
}

    response = client.post("/results/json", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "accepted"
    assert data["source_format"] == "json"
    assert data["test_count"] == 1
    assert "ingestion_id" in data   # exists, but value is random UUID
    assert "received_at" in data    # exists, but value is current time

@mock_aws
def test_post_results_json_returns_422_on_valid_payload():
    s3_client = boto3.client('s3', region_name=os.environ["AWS_DEFAULT_REGION"])
    s3_client.create_bucket(Bucket="harita-testpulse-raw-2026", CreateBucketConfiguration={"LocationConstraint": "ca-central-1"})

    sqs_client = boto3.client('sqs', region_name=os.environ["AWS_DEFAULT_REGION"])
    sqs_client.create_queue(QueueName="harita-testpulse-ingestion-queue")

    payload = {
    "project": "backend-service",
    "commit_sha": "abc1234567890abcdef1234567890abcdef12345",
    "branch": "main",
    "ci_run_id": "ci-run-2026-06-17-001",
    "timestamp": "2026-06-17T14:30:00Z",
    "tests": [
        {
            "name": "testCreateReminder",
            "status": "pass",
            "duration_ms": 142,
            "critical": False
        }
    ]
}

    response = client.post("/results/json", json=payload)
    assert response.status_code == 422
