def min_index(array):
    index=0
    for i in range(1,len(array)):
        if array[i]<array[index]:
            index=i
    return index

def selection_sort(array):
    length=len(array)
    for j in range(length):
        index=min_index(array[j:])+j
        array[j],array[index]=array[index],array[j]
    return array

array=[6,3,1,9,7,5,9,2,8,1,4]
selection_sort(array)
print(array)
        