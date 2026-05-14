"""
OPTIMIZED SYSTEM - Graph, Heap, HashMap, Merge Sort
"""
from typing import List, Dict, Optional
from common.task import Task
from optimized.graph import Graph
from optimized.min_heap import MinHeap
from optimized.merge_sort import sort_by_deadline, sort_by_priority

class OptimizedScheduler:
    def __init__(self):
        self.tasks: List[Task] = []
        self.task_map: Dict[str, Task] = {}
        self.dependency_graph: Graph[str] = Graph()
        self.heap: MinHeap[Task] = MinHeap()
    
    def load_tasks(self, tasks: List[Task]) -> None:
        self.tasks = tasks.copy()
        self.task_map.clear()
        self.dependency_graph.clear()
        self.heap.clear()
        for task in self.tasks:
            self.task_map[task.id] = task
            self.dependency_graph.add_vertex(task.id)
            self.heap.insert(task)
    
    def load_tasks_with_dependencies(self, tasks: List[Task]) -> None:
        """Load tasks and build dependency graph"""
        self.tasks = tasks.copy()
        self.task_map.clear()
        self.dependency_graph.clear()
        self.heap.clear()
        
        # First, add all vertices
        for task in self.tasks:
            self.task_map[task.id] = task
            self.dependency_graph.add_vertex(task.id)
            self.heap.insert(task)
        
        # Second, add all edges (dependencies)
        edge_count = 0
        for task in self.tasks:
            for prereq in task.prerequisites:
                self.dependency_graph.add_edge(prereq, task.id)
                edge_count += 1
        
        # Debug output
        tasks_with_prereqs = sum(1 for t in self.tasks if t.prerequisites)
        print(f"\n[OPTIMIZED] Loaded {len(self.tasks)} tasks")
        print(f"[OPTIMIZED] Tasks with prerequisites: {tasks_with_prereqs}")
        print(f"[OPTIMIZED] Total dependency edges added: {edge_count}")
        print(f"[OPTIMIZED] Graph vertices: {len(self.dependency_graph.vertices)}")
        print(f"[OPTIMIZED] Graph edges: {self.dependency_graph.get_edge_count() if hasattr(self.dependency_graph, 'get_edge_count') else 'N/A'}")
        
        # Show first few dependencies as example
        if tasks_with_prereqs > 0:
            print(f"[OPTIMIZED] Sample dependencies:")
            shown = 0
            for task in self.tasks:
                if task.prerequisites and shown < 3:
                    print(f"   {task.id} ← depends on: {task.prerequisites}")
                    shown += 1
    
    def update_tasks_after_sort(self, sorted_tasks: List[Task]) -> None:
        """Update internal structures after sorting without full rebuild"""
        self.tasks = sorted_tasks
        self.task_map = {task.id: task for task in sorted_tasks}
    
    def hash_search(self, search_id: str) -> Optional[Task]:
        """O(1) average lookup using HashMap"""
        return self.task_map.get(search_id)
    
    def linear_search(self, search_id: str) -> tuple:
        """O(n) linear search for baseline comparison"""
        for i, task in enumerate(self.tasks):
            if task.id == search_id:
                return task, i + 1
        return None, len(self.tasks)
    
    def merge_sort_by_deadline(self) -> List[Task]:
        """O(n log n) merge sort by deadline"""
        return sort_by_deadline(self.tasks)
    
    def merge_sort_by_priority(self) -> List[Task]:
        """O(n log n) merge sort by priority"""
        return sort_by_priority(self.tasks)
    
    def heap_schedule(self) -> List[Task]:
        """Generate schedule using MinHeap priority order"""
        temp_heap = MinHeap()
        for task in self.tasks:
            temp_heap.insert(task)
        scheduled = []
        while not temp_heap.is_empty():
            task = temp_heap.extract_min()
            if task:
                scheduled.append(task)
        return scheduled
    
    def topological_sort_schedule(self) -> List[Task]:
        """Generate schedule respecting task dependencies using Kahn's algorithm"""
        if self.dependency_graph.has_cycle():
            raise ValueError("Cycle detected! Cannot perform topological sort.")
        
        order = self.dependency_graph.topological_sort()
        
        print(f"\n[TOPOLOGICAL SORT] Order length: {len(order)}")
        print(f"[TOPOLOGICAL SORT] Tasks in map: {len(self.task_map)}")
        
        result = []
        for task_id in order:
            if task_id in self.task_map:
                task = self.task_map[task_id]
                result.append(task)
        
        tasks_with_prereqs = sum(1 for t in result if t.prerequisites)
        print(f"[TOPOLOGICAL SORT] Tasks with prerequisites in result: {tasks_with_prereqs}/{len(result)}")
        
        if tasks_with_prereqs > 0:
            print(f"[TOPOLOGICAL SORT] Sample tasks with prerequisites from result:")
            shown = 0
            for task in result:
                if task.prerequisites and shown < 5:
                    print(f"   {task.id} → prerequisites: {task.prerequisites[:3]}")
                    shown += 1
        
        return result
    
    def get_tasks(self) -> List[Task]:
        return self.tasks
    
    def get_dependency_count(self) -> int:
        return sum(len(task.prerequisites) for task in self.tasks)
