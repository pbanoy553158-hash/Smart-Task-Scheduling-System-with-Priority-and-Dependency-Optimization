"""
Custom MinHeap implementation for priority queue
"""
from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')

class MinHeap(Generic[T]):
    def __init__(self):
        self.heap: List[T] = []
        self._size = 0
    
    def insert(self, element: T) -> None:
        self.heap.append(element)
        self._size += 1
        self._bubble_up(self._size - 1)
    
    def extract_min(self) -> Optional[T]:
        if self._size == 0:
            return None
        min_val = self.heap[0]
        last = self.heap[self._size - 1]
        self.heap[0] = last
        self.heap.pop()
        self._size -= 1
        if self._size > 0:
            self._bubble_down(0)
        return min_val
    
    def peek_min(self) -> Optional[T]:
        return self.heap[0] if self._size > 0 else None
    
    def size(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def clear(self) -> None:
        self.heap.clear()
        self._size = 0
    
    def _bubble_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._compare(self.heap[parent], self.heap[index]) <= 0:
                break
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent
    
    def _bubble_down(self, index: int) -> None:
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            if left < self._size and self._compare(self.heap[left], self.heap[smallest]) < 0:
                smallest = left
            if right < self._size and self._compare(self.heap[right], self.heap[smallest]) < 0:
                smallest = right
            if smallest == index:
                break
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest
    
    def _compare(self, a: T, b: T) -> int:
        if hasattr(a, 'priority') and hasattr(b, 'priority'):
            if a.priority != b.priority:
                return -1 if a.priority < b.priority else 1
            if hasattr(a, 'deadline') and hasattr(b, 'deadline'):
                return -1 if a.deadline < b.deadline else 1 if a.deadline > b.deadline else 0
        return 0