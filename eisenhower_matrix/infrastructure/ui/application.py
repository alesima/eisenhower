"""GTK Application"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio
from pathlib import Path

from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService
from eisenhower_matrix.infrastructure.persistence import JsonTaskRepository
from eisenhower_matrix.infrastructure.ui.main_window import MainWindow
from eisenhower_matrix.application import TaskExportUseCase, TaskImportUseCase


class EisenhowerApp(Adw.Application):
    """
    Main GTK Application - UI Adapter
    
    Single Responsibility: Application lifecycle management
    Dependency Injection: Creates and wires dependencies
    """
    
    def __init__(self):
        super().__init__(
            application_id='com.github.alesima.eisenhower',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        # Dependency Injection: Create infrastructure and domain service
        repository = JsonTaskRepository()
        self.service = EisenhowerMatrixService(repository)
        self.export_use_case = TaskExportUseCase(self.service)
        self.import_use_case = TaskImportUseCase(self.service)
    
    def do_activate(self):
        """Activate the application"""
        win = self.props.active_window
        if not win:
            win = MainWindow(self, self.service)
        win.present()
    
    def do_startup(self):
        """Application startup"""
        Adw.Application.do_startup(self)
        
        # Create actions
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.add_action(about_action)
        
        export_action = Gio.SimpleAction.new("export", None)
        export_action.connect("activate", self.on_export)
        self.add_action(export_action)
        
        export_csv_action = Gio.SimpleAction.new("export-csv", None)
        export_csv_action.connect("activate", self.on_export_csv)
        self.add_action(export_csv_action)
        
        export_calendar_action = Gio.SimpleAction.new("export-calendar", None)
        export_calendar_action.connect("activate", self.on_export_calendar)
        self.add_action(export_calendar_action)
        
        export_markdown_action = Gio.SimpleAction.new("export-markdown", None)
        export_markdown_action.connect("activate", self.on_export_markdown)
        self.add_action(export_markdown_action)
        
        import_action = Gio.SimpleAction.new("import", None)
        import_action.connect("activate", self.on_import)
        self.add_action(import_action)
        
        import_csv_action = Gio.SimpleAction.new("import-csv", None)
        import_csv_action.connect("activate", self.on_import_csv)
        self.add_action(import_csv_action)
        
        import_calendar_action = Gio.SimpleAction.new("import-calendar", None)
        import_calendar_action.connect("activate", self.on_import_calendar)
        self.add_action(import_calendar_action)
        
        import_merge_action = Gio.SimpleAction.new("import-merge", None)
        import_merge_action.connect("activate", self.on_import_merge)
        self.add_action(import_merge_action)
        
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *_: self.quit())
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q"])
        
        # Register parameterized move-task action
        # Parameter format: "from_quadrant-task_id-to_quadrant"
        move_task_action = Gio.SimpleAction.new_stateful(
            "move-task",
            GLib.VariantType.new("s"),
            GLib.Variant("s", "")
        )
        move_task_action.connect("activate", self.on_move_task_action)
        self.add_action(move_task_action)
    
    def on_move_task_action(self, action, parameter):
        """Handle parameterized move task action"""
        if not parameter:
            return
        
        # Parse parameter: "from_quadrant-task_id-to_quadrant"
        parts = parameter.get_string().split('-')
        if len(parts) != 3:
            return
        
        try:
            from_q, task_id, to_q = int(parts[0]), int(parts[1]), int(parts[2])
            win = self.props.active_window
            if win and hasattr(win, 'on_task_move'):
                win.on_task_move(from_q, task_id, to_q)
        except ValueError:
            pass  # Invalid parameter format
    
    def on_export(self, action, param):
        """Show export file dialog"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Export Tasks")
        dialog.set_initial_name("eisenhower-backup.json")
        
        # Set default filters
        json_filter = Gtk.FileFilter()
        json_filter.set_name("JSON Files")
        json_filter.add_pattern("*.json")
        
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All Files")
        all_filter.add_pattern("*")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(json_filter)
        filters.append(all_filter)
        dialog.set_filters(filters)
        dialog.set_default_filter(json_filter)
        
        dialog.save(self.props.active_window, None, self._on_export_response)
    
    def _on_export_response(self, dialog, result):
        """Handle export file dialog response"""
        try:
            file = dialog.save_finish(result)
            if file:
                file_path = file.get_path()
                if self.service.export_to_file(file_path):
                    self._show_toast(f"Tasks exported to {file.get_basename()}")
                else:
                    self._show_error_dialog("Export Failed", "Could not export tasks to file")
        except Exception as e:
            if "dismissed" not in str(e).lower():
                self._show_error_dialog("Export Error", str(e))
    
    def on_export_csv(self, action, param):
        """Show CSV export file dialog"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Export Tasks to CSV")
        dialog.set_initial_name("eisenhower-tasks.csv")
        
        # Set default filters
        csv_filter = Gtk.FileFilter()
        csv_filter.set_name("CSV Files")
        csv_filter.add_pattern("*.csv")
        
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All Files")
        all_filter.add_pattern("*")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(csv_filter)
        filters.append(all_filter)
        dialog.set_filters(filters)
        dialog.set_default_filter(csv_filter)
        
        dialog.save(self.props.active_window, None, self._on_export_csv_response)
    
    def _on_export_csv_response(self, dialog, result):
        """Handle CSV export file dialog response"""
        try:
            file = dialog.save_finish(result)
            if file:
                file_path = file.get_path()
                if self.export_use_case.export_to_csv(file_path):
                    self._show_toast(f"Tasks exported to {file.get_basename()}")
                else:
                    self._show_error_dialog("Export Failed", "Could not export tasks to CSV file")
        except Exception as e:
            if "dismissed" not in str(e).lower():
                self._show_error_dialog("Export Error", str(e))
    
    def on_export_calendar(self, action, param):
        """Show calendar export file dialog"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Export Tasks to Calendar CSV")
        dialog.set_initial_name("eisenhower-calendar.csv")
        
        # Set default filters
        csv_filter = Gtk.FileFilter()
        csv_filter.set_name("CSV Files")
        csv_filter.add_pattern("*.csv")
        
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All Files")
        all_filter.add_pattern("*")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(csv_filter)
        filters.append(all_filter)
        dialog.set_filters(filters)
        dialog.set_default_filter(csv_filter)
        
        dialog.save(self.props.active_window, None, self._on_export_calendar_response)
    
    def _on_export_calendar_response(self, dialog, result):
        """Handle calendar export file dialog response"""
        try:
            file = dialog.save_finish(result)
            if file:
                file_path = file.get_path()
                if self.export_use_case.export_to_calendar_csv(file_path):
                    self._show_toast(f"Tasks exported to {file.get_basename()}")
                else:
                    self._show_error_dialog("Export Failed", "Could not export tasks to calendar CSV file")
        except Exception as e:
            if "dismissed" not in str(e).lower():
                self._show_error_dialog("Export Error", str(e))
    
    def on_export_markdown(self, action, param):
        """Show markdown export file dialog"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Export Tasks to Markdown")
        dialog.set_initial_name("eisenhower-tasks.md")
        
        # Set default filters
        md_filter = Gtk.FileFilter()
        md_filter.set_name("Markdown Files")
        md_filter.add_pattern("*.md")
        
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All Files")
        all_filter.add_pattern("*")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(md_filter)
        filters.append(all_filter)
        dialog.set_filters(filters)
        dialog.set_default_filter(md_filter)
        
        dialog.save(self.props.active_window, None, self._on_export_markdown_response)
    
    def _on_export_markdown_response(self, dialog, result):
        """Handle markdown export file dialog response"""
        try:
            file = dialog.save_finish(result)
            if file:
                file_path = file.get_path()
                if self.export_use_case.export_to_markdown(file_path):
                    self._show_toast(f"Tasks exported to {file.get_basename()}")
                else:
                    self._show_error_dialog("Export Failed", "Could not export tasks to markdown file")
        except Exception as e:
            if "dismissed" not in str(e).lower():
                self._show_error_dialog("Export Error", str(e))
    
    def on_import(self, action, param):
        """Show import file dialog"""
        self._show_import_dialog(merge=False)
    
    def on_import_merge(self, action, param):
        """Show import and merge file dialog"""
        self._show_import_dialog(merge=True)
    
    def on_import_csv(self, action, param):
        """Show CSV import file dialog"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Import Tasks from CSV")
        
        # Set default filters
        csv_filter = Gtk.FileFilter()
        csv_filter.set_name("CSV Files")
        csv_filter.add_pattern("*.csv")
        
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All Files")
        all_filter.add_pattern("*")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(csv_filter)
        filters.append(all_filter)
        dialog.set_filters(filters)
        dialog.set_default_filter(csv_filter)
        
        dialog.open(self.props.active_window, None, self._on_import_csv_response)
    
    def _on_import_csv_response(self, dialog, result):
        """Handle CSV import file dialog response"""
        try:
            file = dialog.open_finish(result)
            if file:
                file_path = file.get_path()
                if self.import_use_case.import_from_csv(file_path):
                    self._show_toast(f"Tasks imported from {file.get_basename()}")
                else:
                    self._show_error_dialog("Import Failed", "Could not import tasks from CSV file")
        except Exception as e:
            if "dismissed" not in str(e).lower():
                self._show_error_dialog("Import Error", str(e))
    
    def on_import_calendar(self, action, param):
        """Show calendar import file dialog"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Import Tasks from Calendar (iCal/ICS)")
        
        # Set default filters
        ics_filter = Gtk.FileFilter()
        ics_filter.set_name("Calendar Files")
        ics_filter.add_pattern("*.ics")
        ics_filter.add_pattern("*.ical")
        
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All Files")
        all_filter.add_pattern("*")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(ics_filter)
        filters.append(all_filter)
        dialog.set_filters(filters)
        dialog.set_default_filter(ics_filter)
        
        dialog.open(self.props.active_window, None, self._on_import_calendar_response)
    
    def _on_import_calendar_response(self, dialog, result):
        """Handle calendar import file dialog response"""
        try:
            file = dialog.open_finish(result)
            if file:
                file_path = file.get_path()
                if self.import_use_case.import_from_calendar(file_path):
                    self._show_toast(f"Tasks imported from {file.get_basename()}")
                else:
                    self._show_error_dialog("Import Failed", "Could not import tasks from calendar file")
        except Exception as e:
            if "dismissed" not in str(e).lower():
                self._show_error_dialog("Import Error", str(e))
    
    def _show_import_dialog(self, merge: bool):
        """Show import file dialog"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Import and Merge Tasks" if merge else "Import Tasks")
        
        # Set default filters
        json_filter = Gtk.FileFilter()
        json_filter.set_name("JSON Files")
        json_filter.add_pattern("*.json")
        
        all_filter = Gtk.FileFilter()
        all_filter.set_name("All Files")
        all_filter.add_pattern("*")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(json_filter)
        filters.append(all_filter)
        dialog.set_filters(filters)
        dialog.set_default_filter(json_filter)
        
        dialog.open(self.props.active_window, None, lambda d, r: self._on_import_response(d, r, merge))
    
    def _on_import_response(self, dialog, result, merge: bool):
        """Handle import file dialog response"""
        try:
            file = dialog.open_finish(result)
            if file:
                file_path = file.get_path()
                
                if not merge:
                    # Confirm replacement
                    alert = Adw.MessageDialog.new(self.props.active_window)
                    alert.set_heading("Replace All Tasks?")
                    alert.set_body("This will delete all current tasks and replace them with tasks from the import file.")
                    alert.add_response("cancel", "Cancel")
                    alert.add_response("replace", "Replace All")
                    alert.set_response_appearance("replace", Adw.ResponseAppearance.DESTRUCTIVE)
                    alert.set_default_response("cancel")
                    alert.set_close_response("cancel")
                    
                    def on_response(dialog, response):
                        if response == "replace":
                            self._do_import(file_path, merge)
                    
                    alert.connect("response", on_response)
                    alert.present()
                else:
                    # Merge directly
                    self._do_import(file_path, merge)
        except Exception as e:
            if "dismissed" not in str(e).lower():
                self._show_error_dialog("Import Error", str(e))
    
    def _do_import(self, file_path: str, merge: bool):
        """Perform the import operation"""
        if self.service.import_from_file(file_path, merge=merge):
            file_name = Path(file_path).name
            if merge:
                self._show_toast(f"Tasks merged from {file_name}")
            else:
                self._show_toast(f"Tasks imported from {file_name}")
        else:
            self._show_error_dialog("Import Failed", "Could not import tasks from file")
    
    def _show_toast(self, message: str):
        """Show a toast notification"""
        win = self.props.active_window
        if win and isinstance(win, Adw.ApplicationWindow):
            toast = Adw.Toast.new(message)
            toast.set_timeout(3)
            
            # Get or create toast overlay
            content = win.get_content()
            if not isinstance(content, Adw.ToastOverlay):
                overlay = Adw.ToastOverlay()
                overlay.set_child(content)
                win.set_content(overlay)
                content = overlay
            
            content.add_toast(toast)
    
    def _show_error_dialog(self, title: str, message: str):
        """Show an error dialog"""
        dialog = Adw.MessageDialog.new(self.props.active_window)
        dialog.set_heading(title)
        dialog.set_body(message)
        dialog.add_response("ok", "OK")
        dialog.set_default_response("ok")
        dialog.present()
    
    def on_about(self, action, param):
        """Show about dialog"""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Eisenhower Matrix",
            application_icon="com.github.alesima.eisenhower",
            developer_name="Alex Silva",
            version="1.0.0",
            developers=["Alex Silva"],
            copyright="© 2026 Alex Silva",
            license_type=Gtk.License.MIT_X11,
            website="https://github.com/alesima/eisenhower",
            issue_url="https://github.com/alesima/eisenhower/issues"
        )
        about.present()


def main():
    """Main entry point for GUI"""
    app = EisenhowerApp()
    return app.run(None)
