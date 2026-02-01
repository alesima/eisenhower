# Changelog

All notable changes to the Eisenhower Matrix application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.4] - 2026-01-31

### Added
- **In-app User Guide**: Comprehensive guide accessible from menu or F2 keyboard shortcut
- User guide covers:
  - Understanding the Eisenhower Matrix methodology
  - Detailed explanation of all four quadrants with examples
  - Getting started guide (5-step process)
  - Key app features and how to use them
  - Best practices for effective task management
  - Common mistakes to avoid
  - Success indicators and measuring productivity
- Expandable sections for easy navigation
- Modern libadwaita design with proper scrolling and readability

### Changed
- **Application icon redesigned**: Modern 3D appearance following Flatpak standards
  - Solid Nord color palette (no gradients)
  - 3D depth effects with highlights and shadows
  - Clear 2×2 grid representation of Eisenhower Matrix
  - Quadrant colors: Red, Orange, Blue, Green
  - Follows GNOME Human Interface Guidelines
- Menu reorganized: User Guide added before Keyboard Shortcuts
- Keyboard shortcuts: F2 opens User Guide, F1 opens About dialog

## [1.0.3] - 2026-01-31

### Added
- **Projects feature**: Create and manage multiple Eisenhower matrices
- Project management dialog for creating, editing, and deleting projects
- Project selector in header bar with folder icon
- Each project maintains separate task storage
- Automatic default project creation on first run
- Last accessed tracking for projects
- Window title shows current project name
- Safe deletion with confirmation dialog (cannot delete last project)
- Project metadata: name, description, creation date, last accessed

### Changed
- Task storage now project-specific (tasks_<project_id>.json)
- Application title includes current project name

## [1.0.2] - 2026-01-31

### Added
- **Task search and filtering**: Real-time search across all quadrants
- Search bar toggle button in header
- Search matches task descriptions, notes, and tags (case-insensitive)
- **Due dates with visual indicators**:
  - Calendar date picker with Today and Tomorrow shortcuts
  - Color-coded urgency: Red (overdue), Orange (due soon), Gray (future)
  - Due date display on task rows
  - Domain methods: `is_overdue()`, `is_due_soon(days=3)`
- Service methods for filtering: `search_tasks()`, `get_overdue_tasks()`, `get_due_soon_tasks()`

### Changed
- Task dialog now includes calendar date picker
- Export formats (CSV, Markdown, Calendar) include due_date field
- Import formats properly handle due_date field
- Calendar imports now use native due_date field

## [1.0.1] - 2026-01-31

### Added
- **Comprehensive keyboard shortcuts system**
- Keyboard shortcuts window (accessible via menu)
- Application shortcuts:
  - Ctrl+Q: Quit application
  - Ctrl+E: Export as JSON
  - Ctrl+Shift+E: Export as CSV
  - Ctrl+Alt+E: Export as Markdown
  - Ctrl+I: Import JSON
  - Ctrl+Shift+I: Import CSV
  - Ctrl+Alt+I: Import and merge JSON
  - F1: About dialog
- Window shortcuts:
  - Ctrl+T: Toggle light/dark theme
  - Ctrl+H: Toggle show/hide completed tasks
  - Ctrl+1/2/3/4: Focus on specific quadrant
- Menu item: "Keyboard Shortcuts" to view all shortcuts

### Changed
- Added keyboard accelerators for all major actions
- Improved accessibility with keyboard navigation

## [1.0.0] - 2026-01-31

### Added
- Initial release
- Eisenhower Matrix task organization (4 quadrants)
- GTK4/Adwaita modern user interface
- Task CRUD operations (Create, Read, Update, Delete)
- Task completion tracking with timestamps
- Task reordering within quadrants (up/down buttons)
- Rich task metadata: notes, tags, custom key-value pairs
- Import functionality:
  - JSON (replace or merge modes)
  - CSV with quadrant parsing
  - Calendar (iCal/ICS) with auto-quadrant assignment
- Export functionality:
  - JSON (complete data)
  - CSV (tabular format)
  - Markdown (human-readable)
  - Calendar CSV (for calendar applications)
- Light/Dark theme support with manual toggle
- Show/hide completed tasks toggle
- Completed task styling (strikethrough, muted colors)
- Business rule: Completed tasks cannot be moved
- Observer pattern for reactive UI updates
- Persistent JSON storage
- Flatpak packaging support
- Hexagonal architecture implementation
- SOLID principles throughout codebase
- Absolute imports (no relative imports)
- Comprehensive documentation (README, ARCHITECTURE, guides)

### Technical
- Python 3.9+ support
- GTK4 and libadwaita integration
- Three-layer architecture (Domain, Application, Infrastructure)
- Dependency injection pattern
- Interface segregation with ports and adapters
- Cross-platform support (Linux, macOS, Unix)

[Unreleased]: https://github.com/alesima/eisenhower/compare/v1.0.3...HEAD
[1.0.3]: https://github.com/alesima/eisenhower/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/alesima/eisenhower/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/alesima/eisenhower/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/alesima/eisenhower/releases/tag/v1.0.0
