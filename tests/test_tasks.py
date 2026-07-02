def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_list_tasks_sorted_by_priority(client):
    res = client.get("/api/tasks/")
    assert res.status_code == 200
    body = res.get_json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert "priority" in body[0]


def test_create_task(client):
    res = client.post(
        "/api/tasks/",
        json={"title": "Edit episode 1", "due_date": "2026-07-05", "important": True},
    )
    assert res.status_code == 201
    assert res.get_json()["title"] == "Edit episode 1"


def test_create_task_missing_fields(client):
    res = client.post("/api/tasks/", json={"title": "No due date"})
    assert res.status_code == 400


def test_create_task_invalid_due_date(client):
    res = client.post(
        "/api/tasks/", json={"title": "Bad date", "due_date": "nonsense"}
    )
    assert res.status_code == 400


def test_delete_unknown_task(client):
    res = client.delete("/api/tasks/9999")
    assert res.status_code == 404


def test_delete_existing_task(client):
    created = client.post(
        "/api/tasks/", json={"title": "Temp task", "due_date": "2026-08-01"}
    )
    task_id = created.get_json()["id"]
    res = client.delete(f"/api/tasks/{task_id}")
    assert res.status_code == 204
