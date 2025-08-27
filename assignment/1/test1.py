# coding=utf-8
import sys

if __name__ == "__main__":
    a = sys.stdin.readline().strip()
    n, b = map(int, a.split())
    lis = []
    total = 0
    x=0
    for _ in range(n):
        line = sys.stdin.readline().strip()
        values = int(line)
        lis.append(values)

    lis.sort(reverse=True)  

    for i in range(len(lis)):
        if total < b:
            total += lis[i]  # take the value directly
        else:
            x=i
            break
    print('min_times=',x)

#test sets:
# 5 15
3
2
1
4
6

