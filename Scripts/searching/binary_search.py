# Binary Search
import math

def binarysearch(array, num,lowerbound=0):
    length = len(array)
    mid = length // 2
    breakpoint()
    match length:
        case 0:
            return math.inf
        case 1:
            if array[0] != num:
                return math.inf
            else:
                return 0
        case _:
            match num:
                case _ if num == array[mid]:
                    return mid
                case _ if num < array[mid]:
                    return binarysearch(array[:mid], num, lowerbound)
                case _ if num > array[mid]:
                    return binarysearch(array[mid + 1:], num, lowerbound + mid + 1)+ mid + 1

array1=[1, 3, 7, 9];num1=8
result1=binarysearch(array1, num1)
print(f'The index of {num1} in {array1} is {result1}')

array2=[1, 3, 7];num2=7
result2=binarysearch(array2, num2)
print(f'The index of {num2} in {array2} is {result2}')