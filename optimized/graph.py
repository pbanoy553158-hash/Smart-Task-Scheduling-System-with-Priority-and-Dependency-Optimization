from typing import Dict, List, Set, TypeVar, Generic
from collections import deque

T = TypeVar('T')  # Generic type for vertices (String task IDs)


class Graph(Generic[T]):
    """
    Directed Acyclic Graph (DAG) for modeling task dependencies
    
    Edge meaning: source -> destination means source MUST complete BEFORE destination
    
    Data Structures:
        - adjacency: Maps vertex -> list of outgoing neighbors
        - vertices: Set of all vertices in graph
        - in_degree: Maps vertex -> number of incoming edges
    """
    
    def __init__(self):
        """Initialize empty graph"""
        self.adjacency: Dict[T, List[T]] = {}   # source -> [dest1, dest2, ...]
        self.vertices: Set[T] = set()           # all vertices
        self.in_degree: Dict[T, int] = {}       # vertex -> incoming edge count
    
    # ================================================================
    # VERTEX & EDGE OPERATIONS
    # ================================================================
    
    def add_vertex(self, vertex: T) -> None:
        """Add vertex to graph if not already present"""
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency[vertex] = []
            self.in_degree[vertex] = 0
    
    def add_edge(self, source: T, destination: T) -> bool:
        """
        Add directed edge: source -> destination
        Means: source MUST complete BEFORE destination
        
        Args:
            source: Prerequisite task
            destination: Dependent task
            
        Returns:
            True if edge added, False if edge already exists or self-loop
        """
        self.add_vertex(source)
        self.add_vertex(destination)
        
        # Prevent self-loop (task depending on itself)
        if source == destination:
            return False
        
        # Add edge if not already present
        if destination not in self.adjacency[source]:
            self.adjacency[source].append(destination)
            self.in_degree[destination] = self.in_degree.get(destination, 0) + 1
            return True
        return False
    
    # ================================================================
    # CYCLE DETECTION (DFS-based)
    # ================================================================
    
    def has_cycle(self) -> bool:
        """
        Detect if graph contains a cycle using DFS with recursion stack
        
        Returns:
            True if cycle exists (invalid for topological sort)
            False if graph is acyclic (valid DAG)
        """
        visited = set()     # Nodes fully processed
        rec_stack = set()   # Nodes in current DFS path (detects cycles)
        
        def dfs(vertex: T) -> bool:
            visited.add(vertex)
            rec_stack.add(vertex)
            
            for neighbor in self.adjacency.get(vertex, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Found back edge -> cycle exists
                    return True
            
            rec_stack.remove(vertex)
            return False
        
        # Check all vertices (graph may be disconnected)
        for vertex in self.vertices:
            if vertex not in visited:
                if dfs(vertex):
                    return True
        return False
    
    # ================================================================
    # TOPOLOGICAL SORT (Kahn's Algorithm - BFS based)
    # ================================================================
    
    def topological_sort(self) -> List[T]:
        """
        Kahn's Algorithm for Topological Sorting - O(V + E)
        
        Steps:
            1. Calculate in-degree for each vertex
            2. Add vertices with in-degree 0 to queue
            3. Remove vertex, decrease neighbors' in-degree
            4. Repeat until queue empty
        
        Returns:
            List of vertices in topological order (prerequisites first)
            Empty list if cycle detected
        """
        # Step 1: Calculate in-degree for all vertices
        in_degree: Dict[T, int] = {v: 0 for v in self.vertices}
        for u in self.adjacency:
            for v in self.adjacency[u]:
                in_degree[v] = in_degree.get(v, 0) + 1
        
        # Step 2: Initialize queue with vertices having no prerequisites (in-degree = 0)
        queue = deque([v for v in self.vertices if in_degree[v] == 0])
        result = []
        
        # Step 3 & 4: Process vertices in order
        while queue:
            u = queue.popleft()
            result.append(u)
            
            # Remove u's outgoing edges
            for v in self.adjacency.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        
        # Step 5: Check if all vertices were processed (no cycle)
        if len(result) != len(self.vertices):
            return []  # Cycle detected
        return result
    
    # ================================================================
    # UTILITY METHODS
    # ================================================================
    
    def clear(self) -> None:
        """Clear all graph data (reset for new task set)"""
        self.adjacency.clear()
        self.vertices.clear()
        self.in_degree.clear()
    
    def get_edge_count(self) -> int:
        """Return total number of edges in graph"""
        return sum(len(neighbors) for neighbors in self.adjacency.values())
