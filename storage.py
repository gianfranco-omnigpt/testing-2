"""Data persistence layer for tasks."""

import json
import os
from typing import List, Dict


class JSONStorage:
    """JSON-based storage for tasks."""
    
    def __init__(self, filepath: str):
        """Initialize JSON storage.
        
        Args:
            filepath: Path to the JSON file
        """
        self.filepath = filepath
    
    def load(self) -> List[Dict]:
        """Load tasks from JSON file.
        
        Returns:
            List of task dictionaries
        """
        if not os.path.exists(self.filepath):
            return []
        
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or empty, return empty list
            return []
    
    def save(self, tasks: List[Dict]) -> None:
        """Save tasks to JSON file.
        
        Args:
            tasks: List of task dictionaries to save
        """
        with open(self.filepath, 'w') as f:
            json.dump(tasks, f, indent=2)
    
    def clear(self) -> None:
        """Clear all tasks from storage."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)