import csv

with open(r'C:\Users\Taylor\OneDrive\Desktop\Code\Python\Notes\assignment\Data_1min.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    category = data[0]
    data = data[1:]
    
    print(category)
    print(len(data))