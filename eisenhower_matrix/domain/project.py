"""Project Entity - Core Domain Model"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    """
    Project Entity - Core domain model
    
    Represents a project that contains an Eisenhower Matrix.
    Each project has its own set of tasks organized in four quadrants.
    """
    id: str
    name: str
    created: str
    description: str = ""
    last_accessed: Optional[str] = None
    
    @classmethod
    def create(cls, project_id: str, name: str, description: str = "") -> 'Project':
        """
        Factory method to create a new project with proper defaults
        
        Args:
            project_id: Unique project identifier
            name: Project name
            description: Optional project description
        
        Returns:
            New Project instance
        
        Raises:
            ValueError: If name is empty
        """
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")
        
        now = datetime.now().isoformat()
        return cls(
            id=project_id,
            name=name.strip(),
            description=description.strip(),
            created=now,
            last_accessed=now
        )
    
    def update_details(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Update project details
        
        Args:
            name: New project name
            description: New project description
        
        Raises:
            ValueError: If name is empty
        """
        if name is not None:
            if not name.strip():
                raise ValueError("Project name cannot be empty")
            self.name = name.strip()
        
        if description is not None:
            self.description = description.strip()
    
    def mark_accessed(self) -> None:
        """Update the last accessed timestamp"""
        self.last_accessed = datetime.now().isoformat()
