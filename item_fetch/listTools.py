import pandas as pd
import csv

skinList = pd.DataFrame(columns=['name'])

f1 = open('list_r.csv', "w", encoding='utf-8')

data_reversed = []
with open('csv/list_backup.csv', "r", encoding='utf-8') as myfile:
    for row in reversed(list(csv.reader(myfile))):
        data_reversed.append(row)

print(data_reversed)

skinList.to_csv()

for entry in data_reversed:
    print(type(entry[0]))
    f1.write(str(entry[0]))

f1.close()
