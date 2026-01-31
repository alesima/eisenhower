"""Quadrant Info Value Object"""

from dataclasses import dataclass


@dataclass
class QuadrantInfo:
    """
    Value Object - Quadrant metadata
    
    Immutable information about each quadrant in the matrix.
    """
    number: int
    name: str
    short_name: str
    description: str
    color: str
    css_class: str
    
    # Static quadrant definitions (Value Objects)
    QUADRANTS = {
        1: {
            "name": "Urgent &amp; Important",
            "short_name": "Do First",
            "description": "Critical tasks that require immediate attention",
            "color": "red",
            "css_class": "urgent-important"
        },
        2: {
            "name": "Important, Not Urgent",
            "short_name": "Schedule",
            "description": "Long-term goals and strategic planning",
            "color": "yellow",
            "css_class": "important-not-urgent"
        },
        3: {
            "name": "Urgent, Not Important",
            "short_name": "Delegate",
            "description": "Tasks that need to be done but can be delegated",
            "color": "blue",
            "css_class": "urgent-not-important"
        },
        4: {
            "name": "Not Urgent, Not Important",
            "short_name": "Eliminate",
            "description": "Distractions and time-wasters to minimize",
            "color": "green",
            "css_class": "not-urgent-not-important"
        }
    }
    
    @classmethod
    def get_info(cls, quadrant: int) -> dict:
        """
        Get quadrant information
        
        Returns:
            Dictionary with quadrant metadata
        """
        if quadrant not in cls.QUADRANTS:
            raise ValueError(f"Invalid quadrant number: {quadrant}")
        
        return cls.QUADRANTS[quadrant]
    
    @classmethod
    def validate_quadrant(cls, quadrant: int) -> bool:
        """Validate quadrant number"""
        return quadrant in cls.QUADRANTS
    
    @classmethod
    def get_all_info(cls) -> dict:
        """Get information for all quadrants"""
        return cls.QUADRANTS.copy()
