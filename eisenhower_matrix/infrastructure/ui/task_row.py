"""Task Row Widget"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Gdk

from eisenhower_matrix.domain import Task, QuadrantInfo


class TaskRow(Gtk.Box):
    """
    Task Row Widget - UI Component
    
    Single Responsibility: Display a single task with actions
    """
    
    def __init__(self, task: Task, quadrant: int, on_complete, on_delete, on_move, on_edit, on_reorder, on_archive):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.task = task
        self.quadrant = quadrant
        self.on_complete = on_complete
        self.on_delete = on_delete
        self.on_move = on_move
        self.on_edit = on_edit
        self.on_reorder = on_reorder
        self.on_archive = on_archive
        
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
        
        # Archive button - only show for completed tasks
        if task.completed:
            archive_button = Gtk.Button()
            if task.archived:
                archive_button.set_icon_name('mail-unread-symbolic')
                archive_button.set_tooltip_text('Unarchive task')
            else:
                archive_button.set_icon_name('package-x-generic-symbolic')
                archive_button.set_tooltip_text('Archive task')
            archive_button.connect('clicked', self._on_archive_clicked)
            button_box.append(archive_button)
        
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
        
        # Set up drag and drop
        self._setup_drag_and_drop()
    
    def _setup_drag_and_drop(self):
        """Set up drag and drop functionality"""
        # Create drag source
        drag_source = Gtk.DragSource()
        drag_source.set_actions(Gdk.DragAction.MOVE)
        
        # Set drag data
        drag_data = f"{self.quadrant}:{self.task.id}"
        drag_source.connect('prepare', lambda source, x, y: self._on_drag_prepare(source, drag_data))
        drag_source.connect('drag-begin', self._on_drag_begin)
        drag_source.connect('drag-end', self._on_drag_end)
        
        # Add drag source to the main row
        main_row = self.get_first_child()
        main_row.add_controller(drag_source)
        
        # Create drop target
        drop_target = Gtk.DropTarget()
        drop_target.set_gtypes([str])
        drop_target.set_actions(Gdk.DragAction.MOVE)
        drop_target.connect('drop', self._on_drop)
        drop_target.connect('enter', self._on_drop_enter)
        drop_target.connect('leave', self._on_drop_leave)
        
        # Add drop target to the main row
        main_row.add_controller(drop_target)
    
    def _on_drag_prepare(self, source, drag_data):
        """Prepare drag data"""
        content = Gdk.ContentProvider.new_for_value(drag_data)
        return content
    
    def _on_drag_begin(self, source):
        """Handle drag begin"""
        # Create a snapshot for drag icon
        snapshot = Gtk.Snapshot()
        self.snapshot(snapshot, 0, 0)
        paintable = snapshot.to_paintable(None)
        source.set_icon(paintable, 0, 0)
        
        # Add dragging class for visual feedback
        self.add_css_class('dragging')
    
    def _on_drag_end(self, source, drag, delete_data):
        """Handle drag end"""
        self.remove_css_class('dragging')
    
    def _on_drop_enter(self, target, x, y):
        """Handle drop enter"""
        self.add_css_class('drop-target')
        return Gdk.DragAction.MOVE
    
    def _on_drop_leave(self, target):
        """Handle drop leave"""
        self.remove_css_class('drop-target')
    
    def _on_drop(self, target, value, x, y):
        """Handle drop"""
        self.remove_css_class('drop-target')
        
        if not value:
            return False
        
        try:
            from_quadrant, from_task_id = value.split(':')
            from_quadrant = int(from_quadrant)
            from_task_id = int(from_task_id)
            
            # If dropping on the same task, do nothing
            if from_quadrant == self.quadrant and from_task_id == self.task.id:
                return False
            
            # If same quadrant, reorder
            if from_quadrant == self.quadrant:
                # Determine if we should place before or after based on y position
                height = self.get_height()
                if y < height / 2:
                    # Drop before this task
                    self.on_reorder(from_quadrant, from_task_id, 'before', self.task.id)
                else:
                    # Drop after this task
                    self.on_reorder(from_quadrant, from_task_id, 'after', self.task.id)
            else:
                # Different quadrant - move task
                self.on_move(from_quadrant, from_task_id, self.quadrant)
            
            return True
        except (ValueError, AttributeError):
            return False
    
    def _on_check_toggled(self, check):
        """Handle checkbox toggle"""
        self.on_complete(self.quadrant, self.task.id, check.get_active())
    
    def _on_edit_clicked(self, button):
        """Handle edit button click"""
        self.on_edit(self.quadrant, self.task.id)
    
    def _on_delete_clicked(self, button):
        """Handle delete button click"""
        self.on_delete(self.quadrant, self.task.id)
    
    def _on_archive_clicked(self, button):
        """Handle archive button click"""
        self.on_archive(self.quadrant, self.task.id, not self.task.archived)
