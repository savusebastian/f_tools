import csv
import glob
import itertools
import sys


max_int = sys.maxsize

while True:
	try:
		csv.field_size_limit(max_int)
		break
	except OverflowError:
		max_int = int(max_int / 10)

folder = '/home/sebastian/Downloads/csvs/'
files = glob.glob(f'{folder}*.csv')
pages = 0
issues = 0
t1 = 0
t2 = 0
t3 = 0

for file in files:
	t1_arr = []
	t2_arr = []
	t3_arr = []

	with open(file, 'r', encoding='utf-8') as csv_file:
		csv_reader = csv.reader(csv_file)

		for row in csv_reader:
			pages += 1

			if len(row) > 0 :
				if not row[1] in t1_arr:
					t1_arr.append(row[1])

				if not row[2] in t2_arr and len(row[2]) > 0:
					t2_arr.append(row[2])

				if not row[3] in t3_arr and len(row[3]) > 0:
					t3_arr.append(row[3])

				if row[6] == 'Flagged':
					issues += 1

	t1 += len(t1_arr) - 1
	t2 += len(t2_arr) - 1
	t3 += len(t3_arr) - 1


print('District:', 'Yes' if len(files) > 1 else 'No')
print('Schools:', len(files) - 1)
print('T1:', t1)
print('T2:', t2)
print('T3:', t3)
print('Pages:', pages - len(files))
print('Issues:', issues)

# Github Token
# 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
