"""Application Service - Project Management"""

from typing import List, Optional
import uuid
from eisenhower_matrix.domain import Project, IProjectRepository


class ProjectManagementService:
    """
    Application Service - Manages projects
    
    Single Responsibility: Coordinate project operations
    Dependency Inversion: Depends on IProjectRepository abstraction
    """
    
    def __init__(self, repository: IProjectRepository):
        """
        Initialize with repository dependency (Dependency Injection)
        
        Args:
            repository: Implementation of IProjectRepository port
        """
        self._repository = repository
    
    def create_project(self, name: str, description: str = "") -> Project:
        """
        Create a new project
        
        Args:
            name: Project name
            description: Optional project description
        
        Returns:
            Created Project entity
        
        Raises:
            ValueError: If name is empty
        """
        project_id = str(uuid.uuid4())
        project = Project.create(project_id, name, description)
        self._repository.save(project)
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """
        Get a specific project
        
        Args:
            project_id: Project identifier
        
        Returns:
            Project if found, None otherwise
        """
        return self._repository.load(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """
        Get all projects
        
        Returns:
            List of all projects, sorted by last accessed
        """
        return self._repository.load_all()
    
    def update_project(self, project_id: str, name: Optional[str] = None, 
                      description: Optional[str] = None) -> bool:
        """
        Update project details
        
        Args:
            project_id: Project identifier
            name: New project name
            description: New project description
        
        Returns:
            True if project was updated, False if not found
        
        Raises:
            ValueError: If name is empty
        """
        project = self._repository.load(project_id)
        if project:
            project.update_details(name, description)
            self._repository.save(project)
            return True
        return False
    
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project
        
        Args:
            project_id: Project identifier
        
        Returns:
            True if project was deleted, False if not found
        """
        # Don't allow deleting the last project
        projects = self._repository.load_all()
        if len(projects) <= 1:
            raise ValueError("Cannot delete the last project")
        
        return self._repository.delete(project_id)
    
    def mark_project_accessed(self, project_id: str) -> None:
        """
        Update the last accessed timestamp for a project
        
        Args:
            project_id: Project identifier
        """
        project = self._repository.load(project_id)
        if project:
            project.mark_accessed()
            self._repository.save(project)
    
    def project_exists(self, project_id: str) -> bool:
        """
        Check if a project exists
        
        Args:
            project_id: Project identifier
        
        Returns:
            True if project exists, False otherwise
        """
        return self._repository.exists(project_id)
