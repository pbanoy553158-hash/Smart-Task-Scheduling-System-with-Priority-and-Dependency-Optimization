"""
min_heap.py - Custom MinHeap implementation for priority queue
Author: Smart Task Scheduling System
Description: Implements MinHeap from scratch for O(log n) priority scheduling
Complexities: insert O(log n) | extract_min O(log n) | peek O(1)
"""

from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')  # Generic type (Task objects)


class MinHeap(Generic[T]):
    """
    MinHeap implementation from scratch for priority queue
    
    Heap property: parent.priority <= child.priority
    Used for scheduling tasks: Critical (1) first, Minimal (5) last
    
    Internal representation: array-based complete binary tree
        - Parent: (index - 1) // 2
        - Left child: (index * 2) + 1
        - Right child: (index * 2) + 2
    """
    
    def __init__(self):
        self.heap: List[T] = []   # Array-based heap storage
        self._size = 0            # Number of elements in heap
    
    # ================================================================
    # PUBLIC METHODS
    # ================================================================
    
    def insert(self, element: T) -> None:
        """Insert element and bubble up to maintain heap property - O(log n)"""
        self.heap.append(element)
        self._size += 1
        self._bubble_up(self._size - 1)
    
    def extract_min(self) -> Optional[T]:
        """
        Remove and return minimum (highest priority) element - O(log n)
        Steps:
            1. Save root (minimum element)
            2. Replace root with last element
            3. Remove last element
            4. Bubble down new root to maintain heap property
        """
        if self._size == 0:
            return None
        
        min_val = self.heap[0]                    # Save minimum
        last = self.heap[self._size - 1]          # Get last element
        self.heap[0] = last                       # Move last to root
        self.heap.pop()                           # Remove last
        self._size -= 1
        
        if self._size > 0:
            self._bubble_down(0)                  # Restore heap property
        
        return min_val
    
    def peek_min(self) -> Optional[T]:
        """Return minimum without removing - O(1)"""
        return self.heap[0] if self._size > 0 else None
    
    def size(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def clear(self) -> None:
        """Clear all elements from heap"""
        self.heap.clear()
        self._size = 0
    
    # ================================================================
    # PRIVATE HELPER METHODS
    # ================================================================
    
    def _bubble_up(self, index: int) -> None:
        """
        Move element up until heap property is restored
        Called after insertion at leaf
        """
        while index > 0:
            parent = (index - 1) // 2
            
            # Stop if parent has higher priority (smaller)
            if self._compare(self.heap[parent], self.heap[index]) <= 0:
                break
            
            # Swap with parent and continue upward
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent
    
    def _bubble_down(self, index: int) -> None:
        """
        Move element down until heap property is restored
        Called after extracting root (replaced with last element)
        """
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            
            # Find smallest among parent and children
            if left < self._size and self._compare(self.heap[left], self.heap[smallest]) < 0:
                smallest = left
            if right < self._size and self._compare(self.heap[right], self.heap[smallest]) < 0:
                smallest = right
            
            # Stop if parent is smallest (heap property satisfied)
            if smallest == index:
                break
            
            # Swap with smallest child and continue downward
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest
    
    def _compare(self, a: T, b: T) -> int:
        """
        Compare two tasks for priority ordering
        
        Returns:
            -1 if a has higher priority than b
             0 if equal priority and deadline
             1 if a has lower priority than b
        
        Priority order: Critical(1) > High(2) > Medium(3) > Low(4) > Minimal(5)
        Deadline used as tiebreaker (earlier = higher priority)
        """
        if hasattr(a, 'priority') and hasattr(b, 'priority'):
            # Compare priority first (lower number = higher priority)
            if a.priority != b.priority:
                return -1 if a.priority < b.priority else 1
            
            # Tiebreaker: earlier deadline = higher priority
            if hasattr(a, 'deadline') and hasattr(b, 'deadline'):
                return -1 if a.deadline < b.deadline else 1 if a.deadline > b.deadline else 0
        return 0
