"""Task Row Widget"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio

from eisenhower_matrix.domain import Task, QuadrantInfo


class TaskRow(Gtk.Box):
    """
    Task Row Widget - UI Component
    
    Single Responsibility: Display a single task with actions
    """
    
    def __init__(self, task: Task, quadrant: int, on_complete, on_delete, on_move, on_edit, on_reorder):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.task = task
        self.quadrant = quadrant
        self.on_complete = on_complete
        self.on_delete = on_delete
        self.on_move = on_move
        self.on_edit = on_edit
        self.on_reorder = on_reorder
        
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(6)
        self.set_margin_bottom(6)
        
        # Main row
        main_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        
        # Checkbox for completion
        self.check = Gtk.CheckButton()
        self.check.set_active(task.completed)
        self.check.connect('toggled', self._on_check_toggled)
        main_row.append(self.check)
        
        # Task content (description + tags)
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        content_box.set_hexpand(True)
        
        # Task description
        self.label = Gtk.Label(label=task.description)
        self.label.set_xalign(0)
        self.label.set_wrap(True)
        self.label.set_wrap_mode(2)  # WORD_CHAR
        
        if task.completed:
            self.label.add_css_class('completed-task')
        
        content_box.append(self.label)
        
        # Completion timestamp
        if task.completed and task.completed_at:
            from datetime import datetime
            try:
                completed_dt = datetime.fromisoformat(task.completed_at)
                completed_text = f"✓ Completed: {completed_dt.strftime('%Y-%m-%d %H:%M')}"
                completed_label = Gtk.Label(label=completed_text)
                completed_label.set_xalign(0)
                completed_label.add_css_class('dim-label')
                completed_label.add_css_class('caption')
                content_box.append(completed_label)
            except (ValueError, AttributeError):
                pass
        
        # Tags display
        if task.tags:
            tags_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            for tag in task.tags:
                tag_label = Gtk.Label(label=tag)
                tag_label.add_css_class('tag-badge')
                tag_label.set_margin_top(2)
                tags_box.append(tag_label)
            content_box.append(tags_box)
        
        # Due date display with visual indicators
        if task.due_date and not task.completed:
            from datetime import datetime
            try:
                due_dt = datetime.fromisoformat(task.due_date)
                due_text = f"📅 Due: {due_dt.strftime('%Y-%m-%d')}"
                due_label = Gtk.Label(label=due_text)
                due_label.set_xalign(0)
                due_label.add_css_class('caption')
                
                # Add styling based on urgency
                if task.is_overdue():
                    due_label.add_css_class('overdue-task')
                elif task.is_due_soon(days=3):
                    due_label.add_css_class('due-soon-task')
                else:
                    due_label.add_css_class('dim-label')
                
                content_box.append(due_label)
            except (ValueError, AttributeError):
                pass
        
        # Notes indicator
        if task.notes:
            notes_label = Gtk.Label(label=f"📝 {task.notes[:50]}..." if len(task.notes) > 50 else f"📝 {task.notes}")
            notes_label.set_xalign(0)
            notes_label.add_css_class('dim-label')
            notes_label.add_css_class('caption')
            content_box.append(notes_label)
        
        main_row.append(content_box)
        
        # Action buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Reorder up button
        up_button = Gtk.Button()
        up_button.set_icon_name('go-up-symbolic')
        up_button.set_tooltip_text('Move task up')
        up_button.connect('clicked', self._on_reorder_up_clicked)
        button_box.append(up_button)
        
        # Reorder down button
        down_button = Gtk.Button()
        down_button.set_icon_name('go-down-symbolic')
        down_button.set_tooltip_text('Move task down')
        down_button.connect('clicked', self._on_reorder_down_clicked)
        button_box.append(down_button)
        
        # Edit button
        edit_button = Gtk.Button()
        edit_button.set_icon_name('document-edit-symbolic')
        edit_button.set_tooltip_text('Edit task')
        edit_button.connect('clicked', self._on_edit_clicked)
        button_box.append(edit_button)
        
        # Move button with menu
        move_button = Gtk.MenuButton()
        move_button.set_icon_name('go-jump-symbolic')
        move_button.set_tooltip_text('Move to another quadrant')
        
        # Disable move button for completed tasks
        if task.completed:
            move_button.set_sensitive(False)
            move_button.set_tooltip_text('Cannot move completed tasks')
        else:
            menu = Gio.Menu()
            for q in range(1, 5):
                if q != quadrant:
                    info = QuadrantInfo.get_info(q)
                    # Use parameterized action with format "from-taskid-to"
                    action_param = f"{quadrant}-{task.id}-{q}"
                    menu.append(
                        f"Q{q}: {info['short_name']}", 
                        f"app.move-task('{action_param}')"
                    )
            
            move_button.set_menu_model(menu)
        button_box.append(move_button)
        
        # Delete button
        delete_button = Gtk.Button()
        delete_button.set_icon_name('user-trash-symbolic')
        delete_button.set_tooltip_text('Delete task')
        delete_button.connect('clicked', self._on_delete_clicked)
        button_box.append(delete_button)
        
        main_row.append(button_box)
        
        self.append(main_row)
        
        # Add CSS class
        self.add_css_class('task-row')
    
    def _on_check_toggled(self, check):
        """Handle checkbox toggle"""
        self.on_complete(self.quadrant, self.task.id, check.get_active())
    
    def _on_edit_clicked(self, button):
        """Handle edit button click"""
        self.on_edit(self.quadrant, self.task.id)
    
    def _on_delete_clicked(self, button):
        """Handle delete button click"""
        self.on_delete(self.quadrant, self.task.id)
    
    def _on_reorder_up_clicked(self, button):
        """Handle reorder up button click"""
        self.on_reorder(self.quadrant, self.task.id, 'up')
    
    def _on_reorder_down_clicked(self, button):
        """Handle reorder down button click"""
        self.on_reorder(self.quadrant, self.task.id, 'down')
