# Task Management - Manage todos and reminders

import json
import os
from datetime import datetime

TASKS_FILE = "jarvis_data/tasks.json"

def init_tasks():
    """Initialize task storage"""
    os.makedirs("jarvis_data", exist_ok=True)
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)

def add_task(title, description="", priority="medium", due_date=None):
    """Add a new task"""
    init_tasks()
    
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,
        "created": datetime.now().isoformat(),
        "due_date": due_date,
        "completed": False
    }
    
    tasks.append(task)
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    return f"✅ Task '{title}' added successfully"

def list_tasks(filter_by="all"):
    """List tasks (all, pending, completed)"""
    init_tasks()
    
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    if filter_by == "pending":
        tasks = [t for t in tasks if not t["completed"]]
    elif filter_by == "completed":
        tasks = [t for t in tasks if t["completed"]]
    
    if not tasks:
        return f"No {filter_by} tasks found"
    
    output = []
    output.append(f"\n📋 {filter_by.upper()} TASKS")
    output.append("="*60)
    
    for task in tasks:
        status = "✅" if task["completed"] else "⏳"
        output.append(f"{status} [{task['priority'].upper()}] {task['title']}")
        if task.get("due_date"):
            output.append(f"   Due: {task['due_date']}")
    
    output.append("="*60)
    return "\n".join(output)

def complete_task(task_id):
    """Mark task as completed"""
    init_tasks()
    
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            with open(TASKS_FILE, 'w') as f:
                json.dump(tasks, f, indent=2)
            return f"✅ Task '{task['title']}' completed"
    
    return f"Task ID {task_id} not found"

def get_task_summary():
    """Get task summary"""
    init_tasks()
    
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    total = len(tasks)
    completed = len([t for t in tasks if t["completed"]])
    pending = total - completed
    
    return f"📊 Tasks: {total} total | ✅ {completed} completed | ⏳ {pending} pending"
