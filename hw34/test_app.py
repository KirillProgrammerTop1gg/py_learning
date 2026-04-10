import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import uuid

# ── импорт приложения ──────────────────────────────────────────────────────────
from main import app, tasks

client = TestClient(app)

# ── фикстуры ──────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def clear_tasks():
    """Чистим глобальный словарь tasks перед каждым тестом."""
    tasks.clear()
    yield
    tasks.clear()


@pytest.fixture
def created_task():
    """Создаём одну задачу и возвращаем её task_id."""
    payload = {"name": "Do algebra HW", "description": "In book: 32.6, 32.8, 32.14"}
    resp = client.post("/tasks/", json=payload)
    assert resp.status_code == 201
    return resp.json()["task_id"]


# ══════════════════════════════════════════════════════════════════════════════
# POST /tasks/
# ══════════════════════════════════════════════════════════════════════════════


class TestCreateTask:

    def test_create_task_success(self):
        payload = {"name": "Do algebra HW", "description": "In book: 32.6, 32.8, 32.14"}
        resp = client.post("/tasks/", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["message"] == "Task created successfully"
        assert "task_id" in data

    def test_create_task_returns_uuid(self):
        payload = {
            "name": "Buy groceries",
            "description": "Milk, eggs, bread and butter",
        }
        resp = client.post("/tasks/", json=payload)
        task_id = resp.json()["task_id"]
        # Должен быть валидный UUID v4
        uuid.UUID(task_id, version=4)

    def test_create_duplicate_name_returns_409(self, created_task):
        payload = {"name": "Do algebra HW", "description": "Another description here"}
        resp = client.post("/tasks/", json=payload)
        assert resp.status_code == 409
        assert "already exists" in resp.json()["detail"]

    def test_create_task_name_too_short_returns_422(self):
        payload = {"name": "AB", "description": "Some valid description text"}
        resp = client.post("/tasks/", json=payload)
        assert resp.status_code == 422

    def test_create_task_name_too_long_returns_422(self):
        payload = {"name": "A" * 51, "description": "Some valid description text"}
        resp = client.post("/tasks/", json=payload)
        assert resp.status_code == 422

    def test_create_task_description_too_short_returns_422(self):
        payload = {"name": "Valid Name", "description": "Short"}
        resp = client.post("/tasks/", json=payload)
        assert resp.status_code == 422

    def test_create_task_description_too_long_returns_422(self):
        payload = {"name": "Valid Name", "description": "D" * 251}
        resp = client.post("/tasks/", json=payload)
        assert resp.status_code == 422

    def test_create_task_missing_name_returns_422(self):
        resp = client.post(
            "/tasks/", json={"description": "Some valid description text"}
        )
        assert resp.status_code == 422

    def test_create_task_missing_description_returns_422(self):
        resp = client.post("/tasks/", json={"name": "Valid Name"})
        assert resp.status_code == 422

    def test_create_task_empty_body_returns_422(self):
        resp = client.post("/tasks/", json={})
        assert resp.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# PUT /tasks/{task_id}
# ══════════════════════════════════════════════════════════════════════════════


class TestUpdateTask:

    def test_update_task_success(self, created_task):
        payload = {
            "name": "Updated Task Name",
            "description": "Updated description here!",
        }
        resp = client.put(f"/tasks/{created_task}", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Task updated successfully"
        assert data["task_id"] == created_task

    def test_update_task_same_name_allowed(self, created_task):
        """Обновление задачи с тем же именем (своим) должно проходить."""
        payload = {"name": "Do algebra HW", "description": "Changed description text!"}
        resp = client.put(f"/tasks/{created_task}", json=payload)
        assert resp.status_code == 200

    def test_update_task_not_found_returns_404(self):
        fake_id = str(uuid.uuid4())
        payload = {
            "name": "Some Task Name",
            "description": "Some valid description here",
        }
        resp = client.put(f"/tasks/{fake_id}", json=payload)
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Task not found"

    def test_update_task_duplicate_name_returns_409(self, created_task):
        """Имя другой задачи конфликтует → 409."""
        # Создаём вторую задачу
        client.post(
            "/tasks/",
            json={
                "name": "Second Task Here",
                "description": "Description for second task",
            },
        )
        payload = {
            "name": "Second Task Here",
            "description": "Trying to steal the name",
        }
        resp = client.put(f"/tasks/{created_task}", json=payload)
        assert resp.status_code == 409

    def test_update_task_invalid_uuid_returns_422(self):
        resp = client.put(
            "/tasks/not-a-uuid",
            json={"name": "Valid Name", "description": "Valid description here!"},
        )
        assert resp.status_code == 422

    def test_update_task_name_too_short_returns_422(self, created_task):
        resp = client.put(
            f"/tasks/{created_task}",
            json={"name": "AB", "description": "Valid description here!"},
        )
        assert resp.status_code == 422

    def test_update_task_description_too_long_returns_422(self, created_task):
        resp = client.put(
            f"/tasks/{created_task}",
            json={"name": "Valid Name", "description": "D" * 251},
        )
        assert resp.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# DELETE /tasks/{task_id}
# ══════════════════════════════════════════════════════════════════════════════


class TestDeleteTask:

    def test_delete_task_success(self, created_task):
        resp = client.delete(f"/tasks/{created_task}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "Task deleted successfully"
        assert data["task_id"] == created_task

    def test_delete_task_actually_removes_it(self, created_task):
        client.delete(f"/tasks/{created_task}")
        resp = client.get(f"/tasks/{created_task}")
        assert resp.status_code == 404

    def test_delete_task_not_found_returns_404(self):
        fake_id = str(uuid.uuid4())
        resp = client.delete(f"/tasks/{fake_id}")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Task not found"

    def test_delete_task_twice_returns_404(self, created_task):
        client.delete(f"/tasks/{created_task}")
        resp = client.delete(f"/tasks/{created_task}")
        assert resp.status_code == 404

    def test_delete_task_invalid_uuid_returns_422(self):
        resp = client.delete("/tasks/not-a-valid-uuid")
        assert resp.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# GET /tasks/{task_id}
# ══════════════════════════════════════════════════════════════════════════════


class TestGetTaskById:

    def test_get_task_success(self, created_task):
        resp = client.get(f"/tasks/{created_task}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["task_id"] == created_task
        assert data["name"] == "Do algebra HW"
        assert "description" in data

    def test_get_task_not_found_returns_404(self):
        fake_id = str(uuid.uuid4())
        resp = client.get(f"/tasks/{fake_id}")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Task not found"

    def test_get_task_invalid_uuid_returns_422(self):
        resp = client.get("/tasks/not-a-uuid")
        assert resp.status_code == 422

    def test_get_task_reflects_update(self, created_task):
        client.put(
            f"/tasks/{created_task}",
            json={
                "name": "Updated Task Name",
                "description": "Updated description for the task",
            },
        )
        resp = client.get(f"/tasks/{created_task}")
        assert resp.json()["name"] == "Updated Task Name"


# ══════════════════════════════════════════════════════════════════════════════
# GET /tasks/
# ══════════════════════════════════════════════════════════════════════════════


class TestGetAllTasks:

    def test_get_all_tasks_empty(self):
        resp = client.get("/tasks/")
        assert resp.status_code == 200
        assert resp.json() == {"tasks": []}

    def test_get_all_tasks_returns_created(self):
        client.post(
            "/tasks/",
            json={"name": "Task One Here", "description": "First task description"},
        )
        client.post(
            "/tasks/",
            json={"name": "Task Two Here", "description": "Second task description"},
        )
        resp = client.get("/tasks/")
        assert resp.status_code == 200
        tasks_list = resp.json()["tasks"]
        assert len(tasks_list) == 2

    def test_get_all_tasks_schema(self):
        client.post(
            "/tasks/",
            json={
                "name": "Schema Test Task",
                "description": "Checking response schema fields",
            },
        )
        resp = client.get("/tasks/")
        task = resp.json()["tasks"][0]
        assert "task_id" in task
        assert "name" in task
        assert "description" in task

    def test_get_all_tasks_decreases_after_delete(self):
        r1 = client.post(
            "/tasks/",
            json={"name": "Task One Here", "description": "First task description"},
        )
        client.post(
            "/tasks/",
            json={"name": "Task Two Here", "description": "Second task description"},
        )
        client.delete(f"/tasks/{r1.json()['task_id']}")
        resp = client.get("/tasks/")
        assert len(resp.json()["tasks"]) == 1

    def test_get_all_tasks_ids_are_valid_uuids(self):
        client.post(
            "/tasks/",
            json={
                "name": "UUID Check Task",
                "description": "Checking uuid format in list",
            },
        )
        resp = client.get("/tasks/")
        for task in resp.json()["tasks"]:
            uuid.UUID(task["task_id"], version=4)
