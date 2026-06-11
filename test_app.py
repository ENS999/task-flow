import os
os.environ["DB_NAME"] = "taskflow_test"

from fastapi.testclient import TestClient
from main import app
from manager import Manager

client = TestClient(app)

cleanup_manager = Manager()
cleanup_manager.cursor.execute("DELETE FROM task_tags")
cleanup_manager.cursor.execute("DELETE FROM tasks")
cleanup_manager.cursor.execute("DELETE FROM categories")
cleanup_manager.cursor.execute("DELETE FROM tags")
cleanup_manager.cursor.execute("DELETE FROM users")
cleanup_manager.commit()
cleanup_manager.close()

def register_and_login(name, password):
    reg = client.post("/register", json={
        "username": name,
        "password": password
    })
    response = client.post("/login", json={
        "username": name,
        "password": password
    })
    headers = {"Authorization": f"Bearer {response.json()['token']}"}
    user_id = reg.json()["user_id"]
    return headers, user_id

def test_register():
    response = client.post("/register", json={
        "username": "test_register",
        "password": "123456"
    })
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data

def test_login():
    client.post("/register", json={
        "username": "test_login",
        "password": "123456"
    })

    response = client.post("/login", json={
        "username": "test_login",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "token" in response.json()

    invalid = client.post("/login", json={
        "username": "test_login1",
        "password": "123456"
    })
    assert invalid.status_code == 401

def test_post_categories():
    headers, user_id = register_and_login("test_post_categories", "123456")
    response = client.post("/categories", json={
        "name": "work"
    }, headers=headers)
    assert response.status_code == 201

    response = client.post("/categories", json={
        "name": "work"
    }, headers=headers)
    assert response.status_code == 409

    response = client.post("/categories", json={
        "name": "learn"
    })
    assert response.status_code == 401

    response = client.post("/categories", json={
        "name": 1111111
    }, headers=headers)
    assert response.status_code == 422

def test_get_categories():
    headers, user_id = register_and_login("test_get_categories", "123456")
    response = client.get("/categories", headers=headers)
    assert response.status_code == 200

    response = client.get("/categories")
    assert response.status_code == 401

def test_post_tags():
    headers, user_id = register_and_login("test_post_tags", "123456")
    response = client.post("/tags", json={
        "name": "test"
    }, headers=headers)
    assert response.status_code == 201

    response = client.post("/tags", json={
        "name": "test"
    }, headers=headers)
    assert response.status_code == 409

    response = client.post("/tags", json={
        "name": 11111
    }, headers=headers)
    assert response.status_code == 422

def test_get_tags():
    headers, user_id = register_and_login("test_get_tags", "123456")
    response = client.get("/tags", headers=headers)
    assert response.status_code == 200

    response = client.get("/tags")
    assert response.status_code == 401

def get_category_task_tag(username, category_name, title, status, priority, tag_name):
    headers, user_id = register_and_login(username, "123456")
    categories = client.post("/categories", json={
        "name": category_name
    }, headers=headers)
    category_id = categories.json()['category_id']

    tasks = client.post("/tasks", json={
        "title": title,
        "status": status,
        "priority": priority,
        "category_id": category_id
    }, headers=headers)
    task_id = tasks.json()['task_id']

    tags = client.post("/tags", json={
        "name": tag_name
    }, headers=headers)
    tag_id = tags.json()['tag_id']
    return category_id, task_id, tag_id, headers

def test_post_tasks_tags():
    category_id, task_id, tag_id, headers = get_category_task_tag("test_post_tasks_tags", "learn", "test", "todo", "low", "test_tag")

    response = client.post(f"/tasks/{task_id}/tags", json={
        "tag_id": tag_id,
    }, headers=headers)
    assert response.status_code == 201

    response = client.post(f"/tasks/{task_id}/tags", json={
        "tag_id": tag_id
    })
    assert response.status_code == 401

    response = client.post(f"/tasks/{99}/tags", json={
        "tag_id": tag_id,
    }, headers=headers)
    assert response.status_code == 404

    response = client.post(f"/tasks/{task_id}/tags", json={
        "tag_id": tag_id,
    }, headers=headers)
    assert response.status_code == 409

    response = client.post(f"/tasks/{task_id}/tags", json={
        "tag_id": "tag_id"
    }, headers=headers)
    assert response.status_code == 422

def test_remove_task_tag():
    category_id, task_id, tag_id, headers = get_category_task_tag("test_remove_task_tag", "learn2", "test2", "todo", "low", "test_tag2")
    client.post(f"/tasks/{task_id}/tags", json={"tag_id": tag_id}, headers=headers)

    response = client.delete(f"/tasks/{task_id}/tags/{tag_id}", headers=headers)
    assert response.status_code == 200

    response = client.delete(f"/tasks/{task_id}/tags/{tag_id}")
    assert response.status_code == 401

    response = client.delete(f"/tasks/{99}/tags/{99}", headers=headers)
    assert response.status_code == 404

    response = client.delete("/tasks/abc/tags/abc", headers=headers)
    assert response.status_code == 422

def test_post_task():
    headers, user_id = register_and_login("test_post_task", "123456")
    categories = client.post("/categories", json={
        "name": "learn3"
    }, headers=headers)
    category_id = categories.json()['category_id']

    response = client.post("/tasks", json={
        "title": "test_post_task",
        "status": "todo",
        "priority": "low",
        "category_id": category_id
    }, headers=headers)
    assert response.status_code == 201

    response = client.post("/tasks", json={
        "title": "test_post_task2",
        "status": "todo",
        "priority": "low",
        "category_id": category_id
    })
    assert response.status_code == 401

    response = client.post("/tasks", json={
        "title": "test_post_task3",
        "status": "todo",
        "priority": "low",
        "category_id": 99
    }, headers=headers)
    assert response.status_code == 404

    response = client.post("/tasks", json={
        "title": "test_post_task4",
        "status": "todo",
        "priority": "low",
        "category_id": "category_id"
    }, headers=headers)
    assert response.status_code == 422

def test_get_tasks():
    category_id, task_id, tag_id, headers = get_category_task_tag("test_get_tasks", "learn4", "test4", "todo", "low", "test_tag4")
    response = client.get("/tasks", headers=headers)
    assert response.status_code == 200

    response = client.get("/tasks")
    assert response.status_code == 401

    response = client.get("/tasks?status=banana", headers=headers)
    assert response.status_code == 422

def test_get_task():
    category_id, task_id, tag_id, headers = get_category_task_tag("test_get_task", "learn5", "test5", "todo", "low", "test_tag5")
    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data['task_id'] == task_id
    assert data['status'] == "todo"

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 401

    response = client.get(f"/tasks/{99}", headers=headers)
    assert response.status_code == 404

    response = client.get("/tasks/abc", headers=headers)
    assert response.status_code == 422

def test_put_task():
    headers, user_id = register_and_login("test_put_task", "123456")
    categories = client.post("/categories", json={
        "name": "learn6"
    }, headers=headers)
    category_id = categories.json()['category_id']

    tasks = client.post("/tasks", json={
        "title": "test_put_task",
        "status": "todo",
        "priority": "low",
        "category_id": category_id
    }, headers=headers)
    task_id = tasks.json()['task_id']

    response = client.put(f"/tasks/{task_id}", json={
        "title": "test_put_task2",
        "status": "in_progress",
        "priority": "medium",
        "category_id": category_id
    }, headers=headers)
    assert response.status_code == 200

    response = client.put(f"/tasks/{task_id}", json={
        "title": "test_put_task2",
        "status": "in_progress",
        "priority": "medium",
        "category_id": category_id
    })
    assert response.status_code == 401

    response = client.put(f"/tasks/{task_id}", json={
        "title": "test_put_task2",
        "status": "in_progress",
        "priority": "medium",
        "category_id": 99
    }, headers=headers)
    assert response.status_code == 404

    response = client.put("/tasks/99", json={
        "title": "test",
        "status": "todo",
        "priority": "low",
        "category_id": category_id
    }, headers=headers)
    assert response.status_code == 404

    response = client.put(f"/tasks/{task_id}", json={
        "title": "test_put_task2",
        "status": "in_progress",
        "priority": "medium",
        "category_id": "category_id"
    }, headers=headers)
    assert response.status_code == 422

    client.put(f"/tasks/{task_id}", json={
        "title": "test_put_task2",
        "status": "done",
        "priority": "high",
        "category_id": category_id
    }, headers=headers)

    response = client.put(f"/tasks/{task_id}", json={
        "title": "test_put_task2",
        "status": "todo",
        "priority": "low",
        "category_id": category_id
    }, headers=headers)
    assert response.status_code == 403

def test_del_task():
    category_id, task_id, tag_id, headers = get_category_task_tag("test_del_task", "learn7", "test7", "todo", "low", "test_tag7")
    response = client.delete("/tasks/abc", headers=headers)
    assert response.status_code == 422

    response = client.delete(f"/tasks/{99}", headers=headers)
    assert response.status_code == 404

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 401

    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200