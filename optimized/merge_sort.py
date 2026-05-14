"""
Merge Sort implementation - O(n log n)
"""
from typing import List
from common.task import Task

def sort_by_deadline(tasks: List[Task]) -> List[Task]:
    if tasks is None or len(tasks) <= 1:
        return tasks
    arr = tasks.copy()
    _merge_sort_by_deadline(arr, 0, len(arr) - 1)
    return arr

def _merge_sort_by_deadline(arr: List[Task], left: int, right: int) -> None:
    if left < right:
        mid = (left + right) // 2
        _merge_sort_by_deadline(arr, left, mid)
        _merge_sort_by_deadline(arr, mid + 1, right)
        _merge_by_deadline(arr, left, mid, right)

def _merge_by_deadline(arr: List[Task], left: int, mid: int, right: int) -> None:
    left_arr = arr[left:mid+1]
    right_arr = arr[mid+1:right+1]
    i = j = 0
    k = left
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i].deadline <= right_arr[j].deadline:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

def sort_by_priority(tasks: List[Task]) -> List[Task]:
    if tasks is None or len(tasks) <= 1:
        return tasks
    arr = tasks.copy()
    _merge_sort_by_priority(arr, 0, len(arr) - 1)
    return arr

def _merge_sort_by_priority(arr: List[Task], left: int, right: int) -> None:
    if left < right:
        mid = (left + right) // 2
        _merge_sort_by_priority(arr, left, mid)
        _merge_sort_by_priority(arr, mid + 1, right)
        _merge_by_priority(arr, left, mid, right)

def _merge_by_priority(arr: List[Task], left: int, mid: int, right: int) -> None:
    left_arr = arr[left:mid+1]
    right_arr = arr[mid+1:right+1]
    i = j = 0
    k = left
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i].priority <= right_arr[j].priority:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1