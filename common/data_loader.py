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
    """
    Generate tasks WITHOUT dependencies (for baseline system)
    
    Args:
        count: Number of tasks to generate
        
    Returns:
        List of Task objects with no dependencies
    """
    tasks = []
    for i in range(count):
        prefix = PREFIXES[i % len(PREFIXES)]
        task_id = f"{prefix}{i+1:04d}"
        name = f"{TASK_NAMES[i % len(TASK_NAMES)]} {i+1}"
        priority = random.randint(1, 5)
        deadline = _generate_deadline()
        tasks.append(Task(task_id, name, priority, deadline))
    return tasks


def generate_tasks_with_dependencies(count: int, dependency_percent: int = 40) -> List[Task]:
    """
    Generate tasks WITH dependencies (for optimized system)
    
    Creates three types of dependencies for better visualization:
    1. CHAIN A: First 20 tasks form a sequential chain (Task0 -> Task1 -> Task2...)
    2. CHAIN B: Tasks 100-120 form another chain (if count > 120)
    3. Random dependencies: 40% of remaining tasks get 1-2 random prerequisites
    
    Args:
        count: Number of tasks to generate
        dependency_percent: Chance a task gets a random dependency (default 40%)
        
    Returns:
        List of Task objects with prerequisites and dependencies
    """
    tasks = generate_tasks(count)
    
    # ================================================================
    # CHAIN A: Create a visible dependency chain for first 20-30 tasks
    # ================================================================
    chain_a_length = min(25, count)
    for i in range(1, chain_a_length):
        dep_id = tasks[i-1].id
        if dep_id not in tasks[i].prerequisites:
            tasks[i].prerequisites.append(dep_id)
            tasks[i-1].dependencies.append(tasks[i].id)
    
    # ================================================================
    # CHAIN B: Create another chain in the middle (if enough tasks)
    # ================================================================
    if count > 150:
        chain_b_start = 100
        chain_b_end = min(125, count)
        for i in range(chain_b_start + 1, chain_b_end):
            dep_id = tasks[i-1].id
            if dep_id not in tasks[i].prerequisites:
                tasks[i].prerequisites.append(dep_id)
                tasks[i-1].dependencies.append(tasks[i].id)
    
    # ================================================================
    # CHAIN C: Third chain near the end (if enough tasks)
    # ================================================================
    if count > 300:
        chain_c_start = 250
        chain_c_end = min(270, count)
        for i in range(chain_c_start + 1, chain_c_end):
            dep_id = tasks[i-1].id
            if dep_id not in tasks[i].prerequisites:
                tasks[i].prerequisites.append(dep_id)
                tasks[i-1].dependencies.append(tasks[i].id)
    
    # ================================================================
    # RANDOM DEPENDENCIES: Add extra dependencies to remaining tasks
    # ================================================================
    for i in range(chain_a_length, count):
        # Skip tasks already in chains
        if count > 150 and chain_b_start <= i < chain_b_end:
            continue
        if count > 300 and chain_c_start <= i < chain_c_end:
            continue
            
        if random.randint(1, 100) < dependency_percent:
            # Number of dependencies for this task (1 or 2)
            num_deps = random.randint(1, 2)
            
            for _ in range(num_deps):
                # Find potential predecessors (within last 15 tasks, not current)
                start_idx = max(0, i - 15)
                possible_deps = [j for j in range(start_idx, i) if j != i]
                
                if possible_deps:
                    dep_index = random.choice(possible_deps)
                    dep_id = tasks[dep_index].id
                    
                    if dep_id not in tasks[i].prerequisites:
                        tasks[i].prerequisites.append(dep_id)
                        tasks[dep_index].dependencies.append(tasks[i].id)
    
    # ================================================================
    # DEBUG OUTPUT (visible in console when running)
    # ================================================================
    tasks_with_deps = sum(1 for t in tasks if t.prerequisites)
    total_deps = sum(len(t.prerequisites) for t in tasks)
    total_dependents = sum(len(t.dependencies) for t in tasks)
    
    print(f"\n{'='*60}")
    print(f"📊 DEPENDENCY STATISTICS for {count} tasks:")
    print(f"   - Tasks with prerequisites: {tasks_with_deps}/{count} ({tasks_with_deps*100//count}%)")
    print(f"   - Total prerequisite edges: {total_deps}")
    print(f"   - Total dependent edges: {total_dependents}")
    print(f"   - Chains created: ", end="")
    chains = []
    if chain_a_length > 1:
        chains.append(f"Chain A (tasks 0-{chain_a_length-1})")
    if count > 150 and chain_b_end > chain_b_start + 1:
        chains.append(f"Chain B (tasks {chain_b_start}-{chain_b_end-1})")
    if count > 300 and chain_c_end > chain_c_start + 1:
        chains.append(f"Chain C (tasks {chain_c_start}-{chain_c_end-1})")
    print(", ".join(chains) if chains else "None")
    print(f"{'='*60}\n")
    
    return tasks


def _generate_deadline() -> int:
    """
    Generate a random deadline date in YYYYMMDD format
    
    Returns:
        Integer in format YYYYMMDD (e.g., 20251215 for Dec 15, 2025)
    """
    year = 2025 + random.randint(0, 1)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Using 28 to avoid month length issues
    return year * 10000 + month * 100 + day


# ================================================================
# HELPER FUNCTION: Preview dependencies (for testing)
# ================================================================
def preview_dependencies(count: int = 50):
    """
    Quick function to preview dependencies in console
    Useful for testing that dependencies are working correctly
    """
    tasks = generate_tasks_with_dependencies(count)
    print("\n📋 PREVIEW OF FIRST 20 TASKS WITH DEPENDENCIES:")
    print("-" * 80)
    shown = 0
    for task in tasks:
        if task.prerequisites and shown < 20:
            print(f"   {task.id}: '{task.name[:30]}'")
            print(f"      → Depends on: {', '.join(task.prerequisites[:3])}")
            shown += 1
    if shown == 0:
        print("   No dependencies found in first 20 tasks.")
    print("-" * 80)


# ================================================================
# TESTING BLOCK (run this file directly to test)
# ================================================================
if __name__ == "__main__":
    print("Testing data_loader.py")
    print("\n1. Testing generate_tasks(10):")
    tasks = generate_tasks(10)
    for t in tasks[:5]:
        print(f"   {t.id}: {t.name}")
    
    print("\n2. Testing generate_tasks_with_dependencies(100):")
    tasks_with_deps = generate_tasks_with_dependencies(100, dependency_percent=40)
    
    print("\n3. Preview dependencies:")
    preview_dependencies(50)
