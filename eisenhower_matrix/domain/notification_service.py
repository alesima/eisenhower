"""Notification Service Port Interface"""

from abc import ABC, abstractmethod
from eisenhower_matrix.domain.task import Task


class INotificationService(ABC):
    """
    Port: Notification Service Interface
    
    Defines how the domain can send notifications.
    Open/Closed: Can add new notification types without modifying domain.
    """
    
    @abstractmethod
    def notify_task_added(self, task: Task, quadrant: int) -> None:
        """Notify when a task is added"""
        pass
    
    @abstractmethod
    def notify_task_completed(self, task: Task, quadrant: int) -> None:
        """Notify when a task is completed"""
        pass
    
    @abstractmethod
    def notify_task_deleted(self, task: Task, quadrant: int) -> None:
        """Notify when a task is deleted"""
        pass
