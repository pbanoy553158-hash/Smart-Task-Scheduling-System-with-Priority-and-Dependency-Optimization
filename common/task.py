"""
Task model - stores task properties (id, name, priority, deadline)
"""
from typing import List

class Task:
    def __init__(self, task_id: str, name: str, priority: int, deadline: int):
        self.id = task_id
        self.name = name
        self.priority = priority          # 1=Critical, 5=Minimal
        self.deadline = deadline          # YYYYMMDD format
        self.dependencies: List[str] = []
        self.prerequisites: List[str] = []
        self.completed = False
        self.urgency_score = self._calculate_urgency()
    
    def _calculate_urgency(self) -> int:
        priority_weight = (6 - self.priority) * 10
        year = self.deadline // 10000
        month = (self.deadline // 100) % 100
        day = self.deadline % 100
        days_until = (year - 2025) * 365 + (month - 1) * 30 + day
        deadline_weight = max(0, 100 - days_until)
        return priority_weight + deadline_weight
    
    def get_formatted_deadline(self) -> str:
        d = str(self.deadline)
        if len(d) == 8:
            return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"
        return d
    
    def get_priority_label(self) -> str:
        labels = {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Minimal"}
        return labels.get(self.priority, f"P{self.priority}")
    
    def get_urgency_label(self) -> str:
        if self.urgency_score >= 80: return "Urgent"
        if self.urgency_score >= 60: return "High"
        if self.urgency_score >= 40: return "Medium"
        if self.urgency_score >= 20: return "Low"
        return "Minimal"
    
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.deadline < other.deadline