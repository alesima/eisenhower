"""Application Service - Eisenhower Matrix Management"""

from typing import Dict, List, Optional
from eisenhower_matrix.domain.task import Task
from eisenhower_matrix.domain.quadrant_info import QuadrantInfo
from eisenhower_matrix.domain.task_repository import ITaskRepository
from eisenhower_matrix.domain.observer import IObserver


class EisenhowerMatrixService:
    """
    Application Service - Orchestrates task management operations
    
    Single Responsibility: Coordinate task operations across quadrants
    Open/Closed: Extensible through observers without modification
    Dependency Inversion: Depends on ITaskRepository abstraction, not concrete implementation
    """
    
    def __init__(self, repository: ITaskRepository):
        """
        Initialize with repository dependency (Dependency Injection)
        
        Args:
            repository: Implementation of ITaskRepository port
        """
        self._repository = repository
        self._tasks: Dict[int, List[Task]] = {}
        self._observers: List[IObserver] = []
        self._load_tasks()
    
    def _load_tasks(self) -> None:
        """Load tasks from repository"""
        self._tasks = self._repository.load()
    
    def add_observer(self, observer: IObserver) -> None:
        """
        Register an observer (Observer Pattern)
        
        Open/Closed: Can add new observers without modifying service
        """
        self._observers.append(observer)
    
    def remove_observer(self, observer: IObserver) -> None:
        """Remove an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self) -> None:
        """Notify all observers of changes"""
        for observer in self._observers:
            observer.on_tasks_changed()
    
    def _get_next_id(self, quadrant: int) -> int:
        """
        Generate next task ID for quadrant
        
        Single Responsibility: ID generation logic
        """
        if not self._tasks[quadrant]:
            return 1
        return max(task.id for task in self._tasks[quadrant]) + 1
    
    def add_task(self, quadrant: int, description: str, notes: str = "",
                 tags: Optional[List[str]] = None, 
                 metadata: Optional[Dict[str, str]] = None) -> Task:
        """
        Add a new task to specified quadrant
        
        Args:
            quadrant: Quadrant number (1-4)
            description: Task description
            notes: Additional notes
            tags: List of tags
            metadata: Custom key-value metadata
            
        Returns:
            Created Task entity
            
        Raises:
            ValueError: If quadrant is invalid or description is empty
        """
        if not QuadrantInfo.validate_quadrant(quadrant):
            raise ValueError(f"Invalid quadrant: {quadrant}")
        
        task_id = self._get_next_id(quadrant)
        task = Task.create(task_id, description, notes, tags, metadata)
        
        self._tasks[quadrant].append(task)
        self._repository.save(self._tasks)
        self._notify_observers()
        
        return task
    
    def update_task(self, quadrant: int, task_id: int, 
                    description: Optional[str] = None,
                    notes: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    metadata: Optional[Dict[str, str]] = None) -> bool:
        """
        Update task details
        
        Single Responsibility: Task update coordination
        
        Returns:
            True if task was found and updated, False otherwise
        """
        if not QuadrantInfo.validate_quadrant(quadrant):
            raise ValueError(f"Invalid quadrant: {quadrant}")
        
        for task in self._tasks[quadrant]:
            if task.id == task_id:
                task.update_details(description, notes, tags, metadata)
                self._repository.save(self._tasks)
                self._notify_observers()
                return True
        
        return False
    
    def complete_task(self, quadrant: int, task_id: int) -> bool:
        """
        Mark task as completed
        
        Returns:
            True if task was found and completed, False otherwise
        """
        if not QuadrantInfo.validate_quadrant(quadrant):
            raise ValueError(f"Invalid quadrant: {quadrant}")
        
        for task in self._tasks[quadrant]:
            if task.id == task_id:
                task.mark_completed()
                self._repository.save(self._tasks)
                self._notify_observers()
                return True
        
        return False
    
    def remove_task(self, quadrant: int, task_id: int) -> bool:
        """
        Remove a task from quadrant
        
        Returns:
            True if task was found and removed, False otherwise
        """
        if not QuadrantInfo.validate_quadrant(quadrant):
            raise ValueError(f"Invalid quadrant: {quadrant}")
        
        initial_length = len(self._tasks[quadrant])
        self._tasks[quadrant] = [
            task for task in self._tasks[quadrant] if task.id != task_id
        ]
        
        if len(self._tasks[quadrant]) < initial_length:
            self._repository.save(self._tasks)
            self._notify_observers()
            return True
        
        return False
    
    def move_task(self, from_quadrant: int, task_id: int, to_quadrant: int) -> bool:
        """
        Move task from one quadrant to another
        
        Args:
            from_quadrant: Source quadrant (1-4)
            task_id: Task ID to move
            to_quadrant: Destination quadrant (1-4)
            
        Returns:
            True if task was moved, False if not found
        """
        if not QuadrantInfo.validate_quadrant(from_quadrant):
            raise ValueError(f"Invalid source quadrant: {from_quadrant}")
        if not QuadrantInfo.validate_quadrant(to_quadrant):
            raise ValueError(f"Invalid destination quadrant: {to_quadrant}")
        
        # Find and remove task from source
        task_to_move = None
        for task in self._tasks[from_quadrant]:
            if task.id == task_id:
                task_to_move = task
                break
        
        if not task_to_move:
            return False
        
        self._tasks[from_quadrant].remove(task_to_move)
        
        # Assign new ID in destination quadrant
        task_to_move.id = self._get_next_id(to_quadrant)
        self._tasks[to_quadrant].append(task_to_move)
        
        self._repository.save(self._tasks)
        self._notify_observers()
        
        return True
    
    def reorder_task(self, quadrant: int, task_id: int, direction: str) -> bool:
        """
        Reorder a task within its quadrant (move up or down)
        
        Args:
            quadrant: Quadrant number (1-4)
            task_id: Task ID to reorder
            direction: 'up' to move earlier in list, 'down' to move later
            
        Returns:
            True if task was reordered, False if not found or at boundary
        """
        if not QuadrantInfo.validate_quadrant(quadrant):
            raise ValueError(f"Invalid quadrant: {quadrant}")
        
        tasks = self._tasks[quadrant]
        
        # Find task index
        task_index = None
        for i, task in enumerate(tasks):
            if task.id == task_id:
                task_index = i
                break
        
        if task_index is None:
            return False
        
        # Check boundaries
        if direction == 'up' and task_index == 0:
            return False  # Already at top
        if direction == 'down' and task_index == len(tasks) - 1:
            return False  # Already at bottom
        
        # Swap positions
        if direction == 'up':
            tasks[task_index], tasks[task_index - 1] = tasks[task_index - 1], tasks[task_index]
        elif direction == 'down':
            tasks[task_index], tasks[task_index + 1] = tasks[task_index + 1], tasks[task_index]
        else:
            return False
        
        self._repository.save(self._tasks)
        self._notify_observers()
        return True
    
    def get_tasks(self, quadrant: int, include_completed: bool = True) -> List[Task]:
        """
        Get all tasks from a quadrant
        
        Args:
            quadrant: Quadrant number (1-4)
            include_completed: Whether to include completed tasks
            
        Returns:
            List of tasks in the quadrant
        """
        if not QuadrantInfo.validate_quadrant(quadrant):
            raise ValueError(f"Invalid quadrant: {quadrant}")
        
        tasks = self._tasks[quadrant]
        
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]
        
        return tasks
    
    def get_all_tasks(self) -> Dict[int, List[Task]]:
        """Get all tasks from all quadrants"""
        return self._tasks.copy()
    
    def export_to_file(self, filepath: str) -> bool:
        """
        Export all tasks to a file
        
        Returns:
            True if export succeeded, False otherwise
        """
        try:
            self._repository.export_to_file(filepath, self._tasks)
            return True
        except Exception:
            return False
    
    def import_from_file(self, filepath: str, merge: bool = False) -> bool:
        """
        Import tasks from a file
        
        Args:
            filepath: Path to import file
            merge: If True, merge with existing tasks; if False, replace all
            
        Returns:
            True if import succeeded, False otherwise
        """
        try:
            imported_tasks = self._repository.import_from_file(filepath)
            
            if merge:
                # Merge imported tasks with existing
                for quadrant, tasks in imported_tasks.items():
                    for task in tasks:
                        # Assign new ID to avoid conflicts
                        task.id = self._get_next_id(quadrant)
                        self._tasks[quadrant].append(task)
            else:
                # Replace all tasks
                self._tasks = imported_tasks
            
            self._repository.save(self._tasks)
            self._notify_observers()
            return True
        except Exception:
            return False
