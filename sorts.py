import random
import time


def insertion_sort(arr):
    start = time.perf_counter()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j][0] > key[0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    end = time.perf_counter()
    return f"{end - start:0.4f} seconds"


def partition(arr, low, high):
    pi = (low - 1)
    pivot_index = random.choice(range(low, high))
    pivot = arr[pivot_index]

    for i in range(low, high):
        if arr[i][0] <= pivot[0]:
            pi += 1
            arr[pi], arr[i] = arr[i], arr[pi]
    arr[pi + 1], arr[pivot_index] = arr[pivot_index], arr[pi + 1]
    return pi + 1


def quick_sort(arr):
    start = time.perf_counter()
    quick_sort_code(arr, 0, len(arr) - 1)
    end = time.perf_counter()
    return f"{end - start:0.4f} seconds"


def quick_sort_code(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_code(arr, low, pi - 1)
        quick_sort_code(arr, pi + 1, high)


def merge_sort(arr):
    start = time.perf_counter()
    merge_sort_code(arr)
    end = time.perf_counter()
    return f"{end - start:0.4f} seconds"


def merge_sort_code(arr):
    if len(arr) > 1:

        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort_code(left)
        merge_sort_code(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i][0] < right[j][0]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
