"""
Eisenhower Matrix - Task Prioritization Application

Hexagonal Architecture (Ports and Adapters):
- Domain: Core business logic and entities
- Application: Use cases and application services  
- Infrastructure: Adapters for persistence and UI

SOLID Principles applied throughout.
"""

__version__ = "1.0.1"
__author__ = "Alex"

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

# Export infrastructure implementations
from eisenhower_matrix.infrastructure import JsonTaskRepository, EisenhowerApp, MainWindow

__all__ = [
    'Task',
    'QuadrantInfo',
    'ITaskRepository',
    'IObserver',
    'EisenhowerMatrixService',
    'JsonTaskRepository',
    'EisenhowerApp',
    'MainWindow',
    'TaskManagementUseCase',
    'TaskExportUseCase',
    'TaskImportUseCase',
]
