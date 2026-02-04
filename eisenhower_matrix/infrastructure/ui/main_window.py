"""Main Application Window"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GObject

from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService
from eisenhower_matrix.infrastructure.ui.observer_adapter import GtkObserverAdapter
from eisenhower_matrix.infrastructure.ui.quadrant_panel import QuadrantPanel
from eisenhower_matrix.infrastructure.ui.task_dialog import TaskDialog
from eisenhower_matrix.infrastructure.ui.project_dialog import ProjectSelectorDialog
from eisenhower_matrix.infrastructure.ui.user_guide_dialog import UserGuideDialog


class MainWindow(Adw.ApplicationWindow):
    """Main application window"""
    
    def __init__(self, app):
        super().__init__(application=app)
        self.app = app
        
        # Create observer adapter and attach to service
        self.observer_adapter = GtkObserverAdapter(self.on_matrix_changed)
        self.app.service.add_observer(self.observer_adapter)
        
        self.set_default_size(1200, 800)
        self.update_window_title()
        
        # State for showing completed tasks
        self.show_completed = False
        
        # State for showing archived tasks
        self.show_archived = False
        
        # State for search
        self.search_text = ""
        
        # Header bar
        header = Adw.HeaderBar()
        
        # Project selector button
        project_btn = Gtk.Button()
        project_btn.set_icon_name('folder-symbolic')
        project_btn.set_tooltip_text('Manage projects')
        project_btn.connect('clicked', self._on_projects_clicked)
        header.pack_start(project_btn)
        
        # Search toggle button
        search_toggle = Gtk.ToggleButton()
        search_toggle.set_icon_name('system-search-symbolic')
        search_toggle.set_tooltip_text('Search tasks')
        header.pack_start(search_toggle)
        self.search_toggle = search_toggle
        
        # Theme switcher button
        theme_button = Gtk.Button()
        theme_button.set_icon_name('weather-clear-night-symbolic')
        theme_button.set_tooltip_text('Toggle theme')
        theme_button.connect('clicked', self._on_theme_toggle)
        header.pack_start(theme_button)
        self.theme_button = theme_button
        
        # Show completed tasks toggle button
        completed_button = Gtk.ToggleButton()
        completed_button.set_icon_name('emblem-ok-symbolic')
        completed_button.set_tooltip_text('Show completed tasks')
        completed_button.set_active(self.show_completed)
        completed_button.connect('toggled', self._on_show_completed_toggled)
        header.pack_start(completed_button)
        self.completed_button = completed_button
        
        # Show archived tasks toggle button
        archived_button = Gtk.ToggleButton()
        archived_button.set_icon_name('package-x-generic-symbolic')
        archived_button.set_tooltip_text('Show archived tasks')
        archived_button.set_active(self.show_archived)
        archived_button.connect('toggled', self._on_show_archived_toggled)
        header.pack_start(archived_button)
        self.archived_button = archived_button
        
        # Menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name('open-menu-symbolic')
        
        menu = Gio.Menu()
        
        # Export submenu
        export_menu = Gio.Menu()
        export_menu.append("Export as JSON...", "app.export")
        export_menu.append("Export as CSV...", "app.export-csv")
        export_menu.append("Export as Markdown...", "app.export-markdown")
        export_menu.append("Export to Calendar CSV...", "app.export-calendar")
        menu.append_submenu("Export", export_menu)
        
        # Import submenu
        import_menu = Gio.Menu()
        import_menu.append("Import JSON (Replace)...", "app.import")
        import_menu.append("Import JSON (Merge)...", "app.import-merge")
        import_menu.append("Import CSV...", "app.import-csv")
        import_menu.append("Import Calendar (iCal)...", "app.import-calendar")
        menu.append_submenu("Import", import_menu)
        
        menu.append("User Guide", "app.user-guide")
        menu.append("Keyboard Shortcuts", "app.shortcuts")
        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")
        
        menu_button.set_menu_model(menu)
        header.pack_end(menu_button)
        
        # Main content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        main_box.append(header)
        
        # Search bar
        self.search_bar = Gtk.SearchBar()
        search_entry = Gtk.SearchEntry()
        search_entry.set_placeholder_text("Search tasks...")
        search_entry.set_hexpand(True)
        search_entry.connect('search-changed', self._on_search_changed)
        self.search_bar.set_child(search_entry)
        self.search_bar.connect_entry(search_entry)
        self.search_bar.set_key_capture_widget(self)
        
        # Connect search toggle to search bar
        search_toggle.bind_property('active', self.search_bar, 'search-mode-enabled',
                                    GObject.BindingFlags.BIDIRECTIONAL)
        
        main_box.append(self.search_bar)
        
        # Grid for quadrants
        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(1)
        grid.set_column_spacing(1)
        grid.set_vexpand(True)
        grid.set_hexpand(True)
        
        # Create quadrant panels
        self.panels = {}
        positions = {1: (0, 0), 2: (0, 1), 3: (1, 0), 4: (1, 1)}
        
        for q in range(1, 5):
            panel = QuadrantPanel(
                q, self.app.service,
                self.on_task_complete,
                self.on_task_delete,
                self.on_task_move,
                self.on_task_edit,
                self.on_task_reorder,
                self.on_task_archive
            )
            panel.set_show_completed(self.show_completed)
            self.panels[q] = panel
            row, col = positions[q]
            grid.attach(panel, col, row, 1, 1)
        
        main_box.append(grid)
        
        # Wrap in toast overlay for notifications
        toast_overlay = Adw.ToastOverlay()
        toast_overlay.set_child(main_box)
        
        self.set_content(toast_overlay)
        
        # Set up keyboard shortcuts
        self._setup_keyboard_shortcuts()
        
        # Load CSS
        self.load_css()
    
    def _setup_keyboard_shortcuts(self):
        """Set up window-level keyboard shortcuts"""
        # Theme toggle: Ctrl+T
        theme_action = Gio.SimpleAction.new("toggle-theme", None)
        theme_action.connect("activate", lambda *args: self._on_theme_toggle(None))
        self.add_action(theme_action)
        app = self.get_application()
        app.set_accels_for_action("win.toggle-theme", ["<Ctrl>T"])
        
        # Show/hide completed tasks: Ctrl+H
        completed_action = Gio.SimpleAction.new("toggle-completed", None)
        completed_action.connect("activate", lambda *args: self.completed_button.set_active(not self.completed_button.get_active()))
        self.add_action(completed_action)
        app.set_accels_for_action("win.toggle-completed", ["<Ctrl>H"])
        
        # Show/hide archived tasks: Ctrl+A
        archived_action = Gio.SimpleAction.new("toggle-archived", None)
        archived_action.connect("activate", lambda *args: self.archived_button.set_active(not self.archived_button.get_active()))
        self.add_action(archived_action)
        app.set_accels_for_action("win.toggle-archived", ["<Ctrl>A"])
        
        # Focus quadrants: Ctrl+1, Ctrl+2, Ctrl+3, Ctrl+4
        for q in range(1, 5):
            action = Gio.SimpleAction.new(f"focus-quadrant-{q}", None)
            action.connect("activate", lambda a, p, quadrant=q: self._focus_quadrant(quadrant))
            self.add_action(action)
            app.set_accels_for_action(f"win.focus-quadrant-{q}", [f"<Ctrl>{q}"])
    
    def _focus_quadrant(self, quadrant: int):
        """Focus on a specific quadrant"""
        if quadrant in self.panels:
            panel = self.panels[quadrant]
            panel.grab_focus()
    
    def _on_projects_clicked(self, button):
        """Handle projects button click"""
        dialog = ProjectSelectorDialog(self, self.get_application())
        dialog.present()
    
    def update_window_title(self):
        """Update window title with current project name"""
        app = self.get_application()
        if app and app.current_project:
            self.set_title(f"{app.current_project.name} - Eisenhower Matrix")
        else:
            self.set_title("Eisenhower Matrix")
    
    def _on_search_changed(self, search_entry):
        """Handle search text change"""
        self.search_text = search_entry.get_text().strip()
        self._refresh_all_panels()
    
    def _refresh_all_panels(self):
        """Refresh all quadrant panels"""
        for panel in self.panels.values():
            panel.set_search_text(self.search_text)
            panel.refresh()
    
    def load_css(self):
        """Load custom CSS with light/dark theme support"""
        css_provider = Gtk.CssProvider()
        css = """
        /* Quadrant panels */
        .quadrant-panel {
            background: @window_bg_color;
            border: 1px solid @borders;
        }
        
        /* Quadrant color indicators */
        .urgent-important {
            border-left: 4px solid @error_color;
        }
        
        .important-not-urgent {
            border-left: 4px solid @warning_color;
        }
        
        .urgent-not-important {
            border-left: 4px solid @accent_color;
        }
        
        .not-urgent-not-important {
            border-left: 4px solid @success_color;
        }
        
        /* Task row */
        .task-row {
            padding: 6px;
        }
        
        .task-row:hover {
            background: alpha(@accent_color, 0.1);
        }
        
        /* Completed task styling - strikethrough and muted color */
        .completed-task {
            text-decoration: line-through;
            color: alpha(@window_fg_color, 0.5);
        }
        
        /* Light theme specific */
        @media (prefers-color-scheme: light) {
            .completed-task {
                color: alpha(@window_fg_color, 0.45);
            }
        }
        
        /* Dark theme specific */
        @media (prefers-color-scheme: dark) {
            .completed-task {
                color: alpha(@window_fg_color, 0.55);
            }
        }
        
        /* Tag badges */
        .tag-badge {
            background: alpha(@accent_color, 0.2);
            border-radius: 12px;
            padding: 2px 8px;
            font-size: 0.85em;
        }
        
        @media (prefers-color-scheme: dark) {
            .tag-badge {
                background: alpha(@accent_color, 0.3);
            }
        }
        
        /* Due date indicators */
        .overdue-task {
            color: @error_color;
            font-weight: bold;
        }
        
        .due-soon-task {
            color: @warning_color;
            font-weight: 600;
        }
        
        /* Drag and drop styles */
        .task-row.dragging {
            opacity: 0.5;
        }
        
        .task-row.drop-target {
            background: alpha(@accent_color, 0.3);
            border: 2px solid @accent_color;
            border-radius: 6px;
        }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Update theme button icon based on current theme
        style_manager = Adw.StyleManager.get_default()
        self._update_theme_button_icon(style_manager.get_dark())
    
    def _on_theme_toggle(self, button):
        """Toggle between light and dark theme"""
        style_manager = Adw.StyleManager.get_default()
        
        # Toggle: default -> light -> dark -> default
        current_scheme = style_manager.get_color_scheme()
        
        if current_scheme == Adw.ColorScheme.DEFAULT:
            # Switch to light
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        elif current_scheme == Adw.ColorScheme.FORCE_LIGHT:
            # Switch to dark
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            # Switch back to default (system)
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        
        self._update_theme_button_icon(style_manager.get_dark())
    
    def _update_theme_button_icon(self, is_dark):
        """Update theme button icon based on current theme"""
        if is_dark:
            self.theme_button.set_icon_name('weather-clear-symbolic')
            self.theme_button.set_tooltip_text('Switch to light theme')
        else:
            self.theme_button.set_icon_name('weather-clear-night-symbolic')
            self.theme_button.set_tooltip_text('Switch to dark theme')
    
    def _on_show_completed_toggled(self, button):
        """Toggle showing completed tasks"""
        self.show_completed = button.get_active()
        
        # Update tooltip
        if self.show_completed:
            button.set_tooltip_text('Hide completed tasks')
        else:
            button.set_tooltip_text('Show completed tasks')
        
        # Refresh all panels
        for panel in self.panels.values():
            panel.set_show_completed(self.show_completed)
            panel.refresh()
    
    def _on_show_archived_toggled(self, button):
        """Toggle showing archived tasks"""
        self.show_archived = button.get_active()
        
        # When showing archived tasks, also show completed tasks (since archived tasks are completed)
        if self.show_archived and not self.show_completed:
            self.show_completed = True
            self.completed_button.set_active(True)
        
        # Update tooltip
        if self.show_archived:
            button.set_tooltip_text('Hide archived tasks')
        else:
            button.set_tooltip_text('Show archived tasks')
        
        # Refresh all panels
        for panel in self.panels.values():
            panel.set_show_archived(self.show_archived)
            panel.set_show_completed(self.show_completed)
            panel.refresh()
    
    def on_matrix_changed(self):
        """Handle matrix data changes"""
        for panel in self.panels.values():
            panel.refresh()
    
    def on_task_complete(self, quadrant: int, task_id: int, completed: bool):
        """Handle task completion toggle"""
        if completed:
            self.app.service.complete_task(quadrant, task_id)
        else:
            self.app.service.uncomplete_task(quadrant, task_id)
    
    def on_task_archive(self, quadrant: int, task_id: int, archived: bool):
        """Handle task archive toggle"""
        if archived:
            self.app.service.archive_task(quadrant, task_id)
        else:
            self.app.service.unarchive_task(quadrant, task_id)
    
    def on_task_delete(self, quadrant: int, task_id: int):
        """Handle task deletion"""
        self.app.service.remove_task(quadrant, task_id)
    
    def on_task_move(self, from_q: int, task_id: int, to_q: int):
        """Handle task move"""
        self.app.service.move_task(from_q, task_id, to_q)
    
    def on_task_edit(self, quadrant: int, task_id: int):
        """Handle task edit"""
        task = None
        for t in self.app.service.get_tasks(quadrant):
            if t.id == task_id:
                task = t
                break
        
        if not task:
            return
        
        def on_save(description, notes, tags, metadata, due_date):
            self.app.service.update_task(quadrant, task_id, description, notes, tags, metadata, due_date)
        
        dialog = TaskDialog(self, quadrant, task, on_save)
        dialog.present()    
    def on_task_reorder(self, quadrant: int, task_id: int, direction: str, target_task_id: int = None):
        """Handle task reordering"""
        if direction in ['up', 'down']:
            # Legacy up/down button support
            self.app.service.reorder_task(quadrant, task_id, direction)
        elif direction in ['before', 'after'] and target_task_id is not None:
            # Drag and drop support
            self.app.service.reorder_task_relative(quadrant, task_id, direction, target_task_id)
    
    def refresh_panels_for_project(self):
        """Refresh all panels to use the new service after project switch"""
        # Re-attach observer to new service
        self.app.service.add_observer(self.observer_adapter)
        
        # Update panels with new service
        for q, panel in self.panels.items():
            panel.service = self.app.service
            panel.refresh()