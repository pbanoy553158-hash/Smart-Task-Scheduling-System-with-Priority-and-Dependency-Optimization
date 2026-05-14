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
        self.tasks = tasks.copy()
        self.task_map.clear()
        self.dependency_graph.clear()
        self.heap.clear()
        for task in self.tasks:
            self.task_map[task.id] = task
            self.dependency_graph.add_vertex(task.id)
            self.heap.insert(task)
        for task in self.tasks:
            for prereq in task.prerequisites:
                self.dependency_graph.add_edge(prereq, task.id)
    
    def hash_search(self, search_id: str) -> Optional[Task]:
        return self.task_map.get(search_id)
    
    def linear_search(self, search_id: str) -> tuple:
        for i, task in enumerate(self.tasks):
            if task.id == search_id:
                return task, i + 1
        return None, len(self.tasks)
    
    def merge_sort_by_deadline(self) -> List[Task]:
        return sort_by_deadline(self.tasks)
    
    def merge_sort_by_priority(self) -> List[Task]:
        return sort_by_priority(self.tasks)
    
    def heap_schedule(self) -> List[Task]:
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
        if self.dependency_graph.has_cycle():
            raise ValueError("Cycle detected! Cannot perform topological sort.")
        order = self.dependency_graph.topological_sort()
        result = []
        for task_id in order:
            if task_id in self.task_map:
                result.append(self.task_map[task_id])
        return result
    
    def get_tasks(self) -> List[Task]:
        return self.tasks