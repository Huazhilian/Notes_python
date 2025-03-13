import os
os.chdir(r'C:\Users\Taylor\OneDrive\桌面\FOUND.000\ChkBack 2 Results')

files = os.listdir('./')

with open("ChkBack summary.txt", "r") as f:  # 打开文件
    data = f.readlines()  # 读取文件
    word='Unknown'
    list=[]

for index in range(len(data)):
    if data[index].find(word)!=-1:
        list.append(index)

print(list)
datanew=[data[i] for i in list]
print(datanew)

for fileName in files:
    portion = os.path.splitext(fileName)
    if portion in datanew:
        newName = portion[0] + ".jpg"
        os.rename(fileName, newName)