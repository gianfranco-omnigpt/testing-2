# ULTRA TODO!

A simple and efficient command-line interface application for managing your daily tasks and to-do lists.

## Features

- ✅ Add new tasks
- 📝 List all tasks
- ✔️ Mark tasks as complete
- ❌ Delete tasks
- 🔍 Filter tasks by status (pending/completed)
- 💾 Persistent storage

## Installation

```bash
# Clone the repository
git clone https://github.com/gianfranco-omnigpt/testing-2.git
cd testing-2

# Install dependencies (if any)
pip install -r requirements.txt
```

## Usage

```bash
# Add a new task
todo add "Buy groceries"

# List all tasks
todo list

# List pending tasks only
todo list --status pending

# Mark a task as complete
todo complete <task_id>

# Delete a task
todo delete <task_id>

# Show help
todo --help
```

## Examples

```bash
# Add multiple tasks
todo add "Write documentation"
todo add "Review pull requests"
todo add "Deploy to production"

# View all tasks
todo list
# Output:
# 1. [ ] Write documentation
# 2. [ ] Review pull requests
# 3. [ ] Deploy to production

# Complete a task
todo complete 1

# View updated list
todo list
# Output:
# 1. [✓] Write documentation
# 2. [ ] Review pull requests
# 3. [ ] Deploy to production
```

## Project Structure

```
testing-2/
├── README.md
├── requirements.txt
├── todo.py           # Main CLI application
├── tasks.py          # Task management logic
├── storage.py        # Data persistence layer
└── tests/
    ├── test_tasks.py
    └── test_storage.py
```

## Requirements

- Python 3.7+

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - feel free to use this project for learning and personal use.

## Roadmap

- [ ] Add priority levels to tasks
- [ ] Add due dates
- [ ] Add categories/tags
- [ ] Add search functionality
- [ ] Export tasks to different formats (JSON, CSV)
- [ ] Add task editing capability

## Author

Built with ❤️ by gianfranco-omnigpt