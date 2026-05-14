"""
BASELINE SYSTEM - As specified in documentation
Data Structure: ArrayList (Python list)
Algorithms: Linear Search O(n), Bubble Sort O(n²), FCFS Scheduling
"""
from typing import List, Optional, Tuple
from common.task import Task

class BaselineScheduler:
    def __init__(self):
        """Initialize empty task list"""
        self.tasks: List[Task] = []
    
    def load_tasks(self, tasks: List[Task]) -> None:
        """Load tasks into the system - O(n)"""
        self.tasks = tasks.copy()
    
    def linear_search(self, search_id: str) -> Tuple[Optional[Task], int]:
        """
        Linear Search O(n) - scans sequentially until match found
        Returns: (found_task, number_of_comparisons)
        """
        for i, task in enumerate(self.tasks):
            if task.id == search_id:
                return task, i + 1
        return None, len(self.tasks)
    
    def bubble_sort_by_deadline(self) -> None:
        """
        Bubble Sort O(n²) by deadline
        Repeatedly swaps adjacent elements if out of order
        """
        n = len(self.tasks)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if self.tasks[j].deadline > self.tasks[j + 1].deadline:
                    self.tasks[j], self.tasks[j + 1] = self.tasks[j + 1], self.tasks[j]
    
    def bubble_sort_by_priority(self) -> None:
        """
        Bubble Sort O(n²) by priority
        Lower priority number = higher priority (1=Critical, 5=Minimal)
        """
        n = len(self.tasks)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if self.tasks[j].priority > self.tasks[j + 1].priority:
                    self.tasks[j], self.tasks[j + 1] = self.tasks[j + 1], self.tasks[j]
    
    def fcfs_schedule(self) -> List[Task]:
        """
        First-Come, First-Served scheduling
        Returns tasks in insertion order - O(n)
        """
        return self.tasks.copy()
    
    def get_tasks(self) -> List[Task]:
        """Return current task list"""
        return self.tasks
    
    def get_task_count(self) -> int:
        """Return number of tasks"""
        return len(self.tasks)
    
    def clear_tasks(self) -> None:
        """Clear all tasks"""
        self.tasks.clear()