"""Project Management Dialog"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from typing import Callable, Optional
from eisenhower_matrix.domain import Project


class ProjectDialog(Adw.Window):
    """Dialog for creating/editing projects"""
    
    def __init__(self, parent, project: Optional[Project] = None, on_save: Callable = None):
        super().__init__()
        self.project = project
        self.on_save = on_save
        self.is_edit = project is not None
        
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(400, 250)
        
        title = "Edit Project" if self.is_edit else "New Project"
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
        save_btn = Gtk.Button(label="Save" if self.is_edit else "Create")
        save_btn.add_css_class('suggested-action')
        save_btn.connect('clicked', self._on_save_clicked)
        header.pack_end(save_btn)
        
        # Form
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        content.set_margin_start(24)
        content.set_margin_end(24)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        
        # Name
        name_group = Adw.PreferencesGroup()
        name_group.set_title("Project Name")
        
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("Enter project name...")
        if project:
            self.name_entry.set_text(project.name)
        name_group.add(self.name_entry)
        content.append(name_group)
        
        # Description
        desc_group = Adw.PreferencesGroup()
        desc_group.set_title("Description")
        desc_group.set_description("Optional project description")
        
        desc_frame = Gtk.Frame()
        desc_scroll = Gtk.ScrolledWindow()
        desc_scroll.set_min_content_height(80)
        desc_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.desc_text = Gtk.TextView()
        self.desc_text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.desc_text.set_margin_start(12)
        self.desc_text.set_margin_end(12)
        self.desc_text.set_margin_top(12)
        self.desc_text.set_margin_bottom(12)
        if project and project.description:
            self.desc_text.get_buffer().set_text(project.description)
        
        desc_scroll.set_child(self.desc_text)
        desc_frame.set_child(desc_scroll)
        desc_group.add(desc_frame)
        content.append(desc_group)
        
        toolbar_view.set_content(content)
        self.set_content(toolbar_view)
    
    def _on_save_clicked(self, button):
        """Handle save button click"""
        name = self.name_entry.get_text().strip()
        if not name:
            return
        
        buffer = self.desc_text.get_buffer()
        description = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        
        if self.on_save:
            self.on_save(name, description)
        
        self.close()


class ProjectSelectorDialog(Adw.Window):
    """Dialog for selecting and managing projects"""
    
    def __init__(self, parent, app):
        super().__init__()
        self.app = app
        
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(500, 400)
        self.set_title("Projects")
        
        # Main content
        toolbar_view = Adw.ToolbarView()
        
        # Header bar
        header = Adw.HeaderBar()
        
        # New project button
        new_btn = Gtk.Button(label="New Project")
        new_btn.add_css_class('suggested-action')
        new_btn.connect('clicked', self._on_new_project)
        header.pack_start(new_btn)
        
        toolbar_view.add_top_bar(header)
        
        # Projects list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        self.list_box = Gtk.ListBox()
        self.list_box.add_css_class('boxed-list')
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.set_child(self.list_box)
        
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content_box.set_margin_start(12)
        content_box.set_margin_end(12)
        content_box.set_margin_top(12)
        content_box.set_margin_bottom(12)
        content_box.append(scrolled)
        
        toolbar_view.set_content(content_box)
        self.set_content(toolbar_view)
        
        # Load projects
        self._refresh_projects()
    
    def _refresh_projects(self):
        """Refresh the projects list"""
        # Clear existing
        child = self.list_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.list_box.remove(child)
            child = next_child
        
        # Add projects
        projects = self.app.project_service.get_all_projects()
        for project in projects:
            row = self._create_project_row(project)
            self.list_box.append(row)
    
    def _create_project_row(self, project: Project):
        """Create a row for a project"""
        row = Adw.ActionRow()
        row.set_title(project.name)
        
        if project.description:
            row.set_subtitle(project.description)
        
        # Current project indicator
        if self.app.current_project and project.id == self.app.current_project.id:
            check_icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
            row.add_prefix(check_icon)
        
        # Switch button
        switch_btn = Gtk.Button(label="Open")
        switch_btn.set_valign(Gtk.Align.CENTER)
        switch_btn.connect('clicked', lambda b: self._on_switch_project(project.id))
        row.add_suffix(switch_btn)
        
        # Edit button
        edit_btn = Gtk.Button(icon_name="document-edit-symbolic")
        edit_btn.set_valign(Gtk.Align.CENTER)
        edit_btn.connect('clicked', lambda b: self._on_edit_project(project))
        row.add_suffix(edit_btn)
        
        # Delete button (only if not the last project)
        projects = self.app.project_service.get_all_projects()
        if len(projects) > 1:
            delete_btn = Gtk.Button(icon_name="user-trash-symbolic")
            delete_btn.set_valign(Gtk.Align.CENTER)
            delete_btn.add_css_class('destructive-action')
            delete_btn.connect('clicked', lambda b: self._on_delete_project(project))
            row.add_suffix(delete_btn)
        
        return row
    
    def _on_new_project(self, button):
        """Handle new project button"""
        def on_save(name, description):
            self.app.project_service.create_project(name, description)
            self._refresh_projects()
        
        dialog = ProjectDialog(self, on_save=on_save)
        dialog.present()
    
    def _on_edit_project(self, project: Project):
        """Handle edit project button"""
        def on_save(name, description):
            self.app.project_service.update_project(project.id, name, description)
            self._refresh_projects()
            # Update title if editing current project
            if self.app.current_project and project.id == self.app.current_project.id:
                self.app.current_project.name = name
                self.app.current_project.description = description
                win = self.app.props.active_window
                if win:
                    win.update_window_title()
        
        dialog = ProjectDialog(self, project=project, on_save=on_save)
        dialog.present()
    
    def _on_delete_project(self, project: Project):
        """Handle delete project button"""
        # Show confirmation dialog
        dialog = Adw.MessageDialog.new(self)
        dialog.set_heading("Delete Project?")
        dialog.set_body(f"Are you sure you want to delete '{project.name}'? All tasks will be permanently deleted.")
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("delete", "Delete")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        
        dialog.connect("response", lambda d, r: self._on_delete_confirmed(d, r, project))
        dialog.present()
    
    def _on_delete_confirmed(self, dialog, response, project):
        """Handle delete confirmation"""
        if response == "delete":
            try:
                # If deleting current project, switch to another first
                if self.app.current_project and project.id == self.app.current_project.id:
                    projects = self.app.project_service.get_all_projects()
                    other_project = next((p for p in projects if p.id != project.id), None)
                    if other_project:
                        self.app.switch_project(other_project.id)
                
                self.app.project_service.delete_project(project.id)
                self._refresh_projects()
            except ValueError as e:
                # Show error if cannot delete
                error_dialog = Adw.MessageDialog.new(self)
                error_dialog.set_heading("Cannot Delete")
                error_dialog.set_body(str(e))
                error_dialog.add_response("ok", "OK")
                error_dialog.present()
    
    def _on_switch_project(self, project_id: str):
        """Handle switch project button"""
        self.app.switch_project(project_id)
        self.close()
