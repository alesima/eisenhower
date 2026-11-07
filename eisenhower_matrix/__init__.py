"""
Eisenhower Matrix - Task Prioritization Application

Hexagonal Architecture (Ports and Adapters):
- Domain: Core business logic and entities
- Application: Use cases and application services  
- Infrastructure: Adapters for persistence and UI

SOLID Principles applied throughout.
"""

__version__ = "1.1.0"
__author__ = "Alex Silva"

# Export domain abstractions
from eisenhower_matrix.domain import (
    Task,
    QuadrantInfo,
    ITaskRepository,
    IObserver,
)

# Export application services
from eisenhower_matrix.application import (
    EisenhowerMatrixService,
    TaskManagementUseCase,
    TaskExportUseCase,
    TaskImportUseCase
)

# NOTE: infrastructure (persistence/UI) is intentionally NOT imported here.
# The UI layer requires GTK/libadwaita (gi), which is unavailable in
# headless environments such as CI test runners. Import it explicitly:
#   from eisenhower_matrix.infrastructure import JsonTaskRepository, ...
#   from eisenhower_matrix.infrastructure.ui import EisenhowerApp, ...

__all__ = [
    'Task',
    'QuadrantInfo',
    'ITaskRepository',
    'IObserver',
    'EisenhowerMatrixService',
    'TaskManagementUseCase',
    'TaskExportUseCase',
    'TaskImportUseCase',
]
