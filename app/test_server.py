import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.server import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "uptime" in data

def test_api_info():
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_user_by_id():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == 1

def test_get_user_not_found():
    response = client.get("/api/users/999")
    assert response.status_code == 404

def test_create_user():
    new_user = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = client.post("/api/users", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == new_user["name"]
    assert data["data"]["email"] == new_user["email"]

def test_create_user_missing_fields():
    response = client.post("/api/users", json={"name": "Test User"})
    assert response.status_code == 422  # Validation error

def test_update_user():
    # First create a user
    new_user = {
        "name": "Update Test",
        "email": "update@example.com"
    }
    create_response = client.post("/api/users", json=new_user)
    user_id = create_response.json()["data"]["id"]
    
    # Update the user
    update_data = {"name": "Updated Name"}
    response = client.put(f"/api/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Updated Name"

def test_delete_user():
    # First create a user
    new_user = {
        "name": "Delete Test",
        "email": "delete@example.com"
    }
    create_response = client.post("/api/users", json=new_user)
    user_id = create_response.json()["data"]["id"]
    
    # Delete the user
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    # Verify user is deleted
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404

