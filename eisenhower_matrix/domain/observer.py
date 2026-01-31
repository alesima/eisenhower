"""Observer Port Interface"""

from abc import ABC, abstractmethod


class IObserver(ABC):
    """
    Port: Observer Interface
    
    Defines how the domain notifies external systems of changes.
    Follows Interface Segregation Principle - single method interface.
    """
    
    @abstractmethod
    def on_tasks_changed(self) -> None:
        """Notify that tasks have changed"""
        pass
