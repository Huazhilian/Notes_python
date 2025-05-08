def pivot_sort(arr, low, high):
    pivot = arr[high]  
    i = low - 1 # elements with index <= i are <= pivot

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1 # increase as <= pivot elements increase
            arr[i], arr[j] = arr[j], arr[i] # move <= pivot element to the left
    arr[i + 1], arr[high] = arr[high], arr[i + 1] # put the pivot element in the middle
    return i + 1 # return the pivot index

def quick_sort(arr, low, high):
    if low < high:
        pivot_index = pivot_sort(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

if __name__ == "__main__":
    arr = [9, 3, 4, 7, 6, 2, 4]
    quick_sort(arr, 0, len(arr) - 1)
    print(arr)