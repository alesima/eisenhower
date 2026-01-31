"""Task Repository Port Interface"""

from abc import ABC, abstractmethod
from typing import Dict, List
from eisenhower_matrix.domain.task import Task


class ITaskRepository(ABC):
    """
    Port: Task Repository Interface
    
    Defines how the domain interacts with persistence.
    Implementations (adapters) must conform to this contract.
    
    Interface Segregation: Only essential methods for task persistence
    """
    
    @abstractmethod
    def save(self, tasks: Dict[int, List[Task]]) -> None:
        """Save all tasks to persistent storage"""
        pass
    
    @abstractmethod
    def load(self) -> Dict[int, List[Task]]:
        """Load all tasks from persistent storage"""
        pass
    
    @abstractmethod
    def export_to_file(self, filepath: str, tasks: Dict[int, List[Task]]) -> None:
        """Export tasks to a file"""
        pass
    
    @abstractmethod
    def import_from_file(self, filepath: str) -> Dict[int, List[Task]]:
        """Import tasks from a file"""
        pass
