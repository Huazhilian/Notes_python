def shell_sort(arr):
    n = len(arr)
    gap = n//2

    while gap > 0: 
        for i in range(gap, n):
            k = j = i
            while j >= gap and arr[j - gap] > arr[k]:
                arr[j-gap], arr[k] = arr[k], arr[j-gap] # swap arr[k] to the vary left
                k = j - gap # k goes to the position of the element that was swapped
                j -= gap # j goes to the next position
        gap //= 2 # gap halved
        
array=[9,8,3,7,5,6,4,1,3]
shell_sort(array)
print(array)
        