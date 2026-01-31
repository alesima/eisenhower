"""
UI Infrastructure Layer - GTK Adapters

This module contains UI adapters that connect the domain to GTK presentation.
"""

from eisenhower_matrix.infrastructure.ui.application import EisenhowerApp, main
from eisenhower_matrix.infrastructure.ui.main_window import MainWindow
from eisenhower_matrix.infrastructure.ui.quadrant_panel import QuadrantPanel
from eisenhower_matrix.infrastructure.ui.task_dialog import TaskDialog
from eisenhower_matrix.infrastructure.ui.task_row import TaskRow
from eisenhower_matrix.infrastructure.ui.observer_adapter import GtkObserverAdapter

__all__ = [
    'EisenhowerApp',
    'MainWindow',
    'QuadrantPanel',
    'TaskDialog',
    'TaskRow',
    'GtkObserverAdapter',
    'main',
]
