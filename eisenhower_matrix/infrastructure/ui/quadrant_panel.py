"""Quadrant Panel Widget"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk

from eisenhower_matrix.domain import QuadrantInfo
from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService
from eisenhower_matrix.infrastructure.ui.task_dialog import TaskDialog
from eisenhower_matrix.infrastructure.ui.task_row import TaskRow


class QuadrantPanel(Gtk.Box):
    """
    Quadrant Panel Widget - UI Component
    
    Single Responsibility: Display tasks for one quadrant
    Depends on domain service abstraction
    """
    
    def __init__(self, quadrant: int, service: EisenhowerMatrixService, on_complete, on_delete, on_move, on_edit, on_reorder, on_archive):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.quadrant = quadrant
        self.service = service
        self.on_complete = on_complete
        self.on_delete = on_delete
        self.on_move = on_move
        self.on_edit = on_edit
        self.on_reorder = on_reorder
        self.on_archive = on_archive
        self.show_completed = False
        self.show_archived = False
        self.search_text = ""
        
        info = QuadrantInfo.get_info(quadrant)
        
        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        header.set_margin_start(12)
        header.set_margin_end(12)
        header.set_margin_top(12)
        header.set_margin_bottom(12)
        
        # Title
        title = Gtk.Label()
        title.set_markup(f"<b>Q{quadrant}: {info['name']}</b>")
        title.set_xalign(0)
        header.append(title)
        
        # Subtitle
        subtitle = Gtk.Label(label=info['short_name'])
        subtitle.set_xalign(0)
        subtitle.add_css_class('dim-label')
        subtitle.add_css_class('caption')
        header.append(subtitle)
        
        self.append(header)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(separator)
        
        # Scrolled window for tasks
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        # Task list
        self.task_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        scrolled.set_child(self.task_list)
        self.append(scrolled)
        
        # Add task button
        add_button = Gtk.Button(label="Add Task")
        add_button.set_margin_start(12)
        add_button.set_margin_end(12)
        add_button.set_margin_top(12)
        add_button.set_margin_bottom(12)
        add_button.connect('clicked', self._on_add_clicked)
        self.append(add_button)
        
        # Add CSS classes
        self.add_css_class('quadrant-panel')
        self.add_css_class(info['css_class'])
        
        # Load initial tasks
        self.refresh()
    
    def _on_add_clicked(self, button):
        """Handle add task button click"""
        def on_save(description, notes, tags, metadata, due_date):
            self.service.add_task(self.quadrant, description, notes, tags, metadata, due_date)
        
        dialog = TaskDialog(self.get_root(), self.quadrant, task=None, on_save=on_save)
        dialog.present()
    
    def set_show_completed(self, show: bool):
        """Set whether to show completed tasks"""
        self.show_completed = show
    
    def set_show_archived(self, show: bool):
        """Set whether to show archived tasks"""
        self.show_archived = show
    
    def set_search_text(self, text: str):
        """Set search filter text"""
        self.search_text = text
    
    def refresh(self):
        """Refresh the task list"""
        # Clear existing tasks
        child = self.task_list.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.task_list.remove(child)
            child = next_child
        
        # Add tasks
        all_tasks = self.service.get_tasks(self.quadrant)
        
        # Filter tasks based on show_completed setting
        if self.show_completed:
            tasks = all_tasks
        else:
            tasks = [t for t in all_tasks if not t.completed]
        
        # Filter tasks based on show_archived setting
        if self.show_archived:
            # When showing archived, only show archived tasks
            tasks = [t for t in tasks if t.archived]
        else:
            # When not showing archived, exclude archived tasks
            tasks = [t for t in tasks if not t.archived]
        
        # Apply search filter
        if self.search_text:
            tasks = [t for t in tasks if t.matches_search(self.search_text)]
        
        # Sort tasks: uncompleted tasks always above completed tasks
        tasks.sort(key=lambda t: (t.completed, t.id))
        
        if not tasks:
            empty_label = Gtk.Label(label="No tasks")
            empty_label.add_css_class('dim-label')
            empty_label.set_margin_top(24)
            empty_label.set_margin_bottom(24)
            self.task_list.append(empty_label)
        else:
            for task in tasks:
                task_row = TaskRow(task, self.quadrant, self.on_complete, self.on_delete, self.on_move, self.on_edit, self.on_reorder, self.on_archive)
                self.task_list.append(task_row)
                
                # Add separator
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                self.task_list.append(sep)
