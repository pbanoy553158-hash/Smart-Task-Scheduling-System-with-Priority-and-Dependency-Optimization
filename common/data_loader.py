"""
Generates sample task data for testing
"""
import random
from typing import List
from common.task import Task

TASK_NAMES = [
    "Research Paper", "Code Review", "Unit Testing", "Documentation",
    "Team Meeting", "Client Presentation", "Database Design", "API Development",
    "Frontend UI", "Backend Logic", "Security Audit", "Performance Testing",
    "Deployment", "User Training", "Bug Fixing", "Feature Implementation"
]

PREFIXES = ["TASK", "PROJ", "DEV", "TEST"]
random.seed(42)

def generate_tasks(count: int) -> List[Task]:
    tasks = []
    for i in range(count):
        prefix = PREFIXES[i % len(PREFIXES)]
        task_id = f"{prefix}{i+1:04d}"
        name = f"{TASK_NAMES[i % len(TASK_NAMES)]} {i+1}"
        priority = random.randint(1, 5)
        deadline = _generate_deadline()
        tasks.append(Task(task_id, name, priority, deadline))
    return tasks

def generate_tasks_with_dependencies(count: int, dependency_percent: int = 30) -> List[Task]:
    tasks = generate_tasks(count)
    for i in range(1, count):
        if random.randint(1, 100) < dependency_percent:
            dep_index = random.randint(0, i - 1)
            tasks[i].prerequisites.append(tasks[dep_index].id)
            tasks[dep_index].dependencies.append(tasks[i].id)
    return tasks

def _generate_deadline() -> int:
    year = 2025 + random.randint(0, 1)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return year * 10000 + month * 100 + day