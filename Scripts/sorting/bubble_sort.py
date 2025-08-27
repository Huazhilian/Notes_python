import insertion_sort

def bubble_sort(arr):
    for i in range(len(arr), 1,-1):
        for j in range(1, i):
            insertion_sort.swap(arr, j)

if __name__ == "__main__":
    arr=[8,3,7,8,4,5,9,2,1,6,0,3]
    bubble_sort(arr)
    print(arr)
        