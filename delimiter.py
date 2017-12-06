import csv

with open('test2.csv', 'r', errors='ignore') as fin, \
     open('test2_d.csv', 'w', newline='', encoding='utf-8', errors='ignore') as fout:
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, reader.fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(reader)
