"""Task priority scoring.

Deliberately simple logic - just enough to give the test suite something
real to check, and something to visibly "break" for the pipeline-failure
video.
"""
from datetime import datetime, timezone


def score_task(task: dict, now: datetime | None = None) -> int:
    """Score a task's priority based on due date proximity and importance.

    Args:
        task: dict with a "due_date" ISO string and optional "important" bool.
        now: override for "current time" (used in tests).

    Returns:
        Priority score, higher = more urgent.

    Raises:
        ValueError: if due_date is missing or invalid.
    """
    if not task or not task.get("due_date"):
        raise ValueError("Task must include a due_date")

    try:
        due = datetime.fromisoformat(task["due_date"])
    except ValueError as exc:
        raise ValueError("due_date must be a valid ISO date string") from exc

    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)

    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)

    days_until_due = (due - current).total_seconds() / 86400

    if days_until_due < 0:
        score = 100  # overdue
    elif days_until_due < 1:
        score = 80  # due today
    elif days_until_due < 3:
        score = 50
    elif days_until_due < 7:
        score = 20
    else:
        score = 5

    if task.get("important"):
        score += 25

    return score
