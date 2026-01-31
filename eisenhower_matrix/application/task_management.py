"""Task Management Use Case"""

from typing import List, Optional, Dict
from eisenhower_matrix.domain import Task, IObserver
from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService


class TaskManagementUseCase:
    """
    Coordinates task management operations.
    
    For simple applications, this delegates to the domain service.
    In complex scenarios, it could coordinate multiple services,
    handle transactions, apply authorization, etc.
    """
    
    def __init__(self, matrix_service: EisenhowerMatrixService):
        self._service = matrix_service
    
    def create_task(
        self,
        quadrant: int,
        description: str,
        due_date: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Task:
        """Create a new task in the specified quadrant"""
        return self._service.add_task(quadrant, description, due_date, notes)
    
    def update_task(
        self,
        quadrant: int,
        task_id: int,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        notes: Optional[str] = None
    ) -> bool:
        """Update an existing task"""
        return self._service.update_task(
            quadrant, task_id, description, due_date, notes
        )
    
    def complete_task(self, quadrant: int, task_id: int) -> bool:
        """Mark a task as completed"""
        return self._service.complete_task(quadrant, task_id)
    
    def delete_task(self, quadrant: int, task_id: int) -> bool:
        """Delete a task"""
        return self._service.remove_task(quadrant, task_id)
    
    def move_task(self, from_quadrant: int, to_quadrant: int, task_id: int) -> bool:
        """Move a task between quadrants"""
        return self._service.move_task(from_quadrant, to_quadrant, task_id)
    
    def get_tasks_by_quadrant(self, quadrant: int) -> List[Task]:
        """Get all tasks in a quadrant"""
        return self._service.get_tasks(quadrant)
    
    def get_all_tasks(self) -> Dict[int, List[Task]]:
        """Get all tasks organized by quadrant"""
        return {q: self._service.get_tasks(q) for q in range(1, 5)}
    
    def subscribe_to_changes(self, observer: IObserver) -> None:
        """Subscribe to task change notifications"""
        self._service.add_observer(observer)
    
    def unsubscribe_from_changes(self, observer: IObserver) -> None:
        """Unsubscribe from task change notifications"""
        self._service.remove_observer(observer)
