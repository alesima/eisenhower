"""
Infrastructure Layer - JSON Project Persistence Adapter

Adapter that implements the IProjectRepository port using JSON file storage.
"""

import json
from pathlib import Path
from typing import List, Optional
from eisenhower_matrix.domain import IProjectRepository, Project


class JsonProjectRepository(IProjectRepository):
    """
    Concrete implementation of IProjectRepository using JSON storage
    
    Single Responsibility: Handle JSON persistence for projects
    Dependency Inversion: Implements domain port
    """
    
    def __init__(self, data_file: str = None):
        """
        Initialize JSON project repository
        
        Args:
            data_file: Path to JSON file. Defaults to standard location.
        """
        if data_file is None:
            data_dir = Path.home() / ".local" / "share" / "eisenhower"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.data_file = data_dir / "projects.json"
        else:
            self.data_file = Path(data_file)
        
        # Ensure file exists with default project
        if not self.data_file.exists():
            self._initialize_default_project()
    
    def _initialize_default_project(self) -> None:
        """Create default project on first run"""
        default_project = Project.create("default", "My Tasks", "Default project")
        self.save(default_project)
    
    def save(self, project: Project) -> None:
        """
        Save or update a project
        
        Args:
            project: Project to save
        """
        projects = self._load_all_dict()
        projects[project.id] = self._project_to_dict(project)
        self._save_all_dict(projects)
    
    def load(self, project_id: str) -> Optional[Project]:
        """
        Load a specific project by ID
        
        Args:
            project_id: Project identifier
        
        Returns:
            Project if found, None otherwise
        """
        projects = self._load_all_dict()
        if project_id in projects:
            return self._dict_to_project(projects[project_id])
        return None
    
    def load_all(self) -> List[Project]:
        """
        Load all projects
        
        Returns:
            List of all projects, sorted by last accessed (most recent first)
        """
        projects = self._load_all_dict()
        project_list = [self._dict_to_project(data) for data in projects.values()]
        # Sort by last_accessed, most recent first
        project_list.sort(key=lambda p: p.last_accessed or p.created, reverse=True)
        return project_list
    
    def delete(self, project_id: str) -> bool:
        """
        Delete a project
        
        Args:
            project_id: Project identifier
        
        Returns:
            True if project was deleted, False if not found
        """
        projects = self._load_all_dict()
        if project_id in projects:
            del projects[project_id]
            self._save_all_dict(projects)
            
            # Also delete the project's tasks file
            self._delete_project_tasks(project_id)
            return True
        return False
    
    def exists(self, project_id: str) -> bool:
        """
        Check if a project exists
        
        Args:
            project_id: Project identifier
        
        Returns:
            True if project exists, False otherwise
        """
        projects = self._load_all_dict()
        return project_id in projects
    
    def _load_all_dict(self) -> dict:
        """Load all projects as dictionary"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading projects: {e}")
                return {}
        return {}
    
    def _save_all_dict(self, projects: dict) -> None:
        """Save all projects dictionary to file"""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(projects, f, indent=2)
        except IOError as e:
            print(f"Error saving projects: {e}")
            raise
    
    def _project_to_dict(self, project: Project) -> dict:
        """Convert Project entity to dictionary"""
        return {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'created': project.created,
            'last_accessed': project.last_accessed
        }
    
    def _dict_to_project(self, data: dict) -> Project:
        """Convert dictionary to Project entity"""
        return Project(
            id=data.get('id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            created=data.get('created', ''),
            last_accessed=data.get('last_accessed')
        )
    
    def _delete_project_tasks(self, project_id: str) -> None:
        """Delete the tasks file for a project"""
        data_dir = Path.home() / ".local" / "share" / "eisenhower"
        tasks_file = data_dir / f"tasks_{project_id}.json"
        if tasks_file.exists():
            try:
                tasks_file.unlink()
            except IOError as e:
                print(f"Error deleting project tasks: {e}")
