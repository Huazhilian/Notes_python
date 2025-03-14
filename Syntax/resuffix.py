# python批量更换后缀名
import os
import sys
os.chdir(r'C:\Users\Taylor\OneDrive\桌面\FOUND.000\ChkBack 2 Results') # 切换到目标目录

# 列出当前目录下所有的文件
files = os.listdir('./')
print('files',files)

for fileName in files:
	portion = os.path.splitext(fileName)
	# 后缀是 .CHK -> .jpg
	if portion[1] == ".CHK":
		#把原文件后缀名改为 txt
		newName = portion[0] + ".jpg" 
		os.rename(fileName, newName)



