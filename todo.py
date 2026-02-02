#!/usr/bin/env python3
"""Main CLI application for the to-do app."""

import click
from tasks import TaskManager
from storage import JSONStorage

# Initialize storage and task manager
storage = JSONStorage('tasks.json')
task_manager = TaskManager(storage)


@click.group()
def cli():
    """Simple To-Do CLI Application"""
    pass


@cli.command()
@click.argument('description')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high']), default='medium', help='Task priority')
def add(description, priority):
    """Add a new task."""
    task = task_manager.add_task(description, priority)
    click.echo(f"✓ Added task #{task['id']}: {description}")


@cli.command()
@click.option('--status', type=click.Choice(['all', 'pending', 'completed']), default='all', help='Filter by status')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high']), help='Filter by priority')
def list(status, priority):
    """List all tasks."""
    tasks = task_manager.get_tasks(status=status, priority=priority)
    
    if not tasks:
        click.echo("No tasks found.")
        return
    
    click.echo("\n" + "="*60)
    click.echo("TO-DO LIST")
    click.echo("="*60 + "\n")
    
    for task in tasks:
        status_icon = "✓" if task['completed'] else " "
        priority_color = {
            'high': 'red',
            'medium': 'yellow',
            'low': 'green'
        }.get(task['priority'], 'white')
        
        task_line = f"{task['id']}. [{status_icon}] {task['description']}"
        priority_badge = f"[{task['priority'].upper()}]"
        
        click.echo(f"{task_line} ", nl=False)
        click.secho(priority_badge, fg=priority_color)


@cli.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Mark a task as complete."""
    try:
        task = task_manager.complete_task(task_id)
        click.echo(f"✓ Completed task #{task_id}: {task['description']}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('task_id', type=int)
def uncomplete(task_id):
    """Mark a task as incomplete."""
    try:
        task = task_manager.uncomplete_task(task_id)
        click.echo(f"✓ Reopened task #{task_id}: {task['description']}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete this task?')
def delete(task_id):
    """Delete a task."""
    try:
        task = task_manager.delete_task(task_id)
        click.echo(f"✓ Deleted task #{task_id}: {task['description']}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
def clear():
    """Clear all completed tasks."""
    count = task_manager.clear_completed()
    click.echo(f"✓ Cleared {count} completed task(s)")


@cli.command()
def stats():
    """Show task statistics."""
    stats = task_manager.get_statistics()
    
    click.echo("\n" + "="*60)
    click.echo("TASK STATISTICS")
    click.echo("="*60 + "\n")
    
    click.echo(f"Total tasks: {stats['total']}")
    click.echo(f"Pending: {stats['pending']}")
    click.echo(f"Completed: {stats['completed']}")
    
    if stats['total'] > 0:
        completion_rate = (stats['completed'] / stats['total']) * 100
        click.echo(f"Completion rate: {completion_rate:.1f}%")
    
    click.echo(f"\nBy priority:")
    click.echo(f"  High: {stats['by_priority']['high']}")
    click.echo(f"  Medium: {stats['by_priority']['medium']}")
    click.echo(f"  Low: {stats['by_priority']['low']}")


if __name__ == '__main__':
    cli()