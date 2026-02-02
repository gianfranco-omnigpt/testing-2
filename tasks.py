"""Task management logic."""

from datetime import datetime
from typing import List, Dict, Optional


class TaskManager:
    """Manages task operations and business logic."""
    
    def __init__(self, storage):
        """Initialize TaskManager with a storage backend.
        
        Args:
            storage: Storage instance for persisting tasks
        """
        self.storage = storage
        self.tasks = self.storage.load()
    
    def _save(self):
        """Save tasks to storage."""
        self.storage.save(self.tasks)
    
    def _get_next_id(self) -> int:
        """Get the next available task ID.
        
        Returns:
            Next available integer ID
        """
        if not self.tasks:
            return 1
        return max(task['id'] for task in self.tasks) + 1
    
    def add_task(self, description: str, priority: str = 'medium') -> Dict:
        """Add a new task.
        
        Args:
            description: Task description
            priority: Task priority (low, medium, high)
            
        Returns:
            Created task dictionary
        """
        task = {
            'id': self._get_next_id(),
            'description': description,
            'completed': False,
            'priority': priority,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        self.tasks.append(task)
        self._save()
        return task
    
    def get_tasks(self, status: str = 'all', priority: Optional[str] = None) -> List[Dict]:
        """Get tasks filtered by status and priority.
        
        Args:
            status: Filter by status ('all', 'pending', 'completed')
            priority: Optional priority filter
            
        Returns:
            List of task dictionaries
        """
        filtered_tasks = self.tasks
        
        # Filter by status
        if status == 'pending':
            filtered_tasks = [t for t in filtered_tasks if not t['completed']]
        elif status == 'completed':
            filtered_tasks = [t for t in filtered_tasks if t['completed']]
        
        # Filter by priority
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t['priority'] == priority]
        
        return filtered_tasks
    
    def get_task_by_id(self, task_id: int) -> Dict:
        """Get a task by its ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task dictionary
            
        Raises:
            ValueError: If task not found
        """
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        raise ValueError(f"Task #{task_id} not found")
    
    def complete_task(self, task_id: int) -> Dict:
        """Mark a task as complete.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task dictionary
            
        Raises:
            ValueError: If task not found
        """
        task = self.get_task_by_id(task_id)
        task['completed'] = True
        task['completed_at'] = datetime.now().isoformat()
        self._save()
        return task
    
    def uncomplete_task(self, task_id: int) -> Dict:
        """Mark a task as incomplete.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task dictionary
            
        Raises:
            ValueError: If task not found
        """
        task = self.get_task_by_id(task_id)
        task['completed'] = False
        task['completed_at'] = None
        self._save()
        return task
    
    def delete_task(self, task_id: int) -> Dict:
        """Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Deleted task dictionary
            
        Raises:
            ValueError: If task not found
        """
        task = self.get_task_by_id(task_id)
        self.tasks.remove(task)
        self._save()
        return task
    
    def clear_completed(self) -> int:
        """Clear all completed tasks.
        
        Returns:
            Number of tasks cleared
        """
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t['completed']]
        self._save()
        return initial_count - len(self.tasks)
    
    def get_statistics(self) -> Dict:
        """Get task statistics.
        
        Returns:
            Dictionary containing task statistics
        """
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        by_priority = {
            'high': sum(1 for t in self.tasks if t['priority'] == 'high'),
            'medium': sum(1 for t in self.tasks if t['priority'] == 'medium'),
            'low': sum(1 for t in self.tasks if t['priority'] == 'low')
        }
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'by_priority': by_priority
        }