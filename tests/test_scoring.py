from datetime import datetime, timezone

import pytest

from app.utils.scoring import score_task

NOW = datetime(2026, 7, 1, 0, 0, 0, tzinfo=timezone.utc)


def test_scores_overdue_tasks_highest():
    score = score_task({"due_date": "2026-06-25"}, NOW)
    assert score == 100


def test_scores_tasks_due_today():
    score = score_task({"due_date": "2026-07-01T12:00:00+00:00"}, NOW)
    assert score == 80


def test_adds_importance_bonus():
    base = score_task({"due_date": "2026-07-15"}, NOW)
    important = score_task({"due_date": "2026-07-15", "important": True}, NOW)
    assert important == base + 25


def test_raises_on_missing_due_date():
    with pytest.raises(ValueError, match="must include a due_date"):
        score_task({})


def test_raises_on_invalid_due_date():
    with pytest.raises(ValueError, match="valid ISO date string"):
        score_task({"due_date": "not-a-date"})
