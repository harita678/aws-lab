from app import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_root_return_200():
    response = client.get("/")
    assert response.status_code == 200

def test_root_return_service_info():
    response = client.get("/")
    data = response.json()
    assert "service" in data
    assert "version" in data


@pytest.fixture
def health_call():
    return client.get("/health")

def test_health_return_200(health_call):
    assert health_call.status_code == 200


def test_health_return_status(health_call):
    data = health_call.json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data

def test_health_return_uptime_seconds(health_call):
    data = health_call.json()
   # assert type(data["uptime_seconds"]) == float
    assert isinstance(data["uptime_seconds"], float)

def test_create_user_200():
    response = client.post("/users", json={"name": "Alice", "email": "a@x.com", "password": "secret"})
    assert response.status_code == 200


def test_get_user_by_id():
    response = client.post("/users", json={"name": "bob", "email": "b@x.com", "password": "secret"})
    created_user = response.json()
    user_id = created_user["id"]

    assert created_user["name"] == "bob"
    assert created_user["email"] == "b@x.com"

def test_get_nonexistent_user_404():
    response = client.get("/users/999")
    data = response.json()
    assert response.status_code == 404
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_update_user_changes_email():
    response = client.post("/users",json={"name": "bob", "email": "b@x.com", "password": "secret"})
    user_id = response.json()["id"]

    updated_response = client.put(f"/users/{user_id}", json = {"email": "abc@.com"})

    assert updated_response.status_code == 200
    updated_user = updated_response.json()
    assert updated_user["name"] == "bob"
    assert updated_user["email"] == "abc@.com"

    user = client.get(f"/users/{user_id}")
    user_info = user.json()
    assert user_info["name"] == "bob"
    assert user_info["email"] == "abc@.com"

def test_delete_user_removes_it():
    created_user = client.post("/users", json={"name": "bob", "email": "b@x.com", "password": "secret"})
    user_id = created_user.json()["id"]

    deleted_response = client.delete(f"/users/{user_id}")
    assert deleted_response.status_code == 200

    assert client.get(f"/users/{user_id}").status_code == 404
