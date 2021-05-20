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

folder = '../f_web_interface/static/files/buckeyevalley/'
files = glob.glob(f'{folder}*.csv')
# print(files)
files.remove(f'{folder}report.csv')
pages = 0
issues = 0
t1 = []
t2 = []
t3 = []

for file in files:
	with open(file, 'r', encoding='utf-8') as csv_file:
		csv_reader = csv.reader(csv_file)

		for row in csv_reader:
			pages += 1

			if len(row) > 0 :
				if not row[1] in t1:
					t1.append(row[1])

				if not row[2] in t2 and len(row[2]) > 0:
					t2.append(row[2])

				if not row[3] in t3 and len(row[3]) > 0:
					t3.append(row[3])

				if not row[6] in t3 and row[6] == 'Flagged':
					issues += 1


print('Pages:', pages - len(files))
print('Issues:', issues)
print('T1:', len(t1))
print('T2:', len(t2))
print('T3:', len(t3))
