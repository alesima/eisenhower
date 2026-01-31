"""Task Import Use Case"""

import csv
from eisenhower_matrix.application import EisenhowerMatrixService


class TaskImportUseCase:
    """
    Handles importing tasks from external sources.
    
    Could validate data, merge with existing tasks,
    handle conflicts, etc.
    """
    
    def __init__(self, matrix_service: EisenhowerMatrixService):
        self._service = matrix_service
    
    def import_from_json(self, file_path: str) -> bool:
        """Import tasks from JSON file"""
        try:
            self._service.import_from_file(file_path)
            return True
        except Exception:
            return False
    
    def import_from_csv(self, file_path: str) -> bool:
        """Import tasks from CSV file"""
        try:
            from datetime import datetime
            
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Parse quadrant (convert 'q1' to 1, or use numeric)
                    quadrant_str = row.get('quadrant', 'q4')
                    if quadrant_str.startswith('q'):
                        quadrant = int(quadrant_str[1])
                    else:
                        quadrant = int(quadrant_str)
                    
                    # Parse due date and add to metadata
                    metadata = {}
                    if row.get('due_date'):
                        metadata['Deadline'] = row['due_date']
                    
                    # Parse priority and add to metadata
                    if row.get('priority'):
                        metadata['Priority'] = row['priority']
                    
                    # Parse existing metadata and merge
                    if row.get('metadata'):
                        try:
                            import ast
                            extra_metadata = ast.literal_eval(row['metadata'])
                            metadata.update(extra_metadata)
                        except (ValueError, SyntaxError):
                            pass
                    
                    # Parse tags
                    tags = [tag.strip() for tag in row.get('tags', '').split(',') if tag.strip()]
                    
                    # Add task using matrix service
                    task = self._service.add_task(
                        quadrant=quadrant,
                        description=row['description'],
                        notes=row.get('notes', ''),
                        tags=tags if tags else None,
                        metadata=metadata if metadata else None
                    )
                    
                    # Set completion status if needed
                    if row.get('completed', '').lower() == 'true':
                        task.mark_completed()
                        self._service._repository.save(self._service._tasks)
            
            return True
        except Exception:
            return False
        
    def import_from_calendar(self, file_path: str) -> bool:
        """Import tasks from iCal/ICS calendar file
        
        Parses .ics calendar files and converts events to tasks.
        Events are categorized into quadrants based on their due date:
        - Events within 3 days: Quadrant 1 (Urgent & Important)
        - Events within 2 weeks: Quadrant 2 (Important, Not Urgent)
        - Events beyond 2 weeks: Quadrant 3 (Urgent, Not Important)
        - Events without due dates: Quadrant 4 (Not Urgent, Not Important)
        """
        try:
            from datetime import datetime
            from eisenhower_matrix.domain import Task
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple iCal parser (for basic VEVENT parsing)
            events = []
            lines = content.split('\n')
            current_event = {}
            in_event = False
            
            for line in lines:
                line = line.strip()
                
                if line == 'BEGIN:VEVENT':
                    in_event = True
                    current_event = {}
                elif line == 'END:VEVENT':
                    if current_event:
                        events.append(current_event)
                    in_event = False
                    current_event = {}
                elif in_event and ':' in line:
                    key, value = line.split(':', 1)
                    # Handle properties with parameters (e.g., DTSTART;VALUE=DATE:20260201)
                    if ';' in key:
                        key = key.split(';')[0]
                    current_event[key] = value
            
            # Convert events to tasks
            now = datetime.now()
            for event in events:
                summary = event.get('SUMMARY', 'Untitled Event')
                description_text = event.get('DESCRIPTION', '')
                location = event.get('LOCATION', '')
                
                # Parse date
                due_date = None
                dtstart = event.get('DTSTART', '')
                if dtstart:
                    try:
                        # Handle different date formats
                        if 'T' in dtstart:
                            # Full datetime: 20260201T120000Z
                            due_date = datetime.strptime(dtstart.replace('Z', ''), '%Y%m%dT%H%M%S')
                        else:
                            # Date only: 20260201
                            due_date = datetime.strptime(dtstart, '%Y%m%d')
                    except (ValueError, TypeError):
                        pass
                
                # Determine quadrant based on due date
                quadrant = 4
                if due_date:
                    days_until = (due_date - now).days
                    if days_until <= 3:
                        quadrant = 1  # Urgent & Important
                    elif days_until <= 14:
                        quadrant = 2  # Important, Not Urgent
                    else:
                        quadrant = 3  # Not Urgent
                
                # Build notes
                notes_parts = []
                if description_text:
                    notes_parts.append(description_text)
                if location:
                    notes_parts.append(f"Location: {location}")
                notes = '\n'.join(notes_parts) if notes_parts else ''
                
                # Build metadata
                metadata = {'source': 'calendar', 'event_id': event.get('UID', '')}
                if due_date:
                    metadata['Deadline'] = due_date.isoformat()
                
                # Add task using matrix service
                self._service.add_task(
                    quadrant=quadrant,
                    description=summary,
                    notes=notes,
                    tags=['calendar-import'],
                    metadata=metadata
                )
            
            return True
        except Exception:
            return False
