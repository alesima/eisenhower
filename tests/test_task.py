"""Domain tests for the Task entity."""

from datetime import datetime, timedelta

import pytest

from eisenhower_matrix.domain.task import Task


def test_create_task_with_description():
    task = Task.create(1, "  Fix bug  ")
    assert task.id == 1
    assert task.description == "Fix bug"
    assert task.completed is False
    assert task.created


def test_create_task_rejects_empty_description():
    with pytest.raises(ValueError):
        Task.create(1, "   ")


def test_complete_uncomplete_cycle():
    task = Task.create(1, "Do it")
    task.mark_completed()
    assert task.completed is True
    assert task.completed_at is not None
    task.mark_uncompleted()
    assert task.completed is False
    assert task.completed_at is None


def test_update_details_rejects_empty_description():
    task = Task.create(1, "Do it")
    with pytest.raises(ValueError):
        task.update_details(description="  ")
    task.update_details(description="Done better", notes="n", tags=["a"])
    assert task.description == "Done better"
    assert task.notes == "n"
    assert task.tags == ["a"]


def test_overdue_and_due_soon():
    yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
    soon = (datetime.now() + timedelta(days=1)).date().isoformat()
    later = (datetime.now() + timedelta(days=30)).date().isoformat()

    assert Task.create(1, "a", due_date=yesterday).is_overdue() is True
    assert Task.create(2, "b", due_date=soon).is_overdue() is False
    assert Task.create(3, "c", due_date=soon).is_due_soon() is True
    assert Task.create(4, "d", due_date=later).is_due_soon() is False
    assert Task.create(5, "e", due_date="not-a-date").is_overdue() is False

    done = Task.create(6, "f", due_date=yesterday)
    done.mark_completed()
    assert done.is_overdue() is False


def test_matches_search():
    task = Task.create(1, "Deploy hotfix", notes="production issue", tags=["Work", "urgent"])
    assert task.matches_search("") is True
    assert task.matches_search("hotfix") is True
    assert task.matches_search("PRODUCTION") is True
    assert task.matches_search("work") is True
    assert task.matches_search("nope") is False
