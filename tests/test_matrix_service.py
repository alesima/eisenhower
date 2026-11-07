"""Application service tests with an in-memory repository."""

import pytest

from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService
from eisenhower_matrix.domain.task_repository import ITaskRepository


class InMemoryRepository(ITaskRepository):
    def __init__(self):
        self.stored = {1: [], 2: [], 3: [], 4: []}

    def load(self):
        return {q: list(tasks) for q, tasks in self.stored.items()}

    def save(self, tasks):
        self.stored = {q: list(t) for q, t in tasks.items()}

    def export_to_file(self, filepath, tasks):
        raise NotImplementedError

    def import_from_file(self, filepath):
        raise NotImplementedError


@pytest.fixture
def service():
    return EisenhowerMatrixService(InMemoryRepository())


def test_add_and_get_tasks(service):
    task = service.add_task(1, "Urgent fix", tags=["ops"])
    assert task.id == 1
    assert len(service.get_tasks(1)) == 1
    assert len(service.get_tasks(2)) == 0


def test_add_task_rejects_bad_quadrant(service):
    with pytest.raises(ValueError):
        service.add_task(5, "nope")
    with pytest.raises(ValueError):
        service.add_task(1, "   ")


def test_complete_and_uncomplete(service):
    task = service.add_task(1, "Fix")
    assert service.complete_task(1, task.id) is True
    assert service.get_tasks(1)[0].completed is True
    assert service.get_tasks(1, include_completed=False) == []
    assert service.uncomplete_task(1, task.id) is True
    assert service.get_tasks(1)[0].completed is False
    assert service.complete_task(1, 999) is False


def test_move_task_reassigns_id(service):
    task = service.add_task(1, "Move me")
    assert service.move_task(1, task.id, 2) is True
    assert service.get_tasks(1) == []
    moved = service.get_tasks(2)
    assert len(moved) == 1
    assert moved[0].description == "Move me"
    assert service.move_task(1, 999, 2) is False


def test_remove_and_reorder(service):
    service.add_task(1, "first")
    second = service.add_task(1, "second")
    assert service.reorder_task(1, second.id, "up") is True
    assert service.get_tasks(1)[0].description == "second"
    assert service.reorder_task(1, second.id, "up") is False
    assert service.remove_task(1, second.id) is True
    assert len(service.get_tasks(1)) == 1


def test_search_and_due_filters(service):
    from datetime import datetime, timedelta

    yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
    service.add_task(1, "Deploy hotfix", due_date=yesterday)
    service.add_task(2, "Plan roadmap")
    results = service.search_tasks("hotfix")
    assert list(results.keys()) == [1]
    overdue = service.get_overdue_tasks()
    assert list(overdue.keys()) == [1]
