"""Domain tests for the Project entity."""

import pytest

from eisenhower_matrix.domain.project import Project


def test_create_project():
    project = Project.create("p1", "  My Tasks  ", "desc")
    assert project.id == "p1"
    assert project.name == "My Tasks"
    assert project.created
    assert project.last_accessed


def test_create_project_rejects_empty_name():
    with pytest.raises(ValueError):
        Project.create("p1", "   ")


def test_update_and_accessed():
    project = Project.create("p1", "Old")
    project.update_details(name="New", description="d")
    assert project.name == "New"
    assert project.description == "d"
    with pytest.raises(ValueError):
        project.update_details(name="  ")
    old = project.last_accessed
    project.mark_accessed()
    assert project.last_accessed >= old
