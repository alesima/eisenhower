"""Task Export Use Case"""

import csv
import calendar
from eisenhower_matrix.application.matrix_service import EisenhowerMatrixService


class TaskExportUseCase:
    """
    Handles exporting tasks to external formats.
    
    Could coordinate multiple services, apply transformations,
    or handle different export formats.
    """
    
    def __init__(self, matrix_service: EisenhowerMatrixService):
        self._service = matrix_service
    
    def export_to_json(self, file_path: str) -> bool:
        """Export all tasks to JSON file"""
        try:
            self._service.export_to_file(file_path)
            return True
        except Exception:
            return False
    
    def export_to_csv(self, file_path: str) -> bool:
        """Export all tasks to CSV file"""
        try:
            tasks = self._service.get_all_tasks()
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['quadrant', 'id', 'description', 'notes', 'tags', 
                             'completed', 'completed_at', 'created', 'metadata']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for quadrant, task_list in tasks.items():
                    for task in task_list:
                        writer.writerow({
                            'quadrant': quadrant,
                            'id': task.id,
                            'description': task.description,
                            'notes': task.notes or '',
                            'tags': ','.join(task.tags) if task.tags else '',
                            'completed': task.completed,
                            'completed_at': task.completed_at or '',
                            'created': task.created or '',
                            'metadata': str(task.metadata) if task.metadata else ''
                        })
            return True
        except Exception:
            return False
    
    def export_to_markdown(self, file_path: str) -> bool:
        """Export all tasks to Markdown file"""
        try:
            tasks = self._service.get_all_tasks()
            with open(file_path, 'w', encoding='utf-8') as mdfile:
                for quadrant, task_list in tasks.items():
                    mdfile.write(f"# Quadrant {quadrant}\n\n")
                    for task in task_list:
                        mdfile.write(f"## Task ID: {task.id}\n")
                        mdfile.write(f"- **Description:** {task.description}\n")
                        mdfile.write(f"- **Notes:** {task.notes or 'N/A'}\n")
                        mdfile.write(f"- **Tags:** {', '.join(task.tags) if task.tags else 'N/A'}\n")
                        mdfile.write(f"- **Completed:** {'Yes' if task.completed else 'No'}\n")
                        mdfile.write(f"- **Completed At:** {task.completed_at or 'N/A'}\n")
                        mdfile.write(f"- **Created At:** {task.created or 'N/A'}\n")
                        mdfile.write(f"- **Metadata:** {str(task.metadata) if task.metadata else 'N/A'}\n\n")
            return True
        except Exception:
            return False
    
    def export_to_calendar_csv(self, file_path: str) -> bool:
        """Export all tasks to calendar-compatible CSV file"""
        try:
            tasks = self._service.get_all_tasks()
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Subject', 'Start Date', 'Due Date', 'Description', 
                             'Location', 'Categories']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                quadrant_names = {
                    1: "Important & Urgent",
                    2: "Important & Not Urgent", 
                    3: "Not Important & Urgent",
                    4: "Not Important & Not Urgent"
                }
                
                for quadrant, task_list in tasks.items():
                    for task in task_list:
                        # Use created date as start date, completed_at as due date if completed
                        start_date = task.created.strftime('%Y-%m-%d') if task.created else ''
                        due_date = task.completed_at.strftime('%Y-%m-%d') if task.completed_at else ''
                        
                        writer.writerow({
                            'Subject': task.description,
                            'Start Date': start_date,
                            'Due Date': due_date,
                            'Description': task.notes or '',
                            'Location': '',
                            'Categories': f"{quadrant_names.get(quadrant, 'Unknown')},{','.join(task.tags) if task.tags else ''}"
                        })
            return True
        except Exception:
            return False
