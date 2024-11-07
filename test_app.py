import pytest
from app import app,tasks,users  


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_tasks():
    tasks.clear()

@pytest.fixture(autouse=True)
def clear_users():
    users.clear()
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Task Management API!" in response.data

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    assert response.json["title"] == "Test Task"
    assert response.json["completed"] is False

def test_create_task_no_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert response.json["error"] == "Task title is required!"

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Test Task 1"})
    client.post("/tasks", json={"title": "Test Task 2"})
    response = client.get("/tasks")
    print(response)
    assert response.status_code == 200
    assert len(response.json["tasks"]) == 2

def test_update_task(client):
    client.post("/tasks", json={"title": "Test Task"})
    response = client.put("/tasks/1", json={"completed": True})
    assert response.status_code == 200
    assert response.json["completed"] is True

def test_update_task_not_found(client):
    response = client.put("/tasks/999", json={"completed": True})
    assert response.status_code == 404
    assert response.json["error"] == "Task not found!"

def test_delete_task(client):
    client.post("/tasks", json={"title": "Test Task"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"

def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"

def test_register_user(client):
    response = client.post("/users", json={"username": "testuser"})
    assert response.status_code == 201
    assert response.json["username"] == "testuser"

def test_register_user_no_username(client):
    response = client.post("/users", json={})
    assert response.status_code == 400
    assert response.json["error"] == "Username is required!"

def test_get_users(client):
    client.post("/users", json={"username": "testuser1"})
    client.post("/users", json={"username": "testuser2"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json["users"]) == 2
