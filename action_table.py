from preprocess import get_action_table
import csv

table = get_action_table()
file = open("table.csv", "w")

writer = csv.writer(file)
for key, value in table.items():
    writer.writerow([key[0], key[1], key[2], value.split()[0], value.split()[1:]])

file.close()