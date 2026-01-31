"""Keyboard Shortcuts Dialog"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class ShortcutsWindow(Gtk.ShortcutsWindow):
    """Display keyboard shortcuts"""
    
    def __init__(self, parent):
        super().__init__()
        self.set_transient_for(parent)
        
        # Connect close-request signal to properly handle closing
        self.connect("close-request", self._on_close_request)
        
        section = Gtk.ShortcutsSection()
        section.props.visible = True
        section.props.section_name = "shortcuts"
        
        # Application shortcuts
        app_group = Gtk.ShortcutsGroup()
        app_group.props.title = "Application"
        app_group.props.visible = True
        
        shortcuts = [
            ("<Ctrl>Q", "Quit application"),
            ("F1", "About Eisenhower Matrix"),
            ("<Ctrl>T", "Toggle light/dark theme"),
            ("<Ctrl>H", "Show/hide completed tasks"),
        ]
        
        for accel, title in shortcuts:
            shortcut = Gtk.ShortcutsShortcut()
            shortcut.props.accelerator = accel
            shortcut.props.title = title
            shortcut.props.visible = True
            app_group.append(shortcut)
        
        section.append(app_group)
        
        # Import/Export shortcuts
        io_group = Gtk.ShortcutsGroup()
        io_group.props.title = "Import & Export"
        io_group.props.visible = True
        
        io_shortcuts = [
            ("<Ctrl>E", "Export as JSON"),
            ("<Ctrl><Shift>E", "Export as CSV"),
            ("<Ctrl><Alt>E", "Export as Markdown"),
            ("<Ctrl>I", "Import JSON (replace)"),
            ("<Ctrl><Shift>I", "Import CSV"),
            ("<Ctrl><Alt>I", "Import JSON (merge)"),
        ]
        
        for accel, title in io_shortcuts:
            shortcut = Gtk.ShortcutsShortcut()
            shortcut.props.accelerator = accel
            shortcut.props.title = title
            shortcut.props.visible = True
            io_group.append(shortcut)
        
        section.append(io_group)
        
        # Quadrant navigation shortcuts
        nav_group = Gtk.ShortcutsGroup()
        nav_group.props.title = "Navigation"
        nav_group.props.visible = True
        
        quadrants = [
            ("1", "Focus Quadrant 1 (Urgent & Important)"),
            ("2", "Focus Quadrant 2 (Important, Not Urgent)"),
            ("3", "Focus Quadrant 3 (Urgent, Not Important)"),
            ("4", "Focus Quadrant 4 (Not Urgent, Not Important)"),
        ]
        
        for num, title in quadrants:
            shortcut = Gtk.ShortcutsShortcut()
            shortcut.props.accelerator = f"<Ctrl>{num}"
            shortcut.props.title = title
            shortcut.props.visible = True
            nav_group.append(shortcut)
        
        section.append(nav_group)
        
        self.set_child(section)
    
    def _on_close_request(self, window):
        """Handle close request - destroy window but don't propagate to app"""
        self.destroy()
        return True  # Stop signal propagation
