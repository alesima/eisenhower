"""Task Entity - Core Domain Model"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class Task:
    """
    Task Entity - Core domain model
    
    Represents a single task in the Eisenhower Matrix.
    Contains only business logic, no infrastructure concerns.
    """
    id: int
    description: str
    created: str
    completed: bool = False
    completed_at: Optional[str] = None
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def create(cls, task_id: int, description: str, notes: str = "", 
               tags: List[str] = None, metadata: Dict[str, str] = None) -> 'Task':
        """
        Factory method to create a new task with proper defaults
        
        Single Responsibility: Task creation logic
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
        return cls(
            id=task_id,
            description=description.strip(),
            created=datetime.now().isoformat(),
            completed=False,
            notes=notes or "",
            tags=tags or [],
            metadata=metadata or {}
        )
    
    def mark_completed(self) -> None:
        """
        Domain behavior: Mark task as completed
        
        Single Responsibility: Completion logic
        """
        if not self.completed:
            self.completed = True
            self.completed_at = datetime.now().isoformat()
    
    def update_details(self, description: Optional[str] = None,
                      notes: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      metadata: Optional[Dict[str, str]] = None) -> None:
        """
        Domain behavior: Update task details
        
        Single Responsibility: Task modification logic
        """
        if description is not None:
            if not description.strip():
                raise ValueError("Task description cannot be empty")
            self.description = description.strip()
        
        if notes is not None:
            self.notes = notes
        
        if tags is not None:
            self.tags = tags
        
        if metadata is not None:
            self.metadata = metadata
    
    def is_overdue(self, current_date: Optional[datetime] = None) -> bool:
        """
        Domain behavior: Check if task is overdue based on metadata
        
        Single Responsibility: Business rule for deadline
        """
        if 'Deadline' not in self.metadata:
            return False
        
        try:
            deadline = datetime.fromisoformat(self.metadata['Deadline'])
            compare_date = current_date or datetime.now()
            return compare_date > deadline and not self.completed
        except (ValueError, KeyError):
            return False
