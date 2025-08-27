import time
import lower_to_capital

for i in range(101):
    print("\r{:3}%".format(i),end='')
    time.sleep(0.01)

print('\n',lower_to_capital.lowertocapital('abc'))