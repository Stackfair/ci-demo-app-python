from flask import Blueprint, jsonify, request

from app.utils.scoring import score_task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

# In-memory store - deliberately simple, no database dependency to keep CI fast/free-tier friendly
_tasks = [
    {"id": 1, "title": "Write CI pipeline", "due_date": "2026-07-02", "important": True},
    {"id": 2, "title": "Record voiceover", "due_date": "2026-07-10", "important": False},
]
_next_id = 3


@tasks_bp.get("/")
def list_tasks():
    scored = [
        {**task, "priority": score_task(task)} for task in _tasks
    ]
    scored.sort(key=lambda t: t["priority"], reverse=True)
    return jsonify(scored)


@tasks_bp.post("/")
def create_task():
    global _next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    due_date = data.get("due_date")
    important = bool(data.get("important", False))

    if not title or not due_date:
        return jsonify({"error": "title and due_date are required"}), 400

    try:
        score_task({"due_date": due_date, "important": important})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    task = {"id": _next_id, "title": title, "due_date": due_date, "important": important}
    _tasks.append(task)
    _next_id += 1
    return jsonify(task), 201


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id):
    global _tasks
    if not any(t["id"] == task_id for t in _tasks):
        return jsonify({"error": "Task not found"}), 404

    _tasks = [t for t in _tasks if t["id"] != task_id]
    return "", 204


@tasks_bp.get("/count")
def count_tasks():
    return jsonify({"count": len(_tasks)})
