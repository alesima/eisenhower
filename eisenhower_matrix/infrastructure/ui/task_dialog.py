"""Task Dialog Widget"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from typing import Optional
from eisenhower_matrix.domain import Task


class TaskDialog(Adw.Window):
    """
    Task Dialog Widget - UI Component
    
    Single Responsibility: Display and capture task information
    Open/Closed: Can be extended without modifying core logic
    """
    
    def __init__(self, parent, quadrant: int, task: Optional[Task] = None, on_save=None):
        super().__init__()
        self.quadrant = quadrant
        self.task = task
        self.on_save = on_save
        self.is_edit = task is not None
        
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(500, 600)
        
        title = "Edit Task" if self.is_edit else f"Add Task to Q{quadrant}"
        self.set_title(title)
        
        # Main content
        toolbar_view = Adw.ToolbarView()
        
        # Header bar
        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)
        
        # Cancel button
        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect('clicked', lambda b: self.close())
        header.pack_start(cancel_btn)
        
        # Save button
        self.save_btn = Gtk.Button(label="Save" if self.is_edit else "Add")
        self.save_btn.add_css_class('suggested-action')
        self.save_btn.connect('clicked', self._on_save_clicked)
        header.pack_end(self.save_btn)
        
        # Content
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        # Scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        # Form
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        form_box.set_margin_start(24)
        form_box.set_margin_end(24)
        form_box.set_margin_top(24)
        form_box.set_margin_bottom(24)
        
        # Description
        desc_group = Adw.PreferencesGroup()
        desc_group.set_title("Description")
        desc_group.set_description("Brief task description")
        
        self.desc_entry = Gtk.Entry()
        self.desc_entry.set_placeholder_text("Enter task description...")
        if task:
            self.desc_entry.set_text(task.description)
        desc_group.add(self.desc_entry)
        form_box.append(desc_group)
        
        # Notes
        notes_group = Adw.PreferencesGroup()
        notes_group.set_title("Notes")
        notes_group.set_description("Detailed notes or context")
        
        notes_frame = Gtk.Frame()
        notes_scroll = Gtk.ScrolledWindow()
        notes_scroll.set_min_content_height(120)
        notes_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.notes_text = Gtk.TextView()
        self.notes_text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.notes_text.set_margin_start(12)
        self.notes_text.set_margin_end(12)
        self.notes_text.set_margin_top(12)
        self.notes_text.set_margin_bottom(12)
        if task and task.notes:
            self.notes_text.get_buffer().set_text(task.notes)
        
        notes_scroll.set_child(self.notes_text)
        notes_frame.set_child(notes_scroll)
        notes_group.add(notes_frame)
        form_box.append(notes_group)
        
        # Tags
        tags_group = Adw.PreferencesGroup()
        tags_group.set_title("Tags")
        tags_group.set_description("Comma-separated tags (e.g., work, urgent, client)")
        
        self.tags_entry = Gtk.Entry()
        self.tags_entry.set_placeholder_text("work, urgent, meeting...")
        if task and task.tags:
            self.tags_entry.set_text(", ".join(task.tags))
        tags_group.add(self.tags_entry)
        form_box.append(tags_group)
        
        # Metadata section
        metadata_group = Adw.PreferencesGroup()
        metadata_group.set_title("Metadata")
        metadata_group.set_description("Additional key-value information")
        
        # Metadata entries container
        self.metadata_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Load existing metadata
        if task and task.metadata:
            for key, value in task.metadata.items():
                self._add_metadata_row(key, value)
        
        metadata_group.add(self.metadata_box)
        
        # Add metadata button
        add_meta_btn = Gtk.Button(label="Add Metadata")
        add_meta_btn.set_margin_top(8)
        add_meta_btn.connect('clicked', lambda b: self._add_metadata_row())
        metadata_group.add(add_meta_btn)
        
        form_box.append(metadata_group)
        
        scrolled.set_child(form_box)
        content_box.append(scrolled)
        
        toolbar_view.set_content(content_box)
        self.set_content(toolbar_view)
    
    def _add_metadata_row(self, key: str = "", value: str = ""):
        """Add a metadata key-value row"""
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        
        key_entry = Gtk.Entry()
        key_entry.set_placeholder_text("Key")
        key_entry.set_text(key)
        key_entry.set_hexpand(True)
        row.append(key_entry)
        
        value_entry = Gtk.Entry()
        value_entry.set_placeholder_text("Value")
        value_entry.set_text(value)
        value_entry.set_hexpand(True)
        row.append(value_entry)
        
        remove_btn = Gtk.Button(icon_name="user-trash-symbolic")
        remove_btn.add_css_class('destructive-action')
        remove_btn.connect('clicked', lambda b: self.metadata_box.remove(row))
        row.append(remove_btn)
        
        self.metadata_box.append(row)
    
    def _get_metadata(self) -> dict:
        """Extract metadata from the form"""
        metadata = {}
        child = self.metadata_box.get_first_child()
        while child:
            if isinstance(child, Gtk.Box):
                key_entry = child.get_first_child()
                value_entry = key_entry.get_next_sibling()
                
                if key_entry and value_entry:
                    key = key_entry.get_text().strip()
                    value = value_entry.get_text().strip()
                    if key:  # Only add if key is not empty
                        metadata[key] = value
            
            child = child.get_next_sibling()
        
        return metadata
    
    def _on_save_clicked(self, button):
        """Handle save button click"""
        description = self.desc_entry.get_text().strip()
        if not description:
            # Show error
            return
        
        # Get notes
        buffer = self.notes_text.get_buffer()
        notes = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        
        # Get tags
        tags_text = self.tags_entry.get_text().strip()
        tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        
        # Get metadata
        metadata = self._get_metadata()
        
        if self.on_save:
            self.on_save(description, notes, tags, metadata)
        
        self.close()
