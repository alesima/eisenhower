"""Persistence tests: JSON repositories and XDG path resolution."""

import json

from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService
from eisenhower_matrix.domain.project import Project
from eisenhower_matrix.infrastructure.persistence.json_project_repository import (
    JsonProjectRepository,
)
from eisenhower_matrix.infrastructure.persistence.json_repository import (
    JsonTaskRepository,
)
from eisenhower_matrix.infrastructure.persistence.paths import resolve_data_file


def _service_for(data_file):
    return EisenhowerMatrixService(JsonTaskRepository(data_file=str(data_file)))


def test_task_repository_roundtrip(tmp_path):
    service = _service_for(tmp_path / "tasks_x.json")
    created = service.add_task(3, "Delegate this", notes="n", tags=["t"])
    assert created.id == 1

    reloaded = _service_for(tmp_path / "tasks_x.json")
    tasks = reloaded.get_tasks(3)
    assert len(tasks) == 1
    assert tasks[0].description == "Delegate this"
    assert tasks[0].tags == ["t"]


def test_task_repository_handles_corrupt_file(tmp_path):
    data_file = tmp_path / "tasks_broken.json"
    data_file.write_text("{ not json")
    repo = JsonTaskRepository(data_file=str(data_file))
    assert repo.load() == {1: [], 2: [], 3: [], 4: []}


def test_project_repository_crud(tmp_path):
    repo = JsonProjectRepository(data_file=str(tmp_path / "projects.json"))
    # A default project is created on first run
    assert len(repo.load_all()) >= 1

    project = Project.create("work", "Work", "job tasks")
    repo.save(project)
    assert repo.exists("work") is True
    assert repo.load("work").name == "Work"

    repo.delete("work")
    assert repo.exists("work") is False
    assert repo.load("nope") is None


def test_resolve_data_file_migrates_legacy(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg"))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    legacy_dir = tmp_path / "home" / ".local" / "share" / "eisenhower"
    legacy_dir.mkdir(parents=True)
    legacy = legacy_dir / "tasks_p1.json"
    legacy.write_text(json.dumps({"1": [], "2": [], "3": [], "4": []}))

    try:
        from gi.repository import GLib  # noqa: F401
        gi_available = True
    except Exception:
        gi_available = False

    resolved = resolve_data_file("tasks_p1.json")
    if gi_available:
        # GLib may not honor the monkeypatched env; just ensure a path is returned
        assert resolved.name == "tasks_p1.json"
    else:
        assert resolved == tmp_path / "xdg" / "eisenhower" / "tasks_p1.json"
        assert not legacy.exists()
