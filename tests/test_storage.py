"""Tests for storage layer."""

import pytest
import tempfile
import os
import json
from storage import JSONStorage


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    temp = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp.close()
    yield temp.name
    # Cleanup
    if os.path.exists(temp.name):
        os.remove(temp.name)


class TestJSONStorage:
    """Test JSONStorage functionality."""
    
    def test_load_empty_file(self, temp_file):
        """Test loading from a non-existent file returns empty list."""
        os.remove(temp_file)  # Remove the file
        storage = JSONStorage(temp_file)
        tasks = storage.load()
        
        assert tasks == []
    
    def test_save_and_load(self, temp_file):
        """Test saving and loading tasks."""
        storage = JSONStorage(temp_file)
        
        tasks = [
            {'id': 1, 'description': 'Task 1', 'completed': False},
            {'id': 2, 'description': 'Task 2', 'completed': True}
        ]
        
        storage.save(tasks)
        loaded_tasks = storage.load()
        
        assert loaded_tasks == tasks
    
    def test_save_overwrites_existing(self, temp_file):
        """Test that save overwrites existing data."""
        storage = JSONStorage(temp_file)
        
        # Save initial tasks
        initial_tasks = [{'id': 1, 'description': 'Task 1'}]
        storage.save(initial_tasks)
        
        # Save new tasks
        new_tasks = [{'id': 2, 'description': 'Task 2'}]
        storage.save(new_tasks)
        
        loaded_tasks = storage.load()
        assert loaded_tasks == new_tasks
    
    def test_load_corrupted_file(self, temp_file):
        """Test loading from a corrupted JSON file returns empty list."""
        # Write invalid JSON
        with open(temp_file, 'w') as f:
            f.write('invalid json content {')
        
        storage = JSONStorage(temp_file)
        tasks = storage.load()
        
        assert tasks == []
    
    def test_clear(self, temp_file):
        """Test clearing storage."""
        storage = JSONStorage(temp_file)
        
        # Save some tasks
        tasks = [{'id': 1, 'description': 'Task 1'}]
        storage.save(tasks)
        
        # Clear storage
        storage.clear()
        
        assert not os.path.exists(temp_file)
    
    def test_file_format(self, temp_file):
        """Test that saved file is properly formatted JSON."""
        storage = JSONStorage(temp_file)
        
        tasks = [
            {'id': 1, 'description': 'Task 1'},
            {'id': 2, 'description': 'Task 2'}
        ]
        
        storage.save(tasks)
        
        # Read and verify it's valid JSON
        with open(temp_file, 'r') as f:
            content = f.read()
            loaded = json.loads(content)
            assert loaded == tasks