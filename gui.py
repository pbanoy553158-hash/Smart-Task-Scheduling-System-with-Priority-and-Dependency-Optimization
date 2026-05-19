"""
Smart Task Scheduling System - COMPLETE
With Priority Colors | 3 Operations: Deadline Sort, Heap Schedule, Topological Sort
Performance Results are automatically recorded
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.task import Task
from common.data_loader import generate_tasks, generate_tasks_with_dependencies
from baseline.baseline_scheduler import BaselineScheduler
from optimized.optimized_scheduler import OptimizedScheduler


class TaskSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Scheduling System")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')
        
        self.current_system = "optimized"
        self.scheduler = OptimizedScheduler()
        self.current_tasks = []
        
        self.setup_ui()
        self.log("System Ready - Load tasks to begin")
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#3c3c3c', foreground='white', borderwidth=0)
        style.map('TButton', background=[('active', '#5c5c5c')])
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabelframe', background='#2b2b2b', foreground='white')
        style.configure('TLabelframe.Label', background='#2b2b2b', foreground='#ffcc00')
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = ttk.Frame(main_frame, width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # ============================================================
        # SYSTEM SELECTION
        # ============================================================
        sys_frame = ttk.LabelFrame(left_panel, text="System Selection", padding=10)
        sys_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.system_var = tk.StringVar(value="optimized")
        ttk.Radiobutton(sys_frame, text="Baseline System (List, Linear Search, Bubble Sort)", 
                        variable=self.system_var, value="baseline", command=self.switch_system).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(sys_frame, text="Optimized System (Graph, Heap, HashMap, Merge Sort)", 
                        variable=self.system_var, value="optimized", command=self.switch_system).pack(anchor=tk.W, pady=2)
        
        # ============================================================
        # LOAD TASKS
        # ============================================================
        load_frame = ttk.LabelFrame(left_panel, text="Load Tasks", padding=10)
        load_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(load_frame, text="Load 100 Tasks", command=lambda: self.load_tasks(100)).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Load 500 Tasks", command=lambda: self.load_tasks(500)).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Load 1000 Tasks", command=lambda: self.load_tasks(1000)).pack(fill=tk.X, pady=2)
        
        # ============================================================
        # SEARCH
        # ============================================================
        search_frame = ttk.LabelFrame(left_panel, text="Search Task (HashMap O(1))", padding=10)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.insert(0, "Enter Task ID (e.g., TASK0001)")
        self.search_entry.bind('<FocusIn>', lambda e: self.search_entry.delete(0, tk.END))
        self.search_entry.bind('<Return>', lambda e: self.search_task())
        ttk.Button(search_frame, text="Search", command=self.search_task).pack(fill=tk.X)
        
        # ============================================================
        # SORT OPERATIONS
        # ============================================================
        sort_frame = ttk.LabelFrame(left_panel, text="Sort Operations", padding=10)
        sort_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(sort_frame, text="Sort by Deadline (Merge Sort O(n log n))", 
                   command=self.sort_by_deadline).pack(fill=tk.X, pady=2)
        
        # ============================================================
        # ADVANCED ALGORITHMS
        # ============================================================
        algo_frame = ttk.LabelFrame(left_panel, text="Advanced Algorithms (Optimized System)", padding=10)
        algo_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(algo_frame, text="Heap Schedule (Priority Order - MinHeap)", 
                   command=self.heap_schedule).pack(fill=tk.X, pady=2)
        ttk.Button(algo_frame, text="Topological Sort (Dependency Order - Kahn's Algorithm)", 
                   command=self.topological_sort).pack(fill=tk.X, pady=2)
        
        # ============================================================
        # SYSTEM INFO
        # ============================================================
        info_frame = ttk.LabelFrame(left_panel, text="System Info", padding=10)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.task_count_label = ttk.Label(info_frame, text="Tasks Loaded: 0")
        self.task_count_label.pack(anchor=tk.W)
        self.complexity_label = ttk.Label(info_frame, text="Complexity: O(1)+O(log n)+O(n log n)")
        self.complexity_label.pack(anchor=tk.W)
        
        ttk.Button(left_panel, text="Clear All", command=self.clear_all).pack(fill=tk.X, pady=10)
        
        # ============================================================
        # RIGHT PANEL - RESULTS
        # ============================================================
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Task List
        self.task_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.task_frame, text="Task List")
        self.setup_task_table()
        
        # Tab 2: Performance Results
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Performance Results")
        self.setup_results_table()
        
        # Tab 3: Log
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Log")
        self.log_text = tk.Text(self.log_frame, bg='#1e1e1e', fg='#00ff00', insertbackground='white', wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_task_table(self):
        """Task list table with priority colors"""
        columns = ("ID", "Task Name", "Priority", "Deadline", "Prerequisites")
        self.task_tree = ttk.Treeview(self.task_frame, columns=columns, show="headings", height=35)
        
        for col in columns:
            self.task_tree.heading(col, text=col)
        
        widths = {"ID": 100, "Task Name": 250, "Priority": 100, "Deadline": 100, "Prerequisites": 250}
        for col in columns:
            self.task_tree.column(col, width=widths.get(col, 100))
        
        # Priority color tags
        self.task_tree.tag_configure('Critical', background='#8B0000', foreground='white')
        self.task_tree.tag_configure('High', background='#B22222', foreground='white')
        self.task_tree.tag_configure('Medium', background='#8B8000', foreground='white')
        self.task_tree.tag_configure('Low', background='#006400', foreground='white')
        self.task_tree.tag_configure('Minimal', background='#1a4a1a', foreground='white')
        
        scrollbar = ttk.Scrollbar(self.task_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_results_table(self):
        """Performance results table - records all operations"""
        columns = ("Timestamp", "Operation", "Task Count", "Time (ms)", "Algorithm", "Complexity")
        self.results_tree = ttk.Treeview(self.results_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
        
        widths = {"Timestamp": 120, "Operation": 180, "Task Count": 80, "Time (ms)": 100, "Algorithm": 150, "Complexity": 120}
        for col in columns:
            self.results_tree.column(col, width=widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def add_result(self, operation: str, task_count: int, time_ms: float, algorithm: str, complexity: str):
        """Add a record to the performance results table"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_tree.insert("", 0, values=(
            timestamp, operation, task_count, f"{time_ms:.4f}", algorithm, complexity
        ))
        # Keep only last 50 results to avoid clutter
        if len(self.results_tree.get_children()) > 50:
            last_item = self.results_tree.get_children()[-1]
            self.results_tree.delete(last_item)
    
    def switch_system(self):
        system = self.system_var.get()
        self.current_system = system
        if system == "baseline":
            self.scheduler = BaselineScheduler()
            self.complexity_label.config(text="Complexity: Linear Search O(n) | Bubble Sort O(n²)")
            self.log("Switched to BASELINE System")
        else:
            self.scheduler = OptimizedScheduler()
            self.complexity_label.config(text="Complexity: HashMap O(1) | Heap O(log n) | Merge Sort O(n log n)")
            self.log("Switched to OPTIMIZED System")
        self.current_tasks = []
        self.update_task_table()
        self.task_count_label.config(text="Tasks Loaded: 0")
    
    def load_tasks(self, count: int):
        """Load tasks and record performance"""
        self.log(f"Loading {count} tasks...")
        
        def load():
            start_time = time.perf_counter()
            
            if self.current_system == "optimized":
                tasks = generate_tasks_with_dependencies(count, 70)
                self.scheduler.load_tasks_with_dependencies(tasks)
                algorithm = "HashMap + Heap + Graph"
                complexity = "O(1)+O(log n)+O(V+E)"
            else:
                tasks = generate_tasks(count)
                self.scheduler.load_tasks(tasks)
                algorithm = "list.append()"
                complexity = "O(1) avg"
            
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            self.current_tasks = self.scheduler.get_tasks()
            
            # Record result
            operation = f"LOAD ({self.current_system.upper()})"
            self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, algorithm, complexity))
            self.root.after(0, lambda: self.log(f"✅ Loaded {len(self.current_tasks)} tasks in {time_ms:.4f} ms"))
            self.root.after(0, self.update_task_table)
            self.root.after(0, lambda: self.task_count_label.config(text=f"Tasks Loaded: {len(self.current_tasks)}"))
        
        Thread(target=load).start()
    
    def search_task(self):
        """Search for a task by ID and record performance"""
        if not self.current_tasks:
            self.log("No tasks loaded!")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        
        search_id = self.search_entry.get().strip()
        if not search_id or search_id == "Enter Task ID (e.g., TASK0001)":
            self.log("Please enter a valid Task ID")
            return
        
        self.log(f"Searching for ID: {search_id}...")
        
        def search():
            # Run 100 iterations for accurate timing
            iterations = 100
            start_time = time.perf_counter()
            
            for _ in range(iterations):
                if self.current_system == "baseline":
                    found, _ = self.scheduler.linear_search(search_id)
                else:
                    found = self.scheduler.hash_search(search_id)
            
            end_time = time.perf_counter()
            time_ms = ((end_time - start_time) * 1000) / iterations
            
            # Get actual result
            if self.current_system == "baseline":
                found, _ = self.scheduler.linear_search(search_id)
                algorithm = "Linear Search"
                complexity = "O(n)"
            else:
                found = self.scheduler.hash_search(search_id)
                algorithm = "HashMap.get()"
                complexity = "O(1) avg"
            
            if found:
                self.root.after(0, lambda: self.log(f"✅ Found '{search_id}' in {time_ms:.6f} ms"))
                self.root.after(0, lambda: messagebox.showinfo("Task Found",
                    f"ID: {found.id}\nName: {found.name}\nPriority: {found.get_priority_label()}\nDeadline: {found.get_formatted_deadline()}"))
            else:
                self.root.after(0, lambda: self.log(f"❌ Not found '{search_id}' in {time_ms:.6f} ms"))
                self.root.after(0, lambda: messagebox.showwarning("Not Found", f"Task '{search_id}' not found!"))
            
            # Record result
            operation = f"SEARCH ({self.current_system.upper()})"
            self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, algorithm, complexity))
        
        Thread(target=search).start()
    
    def sort_by_deadline(self):
        """Sort tasks by deadline and record performance"""
        if not self.current_tasks:
            self.log("No tasks loaded!")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        
        self.log("Sorting by deadline...")
        
        def sort_deadline():
            start_time = time.perf_counter()
            
            if self.current_system == "baseline":
                self.scheduler.bubble_sort_by_deadline()
                self.current_tasks = self.scheduler.get_tasks()
                algorithm = "Bubble Sort"
                complexity = "O(n²)"
            else:
                sorted_tasks = self.scheduler.merge_sort_by_deadline()
                self.current_tasks = sorted_tasks
                algorithm = "Merge Sort"
                complexity = "O(n log n)"
            
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            
            self.root.after(0, self.update_task_table)
            self.root.after(0, lambda: self.log(f"✅ Sort by deadline completed in {time_ms:.4f} ms"))
            
            # Record result
            operation = f"SORT BY DEADLINE ({self.current_system.upper()})"
            self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, algorithm, complexity))
        
        Thread(target=sort_deadline).start()
    
    def heap_schedule(self):
        """Generate heap schedule (priority order) and record performance"""
        if self.current_system != "optimized":
            self.log("Heap Schedule only available in Optimized System")
            messagebox.showinfo("Not Available", "Heap Schedule is only available in Optimized System!")
            return
        
        if not self.current_tasks:
            self.log("No tasks loaded!")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        
        self.log("Generating Heap Schedule (Priority Order)...")
        
        def heap_sched():
            start_time = time.perf_counter()
            scheduled = self.scheduler.heap_schedule()
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            
            if not scheduled:
                self.root.after(0, lambda: self.log("❌ Heap schedule returned no tasks!"))
                return
            
            self.root.after(0, lambda: self.display_schedule(scheduled, "Heap Schedule - Priority Order (MinHeap)"))
            self.root.after(0, lambda: self.log(f"✅ Heap schedule generated {len(scheduled)} tasks in {time_ms:.4f} ms"))
            
            # Record result
            operation = "HEAP SCHEDULE (OPTIMIZED)"
            self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, "MinHeap Extract", "O(n log n)"))
        
        Thread(target=heap_sched).start()
    
    def topological_sort(self):
        """Generate topological sort (dependency order) and record performance"""
        if self.current_system != "optimized":
            self.log("Topological Sort only available in Optimized System")
            messagebox.showinfo("Not Available", "Topological Sort is only available in Optimized System!")
            return
        
        if not self.current_tasks:
            self.log("No tasks loaded!")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        
        self.log("Generating Topological Sort (Dependency Order)...")
        
        def topo_sort():
            start_time = time.perf_counter()
            try:
                scheduled = self.scheduler.topological_sort_schedule()
                end_time = time.perf_counter()
                time_ms = (end_time - start_time) * 1000
                
                if not scheduled:
                    self.root.after(0, lambda: self.log("❌ Topological sort returned no tasks!"))
                    return
                
                self.root.after(0, lambda: self.display_schedule(scheduled, "Topological Sort - Dependency Order (Kahn's Algorithm)"))
                self.root.after(0, lambda: self.log(f"✅ Topological sort generated {len(scheduled)} tasks in {time_ms:.4f} ms"))
                
                # Record result
                operation = "TOPOLOGICAL SORT (OPTIMIZED)"
                self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, "Kahn's Algorithm", "O(V+E)"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log(f"❌ Error: {e}"))
        
        Thread(target=topo_sort).start()
    
    def display_schedule(self, scheduled, title):
        """Display schedule results in a new window"""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("1000x650")
        win.configure(bg='#2b2b2b')
        
        columns = ("Order", "Task ID", "Task Name", "Priority", "Deadline", "Prerequisites")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=25)
        
        for col in columns:
            tree.heading(col, text=col)
        
        widths = {"Order": 60, "Task ID": 100, "Task Name": 300, "Priority": 100, "Deadline": 100, "Prerequisites": 200}
        for col in columns:
            tree.column(col, width=widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        for i, task in enumerate(scheduled, 1):
            prereqs = ", ".join(task.prerequisites[:2]) if task.prerequisites else "None"
            if len(task.prerequisites) > 2:
                prereqs += "..."
            tree.insert("", tk.END, values=(i, task.id, task.name[:45], task.get_priority_label(), task.get_formatted_deadline(), prereqs))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)
    
    def update_task_table(self):
        """Update task list table with priority colors"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        for task in self.current_tasks[:500]:
            prereqs = ", ".join(task.prerequisites[:2]) if task.prerequisites else "None"
            if len(task.prerequisites) > 2:
                prereqs += "..."
            
            priority_label = task.get_priority_label()
            self.task_tree.insert("", tk.END,
                values=(task.id, task.name[:40], priority_label, task.get_formatted_deadline(), prereqs),
                tags=(priority_label,))
    
    def clear_all(self):
        """Clear all tasks and results"""
        self.current_tasks = []
        self.scheduler = OptimizedScheduler() if self.current_system == "optimized" else BaselineScheduler()
        self.update_task_table()
        self.task_count_label.config(text="Tasks Loaded: 0")
        
        # Clear performance results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.log("Cleared all tasks and results")
    
    def log(self, message: str):
        """Add timestamped message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskSchedulerGUI(root)
    root.mainloop()
