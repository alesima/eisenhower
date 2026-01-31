"""GTK Observer Adapter"""

from typing import Callable
from eisenhower_matrix.domain import IObserver


class GtkObserverAdapter(IObserver):
    """
    Adapter that implements IObserver for GTK callbacks
    
    Single Responsibility: Bridge between domain observer and GTK callback
    Dependency Inversion: Domain uses IObserver, not GTK-specific code
    """
    
    def __init__(self, callback: Callable):
        self._callback = callback
    
    def on_tasks_changed(self) -> None:
        """Notify via GTK callback"""
        self._callback()
