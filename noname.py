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

		if web_soup.find(id='main').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='main').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='main').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='main').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='main').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='main').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='main') != None and web_soup.find(id='main') != '':
			col1 = web_soup.find(id='main')
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
		'https://www.stamfordpublicschools.org/aite-high-school/principals-corner',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/aite-mission-statement',
'https://www.stamfordpublicschools.org/district/public-affairs/files/aite-2021',
'https://www.stamfordpublicschools.org/aite-high-school/students/pages/bell-schedules',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/files/aite-strategic-school-improvement-plan-0',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/aite-vision-graduate',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/aite-glance',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/awards-and-recognition',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/directions-aite',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/slideshows/facility-virtual-tour',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/niche-ranking',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/school-profile',
'https://www.stamfordpublicschools.org/stamford-high-school/students/pages/merge-technology-hub',
'https://drive.google.com/file/d/1L-lWRvgSHAqCE6ZqkAMPk7pEEyvtTSmp/view',
'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships',
'https://www.stamfordpublicschools.org/aite-high-school/students/links/aite-edge-newspaper',
'https://www.stamfordpublicschools.org/aite-high-school/students/pages/community-service-info',
'https://www.stamfordpublicschools.org/aite-high-school/library-media-center',
'https://www.stamfordpublicschools.org/aite-high-school/students/pages/teaching-and-learning-resource',
'https://www.stamfordpublicschools.org/aite-high-school/students/pages/student-activities',

'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/academic-concentrations',
'https://www.stamfordpublicschools.org/district/news/sps-adopts-seal-biliteracy-recognizing-students-proficient-two-or-more-languages',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/architectural-engineering',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/biomedical-sciences-concentration',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/business',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/fine-arts',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/information-technology',
'http://vhslearning.org',
'https://docs.google.com/forms/d/e/1FAIpQLSfgUc8kQAFePmCmYqbk8ZKGCZAi8_G7DvQfNvV-eXzneXKPkA/viewform',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2021-2022',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/pages/sps-school-counseling-department',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/act',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/files/aite-school-counseling-calendar',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/pages/aite-school-counseling-video-1',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/pages/aite-school-counseling-video',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/pages/aite-school-counseling-video-0',
'https://www.stamfordpublicschools.org/aite-high-school/school-counseling-department-2018-2019/files/advanced-placement-presentation',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/cisco-networking-academy',
'https://www.stamfordpublicschools.org/westhill-high-school/guidance-department/pages/college-applications',
'https://www.stamfordpublicschools.org/stamford-high-school/guidance/pages/college-bound-athletes',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/college-board-sat',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/common-application',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/community-service',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/connecticut-construction-education-center',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/links/edgenuity-login-information',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/extra-help',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/financial-aid-fafsa',
'https://www.stamfordpublicschools.org/aite-high-school/school-counseling-department-2018-2019/files/how-log-volunteer-hours-naviance',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/links/khan-academy-college-board',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/pages/lgbtqia-information',
'https://www.stamfordpublicschools.org/aite-high-school/aite-school-counseling-department-2020-2021/links/nacac-college-fair-information',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/ncaa-clearinghouse',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/ncc-hs-partnership',
'https://docs.google.com/forms/d/e/1FAIpQLSe-5cn8FyhF7A9bqNLQW6Poh5giPW40JNoJpSaSltDGtcdFhw/viewform',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/naviance',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/project-lead-way',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/senior-internship',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/links/student-activities',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/timeline-11th-grade',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/timeline-12th-grade',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/timeline-9th-10th-grades',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/pages/uconn-ece',
'https://www.stamfordpublicschools.org/aite-high-school/guidance/links/virtual-high-school',
'https://www.stamfordpublicschools.org/westhill-high-school/whs-school-counseling-department/pages/working-papers-form-ed-301',
'https://aiteapparel.itemorder.com/shop/sale',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/school-profile',
'https://www.stamfordpublicschools.org/aite-high-school/about-us/pages/website-credits',
'http://www.aiteptso.org',
	]
	mainfolder = 'stamfordpublicschools'
	school_name = 'aite_high'
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
			elif len(tiers) == 10:
				t1 = tiers[-7].capitalize()
				t2 = tiers[-6].capitalize()
				t3 = tiers[-5].capitalize()
				t4 = tiers[-4].capitalize()
				t5 = tiers[-3].capitalize()
				t6 = tiers[-2].capitalize()
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
