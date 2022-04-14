from pathlib import Path
from time import time
import csv

from bs4 import BeautifulSoup
import requests

from util import get_column


def get_content(web_page):
	col1 = 'Flagged'
	col2, col3, col4 = '', '', ''
	col_num = '1'
	page_nav = None
	meta_title = ''
	meta_keywords = ''
	meta_desc = ''
	form = ''
	embed = ''
	iframe = ''
	calendar = ''
	staff = ''
	news = ''
	issue_pages_counter = 0
	print(web_page)

	# if web_page != '#':
	try:
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}
		# web_link = requests.get(web_page, headers=headers, timeout=10, verify=False).content
		web_link = requests.get(web_page, headers=headers, timeout=10).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(class_='entry-content').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='entry-content').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='entry-content').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='entry-content').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='entry-content').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='entry-content').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='entry-content') != None and web_soup.find(class_='entry-content') != '':
			col1 = web_soup.find(class_='entry-content')
			col1 = get_column(col1)
		else:
			issue_pages_counter = 1

		col1 = str(col1)

		if len(col1) > 200000:
			col1 = 'Flagged'
			col2 = 'This page has too much content'
			col3 = ''
			col4 = ''
			col_num = '2'
			issue_pages_counter = 1
		elif len(col1) > 150000:
			col2 = col1[50000:100000]
			col3 = col1[100000:150000]
			col4 = col1[150000:]
			col1 = col1[:50000]
			col_num = '4'
			issue_pages_counter = 1
		elif len(col1) > 100000:
			col2 = col1[50000:100000]
			col3 = col1[100000:]
			col1 = col1[:50000]
			col_num = '3'
		elif len(col1) > 50000:
			col2 = col1[50000:]
			col1 = col1[:50000]
			col_num = '2'

		if len(col4) > 50000:
			col1 = 'Flagged'
			col2 = 'This page has too much content'
			col3 = ''
			col4 = ''
			col_num = '2'
			issue_pages_counter = 1
		elif len(col4) > 0:
			col_num = '4'

		return col1, col2, col3, col4, col_num, page_nav, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, issue_pages_counter

	# else:
	except Exception:
		issue_pages_counter = 1

		return col1, col2, col3, col4, col_num, page_nav, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, issue_pages_counter


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		'https://www.medfordma.org/departments',
		'https://www.medfordma.org/departments/animal-control',
		'https://www.medfordma.org/departments/assessor',
		'https://www.medfordma.org/departments/building-department',
		'https://www.medfordma.org/departments/department-of-public-works/dpw-links/cemetery-division',
		'https://www.medfordma.org/departments/city-clerk',
		'https://www.medfordma.org/departments/collector',
		'https://www.medfordma.org/community-preservation',
		'https://www.medfordma.org/departments/council-on-aging',
		'https://www.medfordma.org/departments/credit-union',
		'https://www.medfordma.org/departments/department-of-public-works',
		'https://www.medfordma.org/departments/electrical',
		'https://www.medfordma.org/departments/department-of-public-works/dpw-links/engineering-division',
		'https://www.medfordma.org/departments/finance-and-auditing',
		'https://www.medfordma.org/departments/fire-department',
		'https://www.medfordma.org/departments/department-of-public-works/dpw-links/forestry-division',
		'https://www.medfordma.org/departments/health-department',
		'https://www.medfordma.org/departments/department-of-public-works/dpw-links/highway-division',
		'https://www.medfordma.org/departments/human-resources',
		'https://www.medfordma.org/departments/information-technology',
		'https://www.medfordma.org/departments/law-department',
		'https://www.medfordma.org/mayor',
		'https://www.medfordma.org/departments/department-of-public-works/dpw-links/park-division',
		'https://www.medfordma.org/parking',
		'https://www.medfordma.org/departments/planning-development-sustainability',
		'https://www.medfordma.org/departments/voter-registration',
		'https://www.medfordma.org/departments/veterans',
		'https://www.medfordma.org/departments/department-of-public-works/dpw-links/water-and-sewer-division',
		'https://www.medfordma.org/departments/weights-and-measures',
		'https://www.medfordma.org/boards',
		'https://www.medfordma.org/departments/planning-development-sustainability/adult-use-marijuana-establishments',
		'https://www.medfordma.org/boards/civic-auditorium-and-convention-center-commission',
		'https://www.medfordma.org/boards/parking-policy',
		'https://www.medfordma.org/departments/disability',
		'https://www.medfordma.org/boards/commissioner-of-trust-funds',
		'https://www.medfordma.org/boards/community-development-board',
		'https://www.medfordma.org/boards/conservation-commission',
		'https://www.medfordma.org/boards/boards-firetaskforce',
		'https://www.medfordma.org/boards/historic-district-commission',
		'https://www.medfordma.org/boards/hormel-stadium-commission',
		'https://www.medfordma.org/departments/human-rights',
		'https://www.medfordma.org/boards/library-trustees',
		'https://www.medfordma.org/boards/license-commission',
		'https://www.medfordma.org/departments/department-of-public-works/dpw-links/park-division/park-commission',
		'https://www.medfordma.org/boards/small-cell-committee',
		'https://www.medfordma.org/boards/traffic-commission',
		'https://www.medfordma.org/welcome-to-medford ',
		'https://www.medfordma.org/boards/board-of-appeals',
		'https://www.medfordma.org/city-council',
		'https://www.medfordma.org/seeclickfix ',
		'https://www.medfordma.org/alerts',
		'https://www.medfordma.org/snow',
		'https://www.medfordma.org/street-sweeping',
		'https://www.medfordma.org/business-resources',
		'https://www.medfordma.org/business-development-resources',
		'https://www.medfordma.org/rodent-prevention',
		'https://www.medfordma.org/transportation',
		'https://www.medfordma.org/departments/department-of-public-works/fleet-maintenance-garage',
		'https://www.medfordma.org/mayor2/city-budget',
		'https://www.medfordma.org/departments/health-department/municipal-vulnerability-project',
		'https://www.medfordma.org/compplan',
		'https://www.medfordma.org/construction',
		'https://www.medfordma.org/coronavirus-information',
		'https://www.medfordma.org/covid-19-business-resources',
		'https://www.medfordma.org/arpa',
		'https://www.medfordma.org/covid-19-vaccine-information',
		'https://www.medfordma.org/coronavirus-information/medford-vaccination-rate-data',
		'https://www.medfordma.org/covid-19-positive-test-rates',
		'https://www.medfordma.org/volunteering',
		'https://www.medfordma.org/coronavirus-information/covid-19-support-recovery-resources',
		'https://www.medfordma.org/departments/finance-and-auditing/21459-2',
		'https://www.medfordma.org/departments/voter-registration/voter-registration',
		'https://www.medfordma.org/departments/recycling',
		'https://www.medfordma.org/departments/personnel/jobs',
		'https://www.medfordma.org/public-records-requests',
		'https://www.medfordma.org/airplane-noise',
	]
	mainfolder = 'medfordma'
	school_name = 'medfordma'
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open(f'../f_web_interface/static/files/{mainfolder}/report.csv', 'w', encoding='utf-8') as csv_report, open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
		csv_report = csv.writer(csv_report)
		csv_report.writerow(['School name', school_name])

		csv_writer = csv.writer(csv_main)
		csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Tier 6', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

		page_counter = 0
		issue_pages_counter = 0

		for link in all_sites:
			tiers = link.split('/')
			t1, t2, t3, t4, t5, t6 = '', '', '', '', '', ''

			if len(tiers) == 3:
				t1 = tiers[-1].capitalize()
			elif len(tiers) == 4:
				t1 = tiers[-1].capitalize()
			elif len(tiers) == 5:
				t1 = tiers[-2].capitalize()
				t2 = tiers[-1].capitalize()
			elif len(tiers) == 6:
				t1 = tiers[-3].capitalize()
				t2 = tiers[-2].capitalize()
				t3 = tiers[-1].capitalize()
			elif len(tiers) == 7:
				t1 = tiers[-4].capitalize()
				t2 = tiers[-3].capitalize()
				t3 = tiers[-2].capitalize()
				t4 = tiers[-1].capitalize()
			elif len(tiers) == 8:
				t1 = tiers[-5].capitalize()
				t2 = tiers[-4].capitalize()
				t3 = tiers[-3].capitalize()
				t4 = tiers[-2].capitalize()
				t5 = tiers[-1].capitalize()
			elif len(tiers) == 9:
				t1 = tiers[-6].capitalize()
				t2 = tiers[-5].capitalize()
				t3 = tiers[-4].capitalize()
				t4 = tiers[-3].capitalize()
				t5 = tiers[-2].capitalize()
				t6 = tiers[-1].capitalize()
			else:
				# t1 = tiers[-6].capitalize()
				# t2 = tiers[-5].capitalize()
				# t3 = tiers[-4].capitalize()
				# t4 = tiers[-3].capitalize()
				# t5 = tiers[-2].capitalize()
				# t6 = tiers[-1].capitalize()
				print(len(tiers))

			page_counter += 1

			if tiers[2].find(mainfolder) == -1:
				csv_writer.writerow([link, t1, t2, t3, t4, t5, t6, '1', 'Linked page', '', '', '', '', '', ''])
			else:
				col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(link)
				issue_pages_counter += content_ipc

				csv_writer.writerow([link, t1, t2, t3, t4, t5, t6, col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

				if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
					csv_report.writerow([link, form, embed, iframe, calendar, staff, news])

				# if nav_sec != None and nav_sec != '' and nav_sec != []:
				# 	for nav_link in nav_sec:
				# 		page_counter += 1
				# 		nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(link)
				# 		issue_pages_counter += content_ipc
				# 		csv_writer.writerow([link, str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])
				#
				# 		if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
				# 			csv_report.writerow([link, form, embed, iframe, calendar, staff, news])

		csv_report.writerow([])
		csv_report.writerow(['Pages scraped', page_counter])
		csv_report.writerow(['Issues', issue_pages_counter])
		csv_report.writerow([])
		csv_report.writerow([])
		csv_report.writerow([])

		# print('Finished:', site)

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
