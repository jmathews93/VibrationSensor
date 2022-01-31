from matplotlib import pyplot as plt
import csv
import pandas as pd

# msft = pd.read_csv('msft.csv')

csvfile = open('vibration_data/barefoot/barefoot2Steps2.csv', newline='')
reader = csv.DictReader(csvfile)

x1 = []
x2 = []
x3 = []
x4 = []
y1 = []
y2 = []
y3 = []
y4 = []

for row in reader:
    if int(row["deviceNum"]) == 1:
        x1.append(int(row["time"]))
        y1.append(int(row["data"]))
    elif int(row["deviceNum"]) == 2:
        x2.append(int(row["time"]))
        y2.append(int(row["data"]))
    elif int(row["deviceNum"]) == 3:
        x3.append(int(row["time"]))
        y3.append(int(row["data"]))
    elif int(row["deviceNum"]) == 4:
        x4.append(int(row["time"]))
        y4.append(int(row["data"]))



# print(x4)
# input()

plt.plot(x1, y1, 'lightcoral', linewidth=3, label='1')
plt.plot(x2, y2, 'palegreen', linewidth=3, label='2')
plt.plot(x3, y3, 'khaki', linewidth=3, label='3')
plt.plot(x4, y4, 'cornflowerblue', linewidth=3, label='4')
plt.ylabel("Percent Anticipated")
plt.xlabel("AEPercent of Train Data")

plt.legend()
plt.show()