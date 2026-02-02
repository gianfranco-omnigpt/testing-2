"""Tests for task management logic."""

import pytest
from tasks import TaskManager
from storage import JSONStorage
import tempfile
import os


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()
    storage = JSONStorage(temp_file.name)
    yield storage
    # Cleanup
    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)


@pytest.fixture
def task_manager(temp_storage):
    """Create a TaskManager instance for testing."""
    return TaskManager(temp_storage)


class TestTaskManager:
    """Test TaskManager functionality."""
    
    def test_add_task(self, task_manager):
        """Test adding a new task."""
        task = task_manager.add_task("Test task", "high")
        
        assert task['id'] == 1
        assert task['description'] == "Test task"
        assert task['priority'] == "high"
        assert task['completed'] is False
        assert task['created_at'] is not None
        assert task['completed_at'] is None
    
    def test_add_multiple_tasks(self, task_manager):
        """Test adding multiple tasks with sequential IDs."""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task3 = task_manager.add_task("Task 3")
        
        assert task1['id'] == 1
        assert task2['id'] == 2
        assert task3['id'] == 3
    
    def test_get_all_tasks(self, task_manager):
        """Test retrieving all tasks."""
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        
        tasks = task_manager.get_tasks()
        assert len(tasks) == 2
    
    def test_get_tasks_by_status(self, task_manager):
        """Test filtering tasks by status."""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task_manager.complete_task(task1['id'])
        
        pending = task_manager.get_tasks(status='pending')
        completed = task_manager.get_tasks(status='completed')
        
        assert len(pending) == 1
        assert len(completed) == 1
        assert pending[0]['id'] == task2['id']
        assert completed[0]['id'] == task1['id']
    
    def test_get_tasks_by_priority(self, task_manager):
        """Test filtering tasks by priority."""
        task_manager.add_task("High priority", "high")
        task_manager.add_task("Low priority", "low")
        task_manager.add_task("Medium priority", "medium")
        
        high_tasks = task_manager.get_tasks(priority='high')
        low_tasks = task_manager.get_tasks(priority='low')
        
        assert len(high_tasks) == 1
        assert len(low_tasks) == 1
        assert high_tasks[0]['priority'] == 'high'
    
    def test_complete_task(self, task_manager):
        """Test marking a task as complete."""
        task = task_manager.add_task("Test task")
        completed_task = task_manager.complete_task(task['id'])
        
        assert completed_task['completed'] is True
        assert completed_task['completed_at'] is not None
    
    def test_uncomplete_task(self, task_manager):
        """Test marking a completed task as incomplete."""
        task = task_manager.add_task("Test task")
        task_manager.complete_task(task['id'])
        uncompleted_task = task_manager.uncomplete_task(task['id'])
        
        assert uncompleted_task['completed'] is False
        assert uncompleted_task['completed_at'] is None
    
    def test_delete_task(self, task_manager):
        """Test deleting a task."""
        task = task_manager.add_task("Test task")
        task_manager.delete_task(task['id'])
        
        tasks = task_manager.get_tasks()
        assert len(tasks) == 0
    
    def test_delete_nonexistent_task(self, task_manager):
        """Test deleting a task that doesn't exist."""
        with pytest.raises(ValueError, match="Task #999 not found"):
            task_manager.delete_task(999)
    
    def test_clear_completed(self, task_manager):
        """Test clearing completed tasks."""
        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task3 = task_manager.add_task("Task 3")
        
        task_manager.complete_task(task1['id'])
        task_manager.complete_task(task2['id'])
        
        count = task_manager.clear_completed()
        
        assert count == 2
        assert len(task_manager.get_tasks()) == 1
    
    def test_get_statistics(self, task_manager):
        """Test getting task statistics."""
        task1 = task_manager.add_task("Task 1", "high")
        task_manager.add_task("Task 2", "medium")
        task_manager.add_task("Task 3", "low")
        
        task_manager.complete_task(task1['id'])
        
        stats = task_manager.get_statistics()
        
        assert stats['total'] == 3
        assert stats['completed'] == 1
        assert stats['pending'] == 2
        assert stats['by_priority']['high'] == 1
        assert stats['by_priority']['medium'] == 1
        assert stats['by_priority']['low'] == 1
    
    def test_persistence(self, temp_storage):
        """Test that tasks persist across TaskManager instances."""
        manager1 = TaskManager(temp_storage)
        manager1.add_task("Persistent task")
        
        # Create new manager with same storage
        manager2 = TaskManager(temp_storage)
        tasks = manager2.get_tasks()
        
        assert len(tasks) == 1
        assert tasks[0]['description'] == "Persistent task"