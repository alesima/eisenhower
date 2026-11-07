"""Import/export use-case tests."""

import csv
import json

import pytest

from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService
from eisenhower_matrix.application.task_export import TaskExportUseCase
from eisenhower_matrix.application.task_import import TaskImportUseCase
from eisenhower_matrix.infrastructure.persistence.json_repository import (
    JsonTaskRepository,
)


@pytest.fixture
def service(tmp_path):
    svc = EisenhowerMatrixService(
        JsonTaskRepository(data_file=str(tmp_path / "tasks.json"))
    )
    svc.add_task(1, "Fix prod", notes="urgent", tags=["ops"])
    svc.add_task(2, "Plan Q3")
    return svc


def test_export_json_and_reimport(service, tmp_path):
    export = TaskExportUseCase(service)
    target = tmp_path / "backup.json"
    assert export.export_to_json(str(target)) is True
    payload = json.loads(target.read_text())
    assert payload

    fresh = EisenhowerMatrixService(
        JsonTaskRepository(data_file=str(tmp_path / "fresh.json"))
    )
    assert TaskImportUseCase(fresh).import_from_json(str(target)) is True
    assert len(fresh.get_tasks(1)) + len(fresh.get_tasks(2)) == 2


def test_export_csv_has_header(service, tmp_path):
    target = tmp_path / "tasks.csv"
    assert TaskExportUseCase(service).export_to_csv(str(target)) is True
    with open(target, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[0]["description"] == "Fix prod"


def test_export_markdown_mentions_quadrants(service, tmp_path):
    target = tmp_path / "tasks.md"
    assert TaskExportUseCase(service).export_to_markdown(str(target)) is True
    text = target.read_text(encoding="utf-8")
    assert "Quadrant 1" in text
    assert "Fix prod" in text


def test_import_csv_roundtrip(service, tmp_path):
    target = tmp_path / "tasks.csv"
    assert TaskExportUseCase(service).export_to_csv(str(target)) is True

    fresh = EisenhowerMatrixService(
        JsonTaskRepository(data_file=str(tmp_path / "from_csv.json"))
    )
    assert TaskImportUseCase(fresh).import_from_csv(str(target)) is True
    total = sum(len(fresh.get_tasks(q)) for q in (1, 2, 3, 4))
    assert total == 2
