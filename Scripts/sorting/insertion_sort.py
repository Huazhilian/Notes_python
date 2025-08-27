def swap(arr, i):
    if arr[i] < arr[i - 1]:
        arr[i], arr[i - 1] = arr[i - 1], arr[i]

def insertion_sort(arr):
    for j in range(1, len(arr)): # breakpoint (red point) in debug mode
        for i in range(j,0,-1):
            swap(arr, i)

if __name__ == "__main__":
    arr=[8,3,7,8,4,5,9,2,1,6,0,3]
    insertion_sort(arr)
    print(arr)