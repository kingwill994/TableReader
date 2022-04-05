import csv
a = "atmProp_englishLabel.csv"
file = open(a)
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
for row in csvreader:
    row.append(row)
print(row)
file.close()
