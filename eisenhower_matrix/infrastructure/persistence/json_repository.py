"""
Infrastructure Layer - JSON Persistence Adapter

Adapter that implements the ITaskRepository port using JSON file storage.
This is a concrete implementation that the domain doesn't know about.
"""

import json
from pathlib import Path
from typing import Dict, List
from eisenhower_matrix.domain import ITaskRepository, Task


class JsonTaskRepository(ITaskRepository):
    """
    Concrete implementation of ITaskRepository using JSON storage
    
    Single Responsibility: Handle JSON persistence
    Dependency Inversion: Implements domain port, depends on abstraction
    """
    
    def __init__(self, data_file: str = None):
        """
        Initialize JSON repository
        
        Args:
            data_file: Path to JSON file. Defaults to standard location.
        """
        if data_file is None:
            data_dir = Path.home() / ".local" / "share" / "eisenhower"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.data_file = data_dir / "tasks.json"
        else:
            self.data_file = Path(data_file)
    
    def load(self) -> Dict[int, List[Task]]:
        """
        Load tasks from JSON file
        
        Returns:
            Dictionary mapping quadrant numbers to task lists
        """
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    return self._deserialize_tasks(data)
            except (json.JSONDecodeError, IOError, KeyError, TypeError) as e:
                print(f"Error loading tasks: {e}")
        
        # Return empty structure
        return {1: [], 2: [], 3: [], 4: []}
    
    def save(self, tasks: Dict[int, List[Task]]) -> None:
        """
        Save tasks to JSON file
        
        Args:
            tasks: Dictionary mapping quadrant numbers to task lists
        """
        try:
            data = self._serialize_tasks(tasks)
            
            # Ensure directory exists
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")
            raise
    
    def export_to_file(self, filepath: str, tasks: Dict[int, List[Task]]) -> None:
        """
        Export tasks to a specific file
        
        Args:
            filepath: Target file path
            tasks: Tasks to export
        """
        try:
            data = self._serialize_tasks(tasks)
            
            export_path = Path(filepath)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error exporting tasks: {e}")
            raise
    
    def import_from_file(self, filepath: str) -> Dict[int, List[Task]]:
        """
        Import tasks from a specific file
        
        Args:
            filepath: Source file path
            
        Returns:
            Dictionary of imported tasks
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return self._deserialize_tasks(data)
        except (json.JSONDecodeError, IOError, KeyError) as e:
            print(f"Error importing tasks: {e}")
            raise
    
    def _serialize_tasks(self, tasks: Dict[int, List[Task]]) -> dict:
        """
        Convert Task objects to JSON-serializable format
        
        Single Responsibility: Serialization logic
        """
        return {
            str(quadrant): [self._task_to_dict(task) for task in task_list]
            for quadrant, task_list in tasks.items()
        }
    
    def _deserialize_tasks(self, data: dict) -> Dict[int, List[Task]]:
        """
        Convert JSON data to Task objects
        
        Single Responsibility: Deserialization logic
        """
        tasks = {}
        for quadrant in range(1, 5):
            quadrant_key = str(quadrant)
            if quadrant_key in data:
                tasks[quadrant] = [
                    self._dict_to_task(task_data)
                    for task_data in data[quadrant_key]
                ]
            else:
                tasks[quadrant] = []
        return tasks
    
    def _task_to_dict(self, task: Task) -> dict:
        """Convert Task entity to dictionary"""
        return {
            'id': task.id,
            'description': task.description,
            'created': task.created,
            'completed': task.completed,
            'completed_at': task.completed_at,
            'notes': task.notes,
            'tags': task.tags,
            'metadata': task.metadata,
            'due_date': task.due_date
        }
    
    def _dict_to_task(self, data: dict) -> Task:
        """
        Convert dictionary to Task entity with backward compatibility
        
        Single Responsibility: Task reconstruction
        """
        # Handle backward compatibility
        if 'notes' not in data:
            data['notes'] = ""
        if 'tags' not in data:
            data['tags'] = []
        if 'metadata' not in data:
            data['metadata'] = {}
        if 'due_date' not in data:
            data['due_date'] = None
        
        return Task(
            id=data['id'],
            description=data['description'],
            created=data['created'],
            completed=data['completed'],
            completed_at=data.get('completed_at'),
            notes=data['notes'],
            tags=data['tags'],
            metadata=data['metadata'],
            due_date=data['due_date']
        )
