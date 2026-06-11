def test_user_journey(api):
    register = api.post("/register", data={
        "username": "test_e2e",
        "password": "123456"
    })
    assert register.status == 201

    login = api.post("/login", data={
        "username": "test_e2e",
        "password": "123456"
    })
    assert login.status == 200
    token = login.json()['token']
    headers = {"Authorization": f"Bearer {token}"}

    category = api.post("/categories", data={
        "name": "test"
    }, headers=headers)
    assert category.status == 201
    category_id = category.json()['category_id']

    task = api.post("/tasks", data={
        "title": "first e2e task",
        "status": "todo",
        "priority": "low",
        "category_id": category_id
    }, headers=headers)
    assert task.status == 201
    task_id = task.json()['task_id']

    get_task = api.get(f"/tasks/{task_id}", headers=headers)
    assert get_task.status == 200
    assert get_task.json()['title'] == "first e2e task"