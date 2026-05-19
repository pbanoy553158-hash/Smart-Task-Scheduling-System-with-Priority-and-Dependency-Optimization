from typing import List


class Task:
    """
    Task model representing a schedulable unit with priority and dependencies

    Dependencies:
        - prerequisites: Tasks that MUST complete BEFORE this task
        - dependencies:  Tasks that MUST complete AFTER this task
    """
    
    def __init__(self, task_id: str, name: str, priority: int, deadline: int):
        """
        Initialize a new Task
        
        Args:
            task_id: Unique identifier (e.g., "TASK0001", "PROJ0002")
            name: Human-readable task name
            priority: 1=Critical, 2=High, 3=Medium, 4=Low, 5=Minimal
            deadline: Due date in YYYYMMDD format (e.g., 20251215)
        """
        self.id = task_id
        self.name = name
        self.priority = priority                    # 1=Critical → 5=Minimal
        self.deadline = deadline                    # YYYYMMDD format
        self.dependencies: List[str] = []           # Tasks that depend on THIS task
        self.prerequisites: List[str] = []          # Tasks THIS task depends on
        self.completed = False                      # Not used in current version
    
    # ================================================================
    # FORMATTING METHODS
    # ================================================================
    
    def get_formatted_deadline(self) -> str:
        """
        Convert YYYYMMDD integer to YYYY-MM-DD string
        
        Example: 20251215 → "2025-12-15"
        """
        d = str(self.deadline)
        if len(d) == 8:
            return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
        return d
    
    def get_priority_label(self) -> str:
        """Convert priority number (1-5) to human-readable label"""
        labels = {
            1: "Critical",
            2: "High", 
            3: "Medium",
            4: "Low",
            5: "Minimal"
        }
        return labels.get(self.priority, f"P{self.priority}")
    
    def get_priority_color(self) -> str:

        colors = {
            1: "#8B0000",   # Critical - Dark Red
            2: "#B22222",   # High - Firebrick Red
            3: "#8B8000",   # Medium - Gold/Brown
            4: "#006400",   # Low - Dark Green
            5: "#1a4a1a"    # Minimal - Forest Green
        }
        return colors.get(self.priority, "#2b2b2b")
    
    # ================================================================
    # COMPARISON METHODS (for MinHeap sorting)
    # ================================================================
    
    def __lt__(self, other):
        """
        Less-than comparison for MinHeap priority queue
        
        Sorts by:
            1. Priority (lower number = higher priority)
            2. Deadline (earlier date first) as tiebreaker
        """
        if self.priority != other.priority:
            return self.priority < other.priority   # Critical (1) < Minimal (5)
        return self.deadline < other.deadline       # Earlier deadline first
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Task({self.id}, priority={self.priority})"
