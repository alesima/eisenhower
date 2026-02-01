"""Project Repository Port - Domain Interface"""

from abc import ABC, abstractmethod
from typing import List, Optional
from eisenhower_matrix.domain.project import Project


class IProjectRepository(ABC):
    """
    Port interface for project persistence
    
    Interface Segregation: Focused on project operations only
    Dependency Inversion: Domain depends on abstraction, not concrete implementation
    """
    
    @abstractmethod
    def save(self, project: Project) -> None:
        """
        Save or update a project
        
        Args:
            project: Project to save
        """
        pass
    
    @abstractmethod
    def load(self, project_id: str) -> Optional[Project]:
        """
        Load a specific project by ID
        
        Args:
            project_id: Project identifier
        
        Returns:
            Project if found, None otherwise
        """
        pass
    
    @abstractmethod
    def load_all(self) -> List[Project]:
        """
        Load all projects
        
        Returns:
            List of all projects
        """
        pass
    
    @abstractmethod
    def delete(self, project_id: str) -> bool:
        """
        Delete a project
        
        Args:
            project_id: Project identifier
        
        Returns:
            True if project was deleted, False if not found
        """
        pass
    
    @abstractmethod
    def exists(self, project_id: str) -> bool:
        """
        Check if a project exists
        
        Args:
            project_id: Project identifier
        
        Returns:
            True if project exists, False otherwise
        """
        pass
