"""
Directed Acyclic Graph (DAG) for task dependencies
"""
from typing import Dict, List, Set, TypeVar, Generic
from collections import deque

T = TypeVar('T')

class Graph(Generic[T]):
    def __init__(self):
        self.adjacency: Dict[T, List[T]] = {}
        self.in_degree: Dict[T, int] = {}
        self.vertices: Set[T] = set()
    
    def add_vertex(self, vertex: T) -> None:
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency[vertex] = []
            self.in_degree[vertex] = 0
    
    def add_edge(self, source: T, destination: T) -> bool:
        if source not in self.vertices:
            self.add_vertex(source)
        if destination not in self.vertices:
            self.add_vertex(destination)
        if self._would_create_cycle(source, destination):
            return False
        self.adjacency[source].append(destination)
        self.in_degree[destination] = self.in_degree.get(destination, 0) + 1
        return True
    
    def _would_create_cycle(self, source: T, destination: T) -> bool:
        return self._can_reach(destination, source)
    
    def _can_reach(self, start: T, target: T) -> bool:
        if start == target:
            return True
        visited = set()
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.adjacency.get(current, []):
                if neighbor == target:
                    return True
                if neighbor not in visited:
                    queue.append(neighbor)
        return False
    
    def has_cycle(self) -> bool:
        temp_in_degree = self.in_degree.copy()
        queue = deque([v for v in self.vertices if temp_in_degree.get(v, 0) == 0])
        processed = 0
        while queue:
            current = queue.popleft()
            processed += 1
            for neighbor in self.adjacency.get(current, []):
                temp_in_degree[neighbor] -= 1
                if temp_in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return processed != len(self.vertices)
    
    def topological_sort(self) -> List[T]:
        result = []
        temp_in_degree = self.in_degree.copy()
        queue = deque([v for v in self.vertices if temp_in_degree.get(v, 0) == 0])
        while queue:
            current = queue.popleft()
            result.append(current)
            for neighbor in self.adjacency.get(current, []):
                temp_in_degree[neighbor] -= 1
                if temp_in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return result
    
    def clear(self) -> None:
        self.adjacency.clear()
        self.in_degree.clear()
        self.vertices.clear()