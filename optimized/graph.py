"""
Directed Acyclic Graph (DAG) for task dependencies
"""
from typing import Dict, List, Set, TypeVar, Generic
from collections import deque

T = TypeVar('T')

class Graph(Generic[T]):
    def __init__(self):
        self.adjacency: Dict[T, List[T]] = {}
        self.vertices: Set[T] = set()
    
    def add_vertex(self, vertex: T) -> None:
        """Add a vertex to the graph"""
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency[vertex] = []
    
    def add_edge(self, source: T, destination: T) -> bool:
        """Add a directed edge from source -> destination"""
        # Ensure both vertices exist
        self.add_vertex(source)
        self.add_vertex(destination)
        
        # Add the edge if not already present
        if destination not in self.adjacency[source]:
            self.adjacency[source].append(destination)
            return True
        return False
    
    def has_cycle(self) -> bool:
        """Detect if graph has a cycle using DFS"""
        visited = set()
        rec_stack = set()
        
        def dfs(vertex: T) -> bool:
            visited.add(vertex)
            rec_stack.add(vertex)
            
            for neighbor in self.adjacency.get(vertex, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(vertex)
            return False
        
        for vertex in self.vertices:
            if vertex not in visited:
                if dfs(vertex):
                    return True
        return False
    
    def topological_sort(self) -> List[T]:
        """Kahn's algorithm - returns vertices in topological order"""
        # Calculate in-degree for each vertex
        in_degree: Dict[T, int] = {v: 0 for v in self.vertices}
        
        for u in self.adjacency:
            for v in self.adjacency[u]:
                in_degree[v] = in_degree.get(v, 0) + 1
        
        # Queue of vertices with 0 in-degree
        queue = deque([v for v in self.vertices if in_degree[v] == 0])
        result = []
        
        while queue:
            u = queue.popleft()
            result.append(u)
            
            for v in self.adjacency.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        
        # If result length != vertices, there's a cycle
        if len(result) != len(self.vertices):
            print(f"[WARNING] Cycle detected! {len(self.vertices)} vertices, {len(result)} in result")
            return []
        
        return result
    
    def clear(self) -> None:
        """Clear all graph data"""
        self.adjacency.clear()
        self.vertices.clear()
    
    def get_edge_count(self) -> int:
        """Return total number of edges"""
        return sum(len(neighbors) for neighbors in self.adjacency.values())
    
    def print_debug(self) -> None:
        """Print graph structure for debugging"""
        print(f"\n[GRAPH DEBUG] Vertices: {len(self.vertices)}")
        print(f"[GRAPH DEBUG] Edges: {self.get_edge_count()}")
        
        # Show first 10 edges as sample
        shown = 0
        for vertex, neighbors in self.adjacency.items():
            if neighbors and shown < 10:
                print(f"   {vertex} -> {neighbors[:3]}{'...' if len(neighbors) > 3 else ''}")
                shown += 1
        
        if self.get_edge_count() > shown:
            print(f"   ... and {self.get_edge_count() - shown} more edges")
