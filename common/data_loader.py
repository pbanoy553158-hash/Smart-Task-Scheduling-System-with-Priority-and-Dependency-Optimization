import random
from typing import List
from common.task import Task

# ================================================================
# CONSTANTS
# ================================================================

TASK_NAMES = [
    "Research Paper", "Code Review", "Unit Testing", "Documentation",
    "Team Meeting", "Client Presentation", "Database Design", "API Development",
    "Frontend UI", "Backend Logic", "Security Audit", "Performance Testing",
    "Deployment", "User Training", "Bug Fixing", "Feature Implementation"
]

PREFIXES = ["TASK", "PROJ", "DEV", "TEST"]
random.seed(42)  # Fixed seed = reproducible results across runs


# ================================================================
# PUBLIC FUNCTIONS
# ================================================================

def generate_tasks(count: int) -> List[Task]:
    """
    Generate tasks WITHOUT dependencies (for baseline system)
    
    Args:
        count: Number of tasks to generate
        
    Returns:
        List of Task objects with empty prerequisites/dependencies
    """
    tasks = []
    for i in range(count):
        prefix = PREFIXES[i % len(PREFIXES)]
        task_id = f"{prefix}{i+1:04d}"           # e.g., TASK0001, PROJ0002
        name = f"{TASK_NAMES[i % len(TASK_NAMES)]} {i+1}"
        priority = random.randint(1, 5)           # 1=Critical, 5=Minimal
        deadline = _generate_deadline()
        tasks.append(Task(task_id, name, priority, deadline))
    return tasks


def generate_tasks_with_dependencies(count: int, dependency_percent: int = 70) -> List[Task]:
    """
    Generate tasks WITH dependencies for optimized system
    
    Creates a chain where every task depends on the previous task,
    ensuring visible dependencies in topological sort output.
    
    Args:
        count: Number of tasks to generate
        dependency_percent: Chance to add extra random dependencies (0-100)
        
    Returns:
        List of Task objects with prerequisites and dependencies populated
    """
    tasks = generate_tasks(count)
    
    # ============================================================
    # STEP 1: Create a linear dependency chain through ALL tasks
    # Task 1 depends on Task 0, Task 2 depends on Task 1, etc.
    # This guarantees topological sort has visible dependencies
    # ============================================================
    for i in range(1, count):
        dep_id = tasks[i-1].id
        if dep_id not in tasks[i].prerequisites:
            tasks[i].prerequisites.append(dep_id)          # Task i needs task i-1
            tasks[i-1].dependencies.append(tasks[i].id)    # Task i-1 blocks task i
    
    # ============================================================
    # STEP 2: Add extra random dependencies for graph complexity
    # Only looks back up to 15 tasks to avoid excessive complexity
    # ============================================================
    extra_count = 0
    for i in range(count):
        if random.randint(1, 100) < dependency_percent and i > 2:
            # Look back up to 15 tasks (not including immediate previous)
            possible = list(range(max(0, i - 15), i - 1))
            if possible:
                dep_idx = random.choice(possible)
                dep_id = tasks[dep_idx].id
                if dep_id not in tasks[i].prerequisites:
                    tasks[i].prerequisites.append(dep_id)
                    tasks[dep_idx].dependencies.append(tasks[i].id)
                    extra_count += 1
    
    # ============================================================
    # STEP 3: Print statistics for debugging
    # ============================================================
    tasks_with_deps = sum(1 for t in tasks if t.prerequisites)
    total_deps = sum(len(t.prerequisites) for t in tasks)
    
    print(f"[GEN] Tasks: {count} | With deps: {tasks_with_deps} ({tasks_with_deps*100//count}%) | Edges: {total_deps}")
    
    return tasks


# ================================================================
# PRIVATE HELPER FUNCTIONS
# ================================================================

def _generate_deadline() -> int:
    """
    Generate random deadline in YYYYMMDD format
    
    Returns:
        int like 20251215 for December 15, 2025
    """
    year = 2025 + random.randint(0, 1)   # 2025 or 2026
    month = random.randint(1, 12)
    day = random.randint(1, 28)          # Use 28 to avoid month length issues
    return year * 10000 + month * 100 + day


# ================================================================
# TESTING BLOCK (runs only when script executed directly)
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing data_loader.py")
    print("=" * 60)
    
    tasks = generate_tasks_with_dependencies(50, dependency_percent=70)
    
    print("\nFirst 15 tasks and their prerequisites:")
    for task in tasks[:15]:
        prereq_str = ", ".join(task.prerequisites) if task.prerequisites else "None"
        print(f"   {task.id}: {prereq_str}")
