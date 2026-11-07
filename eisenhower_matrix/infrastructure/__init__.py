"""Infrastructure Package

NOTE: the GTK UI subpackage is intentionally NOT imported here. It requires
gi (PyGObject/GTK), which is unavailable in headless environments such as
CI test runners. Import it explicitly where needed:
  from eisenhower_matrix.infrastructure.ui import EisenhowerApp, MainWindow
"""

from eisenhower_matrix.infrastructure.persistence import JsonTaskRepository
from eisenhower_matrix.infrastructure.persistence.json_project_repository import JsonProjectRepository

__all__ = ['JsonTaskRepository', 'JsonProjectRepository']
