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
    due_date: Optional[str] = None  # ISO format date string
    
    @classmethod
    def create(cls, task_id: int, description: str, notes: str = "", 
               tags: List[str] = None, metadata: Dict[str, str] = None,
               due_date: Optional[str] = None) -> 'Task':
        """
        Factory method to create a new task with proper defaults
        
        Single Responsibility: Task creation logic
        
        Args:
            task_id: Unique task identifier
            description: Task description
            notes: Optional task notes
            tags: Optional list of tags
            metadata: Optional metadata dictionary
            due_date: Optional due date in ISO format (YYYY-MM-DD)
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
            metadata=metadata or {},
            due_date=due_date
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
                      metadata: Optional[Dict[str, str]] = None,
                      due_date: Optional[str] = None) -> None:
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
        
        if due_date is not None:
            self.due_date = due_date
    
    def is_overdue(self, current_date: Optional[datetime] = None) -> bool:
        """
        Domain behavior: Check if task is overdue
        
        Single Responsibility: Business rule for deadline
        """
        if not self.due_date or self.completed:
            return False
        
        try:
            due = datetime.fromisoformat(self.due_date)
            compare_date = current_date or datetime.now()
            return compare_date.date() > due.date()
        except (ValueError, TypeError):
            return False
    
    def is_due_soon(self, days: int = 3, current_date: Optional[datetime] = None) -> bool:
        """
        Domain behavior: Check if task is due within specified days
        
        Args:
            days: Number of days to check ahead (default 3)
            current_date: Optional date to compare against
        
        Returns:
            True if task is due within specified days and not completed
        """
        if not self.due_date or self.completed:
            return False
        
        try:
            due = datetime.fromisoformat(self.due_date)
            compare_date = current_date or datetime.now()
            days_until_due = (due.date() - compare_date.date()).days
            return 0 <= days_until_due <= days
        except (ValueError, TypeError):
            return False
    
    def matches_search(self, search_text: str) -> bool:
        """
        Domain behavior: Check if task matches search text
        
        Searches in description, notes, and tags (case-insensitive)
        
        Args:
            search_text: Text to search for
        
        Returns:
            True if task matches search criteria
        """
        if not search_text:
            return True
        
        search_lower = search_text.lower()
        
        # Search in description
        if search_lower in self.description.lower():
            return True
        
        # Search in notes
        if search_lower in self.notes.lower():
            return True
        
        # Search in tags
        for tag in self.tags:
            if search_lower in tag.lower():
                return True
        
        return False
