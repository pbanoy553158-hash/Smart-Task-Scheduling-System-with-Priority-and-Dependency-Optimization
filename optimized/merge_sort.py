from typing import List
from common.task import Task


# ================================================================
# SORT BY DEADLINE (Main sorting method used in GUI)
# ================================================================

def sort_by_deadline(tasks: List[Task]) -> List[Task]:
    """
    Sort tasks by deadline (earliest first) using Merge Sort - O(n log n)
    
    Args:
        tasks: List of Task objects to sort
        
    Returns:
        New sorted list (original unchanged)
    """
    if tasks is None or len(tasks) <= 1:
        return tasks.copy() if tasks else []
    
    arr = tasks.copy()
    _merge_sort_by_deadline(arr, 0, len(arr) - 1)
    return arr


def _merge_sort_by_deadline(arr: List[Task], left: int, right: int) -> None:
    """
    Recursive divide step of Merge Sort
    
    Args:
        arr: Array to sort (modified in-place)
        left: Left boundary index
        right: Right boundary index
    """
    if left < right:
        mid = (left + right) // 2
        _merge_sort_by_deadline(arr, left, mid)      # Sort left half
        _merge_sort_by_deadline(arr, mid + 1, right) # Sort right half
        _merge_by_deadline(arr, left, mid, right)    # Merge sorted halves


def _merge_by_deadline(arr: List[Task], left: int, mid: int, right: int) -> None:
    """
    Conquer step: merge two sorted subarrays
    
    Subarrays:
        left_sub = arr[left:mid+1]
        right_sub = arr[mid+1:right+1]
    
    Merges by comparing deadlines (earlier deadline = smaller)
    """
    # Create copies of left and right subarrays
    left_arr = arr[left:mid+1]
    right_arr = arr[mid+1:right+1]
    
    i = j = 0          # Pointers for left_arr and right_arr
    k = left           # Pointer for original array
    
    # Merge while both subarrays have elements
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i].deadline <= right_arr[j].deadline:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    # Copy remaining elements from left subarray
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    # Copy remaining elements from right subarray
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1
