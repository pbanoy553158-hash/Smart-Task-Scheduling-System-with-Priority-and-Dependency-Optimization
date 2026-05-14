"""
Smart Task Scheduling System - Complete GUI
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.task import Task
from common.data_loader import generate_tasks, generate_tasks_with_dependencies
from baseline.baseline_scheduler import BaselineScheduler
from optimized.optimized_scheduler import OptimizedScheduler

class TaskSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Scheduling System")
        self.root.geometry("1400x850")
        self.root.configure(bg='#2b2b2b')
        
        self.current_system = "baseline"
        self.scheduler = BaselineScheduler()
        self.current_tasks = []
        
        self.setup_ui()
        self.log("System Ready - Select 'Load Tasks' to begin")
    
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
        
        left_panel = ttk.Frame(main_frame, width=380)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        sys_frame = ttk.LabelFrame(left_panel, text="System Selection", padding=10)
        sys_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.system_var = tk.StringVar(value="baseline")
        ttk.Radiobutton(sys_frame, text="Baseline System (ArrayList, Linear Search, Bubble Sort)", 
                        variable=self.system_var, value="baseline", command=self.switch_system).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(sys_frame, text="Optimized System (Graph, Heap, HashMap, Merge Sort)", 
                        variable=self.system_var, value="optimized", command=self.switch_system).pack(anchor=tk.W, pady=2)
        
        load_frame = ttk.LabelFrame(left_panel, text="Load Tasks", padding=10)
        load_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(load_frame, text="Load 100 Tasks", command=lambda: self.load_tasks(100)).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Load 500 Tasks", command=lambda: self.load_tasks(500)).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Load 1000 Tasks", command=lambda: self.load_tasks(1000)).pack(fill=tk.X, pady=2)
        
        search_frame = ttk.LabelFrame(left_panel, text="Search Task", padding=10)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.insert(0, "Enter Task ID (e.g., TASK0001)")
        self.search_entry.bind('<FocusIn>', lambda e: self.search_entry.delete(0, tk.END) if self.search_entry.get() == "Enter Task ID (e.g., TASK0001)" else None)
        
        ttk.Button(search_frame, text="Search", command=self.search_task).pack(fill=tk.X)
        
        sort_frame = ttk.LabelFrame(left_panel, text="Sort Tasks", padding=10)
        sort_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(sort_frame, text="Sort by Deadline", command=self.sort_by_deadline).pack(fill=tk.X, pady=2)
        ttk.Button(sort_frame, text="Sort by Priority", command=self.sort_by_priority).pack(fill=tk.X, pady=2)
        
        self.optimized_frame = ttk.LabelFrame(left_panel, text="Optimized Algorithms (Optimized System Only)", padding=10)
        ttk.Button(self.optimized_frame, text="Heap Schedule (Priority Order)", command=self.heap_schedule).pack(fill=tk.X, pady=2)
        ttk.Button(self.optimized_frame, text="Topological Sort (Dependency Order)", command=self.topological_sort).pack(fill=tk.X, pady=2)
        
        info_frame = ttk.LabelFrame(left_panel, text="System Info", padding=10)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.task_count_label = ttk.Label(info_frame, text="Tasks Loaded: 0")
        self.task_count_label.pack(anchor=tk.W)
        self.complexity_label = ttk.Label(info_frame, text="Complexity: O(n)")
        self.complexity_label.pack(anchor=tk.W)
        
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.task_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.task_frame, text="Task List")
        self.setup_task_table()
        
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Performance Results")
        self.setup_results_table()
        
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Log")
        
        self.log_text = tk.Text(self.log_frame, bg='#1e1e1e', fg='#00ff00', insertbackground='white', wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_task_table(self):
        columns = ("ID", "Task Name", "Priority", "Deadline", "Status", "Prerequisites")
        self.task_tree = ttk.Treeview(self.task_frame, columns=columns, show="headings", height=25)
        for col in columns:
            self.task_tree.heading(col, text=col)
            widths = {"ID": 90, "Task Name": 180, "Priority": 100, "Deadline": 100, "Status": 80, "Prerequisites": 150}
            self.task_tree.column(col, width=widths.get(col, 100))
        scrollbar = ttk.Scrollbar(self.task_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_results_table(self):
        columns = ("Operation", "Task Count", "Time (ms)", "Algorithm", "Complexity")
        self.results_tree = ttk.Treeview(self.results_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=130)
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def switch_system(self):
        system = self.system_var.get()
        self.current_system = system
        if system == "baseline":
            self.scheduler = BaselineScheduler()
            self.complexity_label.config(text="Complexity: Linear Search O(n) | Bubble Sort O(n²)")
            self.optimized_frame.pack_forget()
            self.log("Switched to BASELINE System")
        else:
            self.scheduler = OptimizedScheduler()
            self.complexity_label.config(text="Complexity: HashMap O(1) | Heap O(log n) | Merge Sort O(n log n)")
            self.optimized_frame.pack(fill=tk.X, pady=(0, 10))
            self.log("Switched to OPTIMIZED System")
        self.current_tasks = []
        self.update_task_table()
        self.task_count_label.config(text="Tasks Loaded: 0")
    
    def load_tasks(self, count):
        self.log(f"Loading {count} tasks...")
        def load():
            start_time = time.perf_counter()
            if self.current_system == "optimized":
                tasks = generate_tasks_with_dependencies(count, 30)
                self.scheduler.load_tasks_with_dependencies(tasks)
            else:
                tasks = generate_tasks(count)
                self.scheduler.load_tasks(tasks)
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            self.current_tasks = tasks
            self.root.after(0, self.update_task_table)
            self.root.after(0, lambda: self.task_count_label.config(text=f"Tasks Loaded: {count}"))
            operation = f"LOAD ({self.current_system.upper()})"
            algorithm = "ArrayList.addAll()" if self.current_system == "baseline" else "HashMap + Heap + Graph"
            complexity = "O(n)" if self.current_system == "baseline" else "O(1)+O(log n)+O(V)"
            self.root.after(0, lambda: self.add_result(operation, count, time_ms, algorithm, complexity))
            self.root.after(0, lambda: self.log(f"✅ Loaded {count} tasks in {time_ms:.4f} ms"))
        Thread(target=load).start()
    
    def search_task(self):
        if not self.current_tasks:
            self.log("No tasks loaded. Please load tasks first.")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        search_id = self.search_entry.get().strip()
        if search_id == "Enter Task ID (e.g., TASK0001)":
            self.log("Please enter a valid Task ID")
            return
        self.log(f"Searching for ID: {search_id}...")
        def search():
            start_time = time.perf_counter()
            if self.current_system == "baseline":
                found, comparisons = self.scheduler.linear_search(search_id)
            else:
                found = self.scheduler.hash_search(search_id)
                comparisons = 1
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            if found:
                self.root.after(0, lambda: self.log(f"✅ FOUND '{search_id}' in {time_ms:.4f} ms"))
                messagebox.showinfo("Task Found", f"ID: {found.id}\nName: {found.name}\nPriority: {found.get_priority_label()}\nDeadline: {found.get_formatted_deadline()}")
            else:
                self.root.after(0, lambda: self.log(f"❌ NOT FOUND '{search_id}' in {time_ms:.4f} ms"))
                messagebox.showwarning("Task Not Found", f"Task '{search_id}' not found!")
            operation = f"SEARCH ({self.current_system.upper()})"
            algorithm = "Linear Scan" if self.current_system == "baseline" else "HashMap.get()"
            complexity = "O(n)" if self.current_system == "baseline" else "O(1) avg"
            self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, algorithm, complexity))
        Thread(target=search).start()
    
    def sort_by_deadline(self):
        if not self.current_tasks:
            self.log("No tasks loaded. Please load tasks first.")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        self.log("Sorting by deadline...")
        def sort_deadline():
            start_time = time.perf_counter()
            if self.current_system == "baseline":
                self.scheduler.bubble_sort_by_deadline()
            else:
                sorted_tasks = self.scheduler.merge_sort_by_deadline()
                self.scheduler.load_tasks_with_dependencies(sorted_tasks)
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            self.current_tasks = self.scheduler.get_tasks()
            self.root.after(0, self.update_task_table)
            operation = f"SORT BY DEADLINE ({self.current_system.upper()})"
            algorithm = "Bubble Sort" if self.current_system == "baseline" else "Merge Sort"
            complexity = "O(n²)" if self.current_system == "baseline" else "O(n log n)"
            self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, algorithm, complexity))
            self.root.after(0, lambda: self.log(f"✅ Sort by deadline completed in {time_ms:.4f} ms"))
        Thread(target=sort_deadline).start()
    
    def sort_by_priority(self):
        if not self.current_tasks:
            self.log("No tasks loaded. Please load tasks first.")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        self.log("Sorting by priority...")
        def sort_priority():
            start_time = time.perf_counter()
            if self.current_system == "baseline":
                self.scheduler.bubble_sort_by_priority()
            else:
                sorted_tasks = self.scheduler.merge_sort_by_priority()
                self.scheduler.load_tasks_with_dependencies(sorted_tasks)
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            self.current_tasks = self.scheduler.get_tasks()
            self.root.after(0, self.update_task_table)
            operation = f"SORT BY PRIORITY ({self.current_system.upper()})"
            algorithm = "Bubble Sort" if self.current_system == "baseline" else "Merge Sort"
            complexity = "O(n²)" if self.current_system == "baseline" else "O(n log n)"
            self.root.after(0, lambda: self.add_result(operation, len(self.current_tasks), time_ms, algorithm, complexity))
            self.root.after(0, lambda: self.log(f"✅ Sort by priority completed in {time_ms:.4f} ms"))
        Thread(target=sort_priority).start()
    
    def heap_schedule(self):
        if self.current_system != "optimized":
            self.log("Heap Schedule only available in Optimized System")
            messagebox.showinfo("Not Available", "Heap Schedule is only available in Optimized System!")
            return
        if not self.current_tasks:
            self.log("No tasks loaded. Please load tasks first.")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        self.log("Generating Heap Schedule (Priority Order)...")
        def heap_sched():
            start_time = time.perf_counter()
            scheduled = self.scheduler.heap_schedule()
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            self.root.after(0, lambda: self.display_schedule(scheduled, "Heap Schedule - Priority Order"))
            self.root.after(0, lambda: self.add_result("HEAP SCHEDULE", len(self.current_tasks), time_ms, "MinHeap Extract", "O(n log n)"))
            self.root.after(0, lambda: self.log(f"✅ Heap schedule generated in {time_ms:.4f} ms"))
        Thread(target=heap_sched).start()
    
    def topological_sort(self):
        if self.current_system != "optimized":
            self.log("Topological Sort only available in Optimized System")
            messagebox.showinfo("Not Available", "Topological Sort is only available in Optimized System!")
            return
        if not self.current_tasks:
            self.log("No tasks loaded. Please load tasks first.")
            messagebox.showwarning("No Tasks", "Please load tasks first!")
            return
        self.log("Generating Topological Sort (Dependency Order)...")
        def topo_sort():
            start_time = time.perf_counter()
            try:
                scheduled = self.scheduler.topological_sort_schedule()
                end_time = time.perf_counter()
                time_ms = (end_time - start_time) * 1000
                self.root.after(0, lambda: self.display_schedule(scheduled, "Topological Sort - Dependency Order"))
                self.root.after(0, lambda: self.add_result("TOPOLOGICAL SORT", len(self.current_tasks), time_ms, "Kahn's Algorithm", "O(V+E)"))
                self.root.after(0, lambda: self.log(f"✅ Topological sort completed in {time_ms:.4f} ms"))
            except ValueError as e:
                self.root.after(0, lambda: self.log(f"❌ Error: {e}"))
                messagebox.showerror("Cycle Detected", str(e))
        Thread(target=topo_sort).start()
    
    def display_schedule(self, scheduled, title):
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title(title)
        schedule_window.geometry("900x600")
        schedule_window.configure(bg='#2b2b2b')
        columns = ("Order", "Task ID", "Task Name", "Priority", "Deadline", "Prerequisites")
        tree = ttk.Treeview(schedule_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            widths = {"Order": 60, "Task ID": 100, "Task Name": 250, "Priority": 100, "Deadline": 100, "Prerequisites": 150}
            tree.column(col, width=widths.get(col, 100))
        for i, task in enumerate(scheduled[:200], 1):
            prereqs = ", ".join(task.prerequisites[:2]) if task.prerequisites else "None"
            if len(task.prerequisites) > 2:
                prereqs += "..."
            tree.insert("", tk.END, values=(i, task.id, task.name[:40], task.get_priority_label(), 
                                           task.get_formatted_deadline(), prereqs))
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Button(schedule_window, text="Close", command=schedule_window.destroy).pack(pady=10)
    
    def update_task_table(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        for task in self.current_tasks[:200]:
            prereqs = ", ".join(task.prerequisites[:2]) if task.prerequisites else "None"
            if len(task.prerequisites) > 2:
                prereqs += "..."
            self.task_tree.insert("", tk.END, values=(
                task.id, task.name[:40], task.get_priority_label(), task.get_formatted_deadline(), "Pending", prereqs
            ))
    
    def add_result(self, operation, count, time_ms, algorithm, complexity):
        self.results_tree.insert("", 0, values=(operation, count, f"{time_ms:.4f}", algorithm, complexity))
    
    def log(self, message):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskSchedulerGUI(root)
    root.mainloop()