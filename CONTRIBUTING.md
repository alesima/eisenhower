# Contributing to Eisenhower Matrix

Thank you for considering contributing to the Eisenhower Matrix application! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, GTK version, Python version)

### Suggesting Features

1. **Check existing feature requests**
2. **Create an issue** with:
   - Clear description of the feature
   - Use case and benefits
   - Potential implementation approach
   - Mockups or examples if applicable

### Code Contributions

#### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/alex/eisenhower.git
cd eisenhower

# Install system dependencies
sudo apt install python3 python3-pip python3-gi gir1.2-gtk-4.0 gir1.2-adw-1  # Ubuntu/Debian
sudo dnf install python3 python3-pip python3-gobject gtk4 libadwaita          # Fedora
sudo pacman -S python python-pip python-gobject gtk4 libadwaita               # Arch

# Install in development mode
pip install -e ".[dev]"

# Run application
python -m eisenhower_matrix.infrastructure.ui.application
```

#### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following coding standards
4. **Test your changes**:
   ```bash
   # Run linting
   flake8 eisenhower_matrix/
   black --check eisenhower_matrix/
   
   # Run tests
   pytest -v
   
   # Test Flatpak build
   ./build-flatpak.sh
   ```
5. **Commit with clear messages**:
   ```bash
   git commit -m "feat: Add feature description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

#### Commit Message Convention

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

Examples:
```
feat: Add dark mode toggle button
fix: Correct CSV export encoding issue
docs: Update installation instructions
refactor: Extract task validation to domain layer
```

### Coding Standards

#### Architecture

The project follows **Hexagonal Architecture** with **SOLID principles**:

```
Domain Layer (Core)
  ↓ no dependencies
Application Layer (Use Cases)
  ↓ depends on domain abstractions
Infrastructure Layer (Adapters)
  ↓ depends on application/domain
```

**Rules**:
- Domain layer has **zero** infrastructure dependencies
- Use **absolute imports** only (no relative imports)
- Depend on **abstractions** (interfaces/ports), not concrete implementations
- Apply **dependency injection** pattern
- Each class has **single responsibility**

#### Python Style

- Follow **PEP 8** guidelines
- Use **type hints** for function signatures
- Write **docstrings** for classes and public methods
- Maximum line length: **120 characters**
- Use **black** for formatting
- Use **flake8** for linting

Example:
```python
from typing import List, Optional
from eisenhower_matrix.domain.task import Task

class TaskRepository:
    """Repository for task persistence operations."""
    
    def save(self, tasks: List[Task]) -> bool:
        """
        Save tasks to storage.
        
        Args:
            tasks: List of tasks to save
            
        Returns:
            True if successful, False otherwise
        """
        # Implementation
        pass
```

#### GTK/UI Guidelines

- Use **GTK4** and **libadwaita** widgets
- Follow **GNOME Human Interface Guidelines**
- Keep UI code in `infrastructure/ui/` layer
- Use **observers** for reactive updates
- Implement proper **error dialogs** for user feedback

#### Testing

- Write **unit tests** for domain logic
- Write **integration tests** for use cases
- Mock **external dependencies**
- Aim for **>80% coverage** on domain layer

Example:
```python
def test_add_task():
    # Arrange
    mock_repo = MockTaskRepository()
    service = EisenhowerMatrixService(mock_repo)
    
    # Act
    task = service.add_task(1, "Test task", "Notes")
    
    # Assert
    assert task.description == "Test task"
    assert mock_repo.save_called
```

### Documentation

When contributing:

- Update **README.md** for user-facing changes
- Update **ARCHITECTURE.md** for architectural changes
- Add entries to **CHANGELOG.md**
- Add **docstrings** to new functions/classes
- Update **type hints** if function signatures change

### Pull Request Process

1. **Ensure CI passes**:
   - Flatpak builds successfully
   - Tests pass
   - Linting passes

2. **Update documentation**:
   - README if user-facing change
   - ARCHITECTURE if structural change
   - CHANGELOG with your changes

3. **Write clear PR description**:
   - What does this PR do?
   - Why is this change needed?
   - Any breaking changes?
   - Screenshots for UI changes

4. **Respond to review feedback**:
   - Address comments promptly
   - Make requested changes
   - Ask questions if unclear

5. **Squash commits** if requested

### Areas for Contribution

#### Good First Issues

- Add keyboard shortcuts
- Improve error messages
- Add tooltips
- Fix typos in documentation
- Add tests

#### Feature Ideas

- Task search and filtering
- Task due dates and reminders
- Task dependencies
- Drag-and-drop between quadrants
- Task statistics and analytics
- Multiple task lists/projects
- Cloud sync
- Mobile companion app

#### Architecture Improvements

- Add SQLite repository adapter
- Add CLI adapter
- Add web API adapter
- Implement domain events
- Add comprehensive test suite
- Add performance monitoring

## Getting Help

- **Issues**: Ask questions in GitHub issues
- **Discussions**: Use GitHub discussions for general questions
- **Documentation**: Check README and ARCHITECTURE docs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
