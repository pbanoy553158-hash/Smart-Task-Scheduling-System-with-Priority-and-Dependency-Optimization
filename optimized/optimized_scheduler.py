"""
optimized_scheduler.py - Core optimized system with all algorithms
Author: Smart Task Scheduling System
Description: Manages tasks using Graph (DAG), MinHeap (priority), HashMap (lookup), Merge Sort
Complexities: Topological O(V+E) | Heap O(log n) | Merge Sort O(n log n) | HashMap O(1) avg
"""

from typing import List, Dict, Optional
from common.task import Task
from optimized.graph import Graph
from optimized.min_heap import MinHeap
from optimized.merge_sort import sort_by_deadline, sort_by_priority


class OptimizedScheduler:
    """
    Optimized Scheduler with O(1) search, O(log n) priority, O(n log n) sorting
    
    Components:
        - tasks: List of all tasks
        - task_map: HashMap for O(1) ID lookup
        - dependency_graph: DAG for topological sort
        - heap: MinHeap for priority scheduling
    """
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.task_map: Dict[str, Task] = {}
        self.dependency_graph: Graph[str] = Graph()
        self.heap: MinHeap[Task] = MinHeap()
    
    # ================================================================
    # LOAD METHODS
    # ================================================================
    
    def load_tasks(self, tasks: List[Task]) -> None:
        """Load tasks WITHOUT dependencies (for baseline comparison)"""
        self.tasks = tasks.copy()
        self.task_map.clear()
        self.dependency_graph.clear()
        self.heap.clear()
        
        for task in self.tasks:
            self.task_map[task.id] = task
            self.dependency_graph.add_vertex(task.id)
            self.heap.insert(task)
        
        print(f"[LOADED] {len(self.tasks)} tasks (no dependencies)")
    
    def load_tasks_with_dependencies(self, tasks: List[Task]) -> None:
        """Load tasks WITH dependencies and build graph edges"""
        self.tasks = tasks.copy()
        self.task_map.clear()
        self.dependency_graph.clear()
        self.heap.clear()
        
        # Step 1: Add all vertices
        for task in self.tasks:
            self.task_map[task.id] = task
            self.dependency_graph.add_vertex(task.id)
            self.heap.insert(task)
        
        # Step 2: Add all edges from prerequisites
        edge_count = 0
        for task in self.tasks:
            for prereq in task.prerequisites:
                if self.dependency_graph.add_edge(prereq, task.id):
                    edge_count += 1
        
        tasks_with_prereqs = sum(1 for t in self.tasks if t.prerequisites)
        print(f"[LOADED] {len(self.tasks)} tasks, {tasks_with_prereqs} with deps, {edge_count} edges")
    
    # ================================================================
    # SEARCH METHODS
    # ================================================================
    
    def hash_search(self, search_id: str) -> Optional[Task]:
        """O(1) average lookup using HashMap (Python dict)"""
        return self.task_map.get(search_id)
    
    def linear_search(self, search_id: str) -> tuple:
        """O(n) linear search for baseline comparison"""
        for i, task in enumerate(self.tasks):
            if task.id == search_id:
                return task, i + 1
        return None, len(self.tasks)
    
    # ================================================================
    # SORT METHODS (Merge Sort)
    # ================================================================
    
    def merge_sort_by_deadline(self) -> List[Task]:
        """O(n log n) sort by deadline - updates internal state"""
        if not self.tasks:
            return []
        sorted_tasks = sort_by_deadline(self.tasks)
        self.tasks = sorted_tasks
        self.task_map = {task.id: task for task in self.tasks}
        print(f"[SORT] Sorted {len(self.tasks)} tasks by deadline")
        return self.tasks
    
    def merge_sort_by_priority(self) -> List[Task]:
        """
        O(n log n) sort by priority - NOT USED in final GUI
        Kept for reference; Heap Schedule is used instead
        """
        if not self.tasks:
            return []
        sorted_tasks = sort_by_priority(self.tasks)
        self.tasks = sorted_tasks
        self.task_map = {task.id: task for task in self.tasks}
        print(f"[SORT] Sorted {len(self.tasks)} tasks by priority")
        return self.tasks
    
    # ================================================================
    # SCHEDULING METHODS
    # ================================================================
    
    def heap_schedule(self) -> List[Task]:
        """
        Priority-based execution order using MinHeap
        Extracts tasks: Critical → High → Medium → Low → Minimal
        Complexity: O(n log n) for n extractions
        """
        if not self.tasks:
            return []
        
        # Create temporary heap with all tasks
        temp_heap = MinHeap()
        for task in self.tasks:
            temp_heap.insert(task)
        
        # Extract in priority order
        scheduled = []
        while not temp_heap.is_empty():
            task = temp_heap.extract_min()
            if task:
                scheduled.append(task)
        
        print(f"[HEAP] Scheduled {len(scheduled)} tasks in priority order")
        return scheduled
    
    def topological_sort_schedule(self) -> List[Task]:
        """
        Dependency-based execution order using Kahn's Algorithm
        Ensures prerequisites appear BEFORE dependents
        Complexity: O(V + E)
        """
        if not self.tasks:
            return []
        
        # Check for cycles first (invalid DAG)
        if self.dependency_graph.has_cycle():
            print("[TOPO] Cycle detected! Cannot perform topological sort.")
            return []
        
        # Get topological order
        order = self.dependency_graph.topological_sort()
        if not order:
            return []
        
        # Convert IDs back to Task objects
        result = []
        for task_id in order:
            if task_id in self.task_map:
                result.append(self.task_map[task_id])
        
        print(f"[TOPO] Sorted {len(result)} tasks in dependency order")
        return result
    
    # ================================================================
    # GETTER METHODS
    # ================================================================
    
    def get_tasks(self) -> List[Task]:
        """Return current task list"""
        return self.tasks
    
    def get_task_count(self) -> int:
        """Return number of tasks loaded"""
        return len(self.tasks)
    
    def get_dependency_count(self) -> int:
        """Return total number of prerequisite edges"""
        return sum(len(task.prerequisites) for task in self.tasks)
