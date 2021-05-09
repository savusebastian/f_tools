import csv
import glob
import sys


max_int = sys.maxsize

while True:
	try:
		csv.field_size_limit(max_int)
		break
	except OverflowError:
		max_int = int(max_int / 10)

files = glob.glob('*.csv')
pages = 0
issues = 0
images = 0
docs = 0
size_limit_pages = 0

for file in files:
	with open(file, 'r', encoding='utf-8') as csv_file:
		csv_reader = csv.reader(csv_file)
		holder = []

		for row in csv_reader:
			if len(row) > 0 and len(row[1]) < 6:
				holder.append(row[1])

			if len(row) > 10 and len(row[7]) > 0:
				size_limit_pages += 1

		pages += int(holder[-4])
		issues += int(holder[-3])
		images += int(holder[-2])
		docs += int(holder[-1])

print('Pages:', pages)
print('Issues:', issues)
print('Images:', images)
print('Docs:', docs)
print('Size limit pages:', size_limit_pages)
