# Changelog

All notable changes to the Eisenhower Matrix application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD workflows
- Automated Flatpak builds
- Flathub submission preparation

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

[Unreleased]: https://github.com/alex/eisenhower/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/alex/eisenhower/releases/tag/v1.0.0
