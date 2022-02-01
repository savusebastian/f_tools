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

		if web_soup.find(class_='ptl_page').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='ptl_page').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='ptl_page').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='ptl_page').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='ptl_page').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='ptl_page').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='ptl_page') != None and web_soup.find(class_='ptl_page') != '':
			col1 = web_soup.find(class_='ptl_page')
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
		'https://chs.ceres.k12.ca.us',
		'https://chs.ceres.k12.ca.us/staff',
		'https://chs.ceres.k12.ca.us/staff/staff_resources',
		'https://chs.ceres.k12.ca.us/contact_school',
		'https://chs.ceres.k12.ca.us/information',
		'https://chs.ceres.k12.ca.us/information/parent_info',
		'https://chs.ceres.k12.ca.us/information/parent_info/tips',
		'https://chs.ceres.k12.ca.us/information/parent_info/our_community',
		'https://chs.ceres.k12.ca.us/information/parent_info/ClassRings',
		'https://chs.ceres.k12.ca.us/information/parent_info/yearbookordercenter',
		'https://chs.ceres.k12.ca.us/information/parent_info/technology_resources',
		'https://chs.ceres.k12.ca.us/information/administration',
		'https://chs.ceres.k12.ca.us/information/student_handbook',
		'https://chs.ceres.k12.ca.us/information/menus',
		'https://chs.ceres.k12.ca.us/information/williams_complaint_form',
		'https://chs.ceres.k12.ca.us/information/policies_and_procedures',
		'https://chs.ceres.k12.ca.us/information/dress_code',
		'https://chs.ceres.k12.ca.us/information/technology_use_policy',
		'https://chs.ceres.k12.ca.us/information/guest_passes',
		'https://chs.ceres.k12.ca.us/information/attendance_procedures',
		'https://chs.ceres.k12.ca.us/information/course_catalog',
		'https://chs.ceres.k12.ca.us/information/important_numbers',
		'https://chs.ceres.k12.ca.us/information/williams_u_c_p_classroom_posting',
		'https://chs.ceres.k12.ca.us/information/CHSMap',
		'https://chs.ceres.k12.ca.us/information/bulldog_block_information',
		'https://chs.ceres.k12.ca.us/information/ceres_high_webstore',
		'https://chs.ceres.k12.ca.us/information/bell_schedule',
		'https://chs.ceres.k12.ca.us/academics',
		'https://chs.ceres.k12.ca.us/academics/career_technical_education',
		'https://chs.ceres.k12.ca.us/academics/career_technical_education/c_h_s_f_f_a_homepage',
		'https://chs.ceres.k12.ca.us/academics/math',
		'https://chs.ceres.k12.ca.us/academics/modern_language',
		'https://chs.ceres.k12.ca.us/academics/performing_arts',
		'https://chs.ceres.k12.ca.us/academics/p_e__dance',
		'https://chs.ceres.k12.ca.us/academics/science',
		'https://chs.ceres.k12.ca.us/academics/social_studies',
		'https://chs.ceres.k12.ca.us/academics/special_education',
		'https://chs.ceres.k12.ca.us/academics/ap_class_syllabi_and_summer_assignments',
		'https://chs.ceres.k12.ca.us/academics/library',
		'https://chs.ceres.k12.ca.us/academics/tutoring_schedule_2021-2022',
		'https://chs.ceres.k12.ca.us/academics/22CourseCatalog',
		'https://chs.ceres.k12.ca.us/guidance',
		'https://chs.ceres.k12.ca.us/guidance/state_standards',
		'https://chs.ceres.k12.ca.us/guidance/CHSCourseCatalog',
		'https://chs.ceres.k12.ca.us/guidance/c_u_s_d_college_awareness',
		'https://chs.ceres.k12.ca.us/guidance/learning_directors',
		'https://chs.ceres.k12.ca.us/guidance/learning_directors/ceres_high_school_counseling___guidance_website',
		'https://chs.ceres.k12.ca.us/guidance/learning_directors/learning_director_newsletter',
		'https://chs.ceres.k12.ca.us/guidance/student_support_specialist_webpage',
		'https://chs.ceres.k12.ca.us/guidance/transcript_request',
		'https://chs.ceres.k12.ca.us/guidance/a_b_104',
		'https://chs.ceres.k12.ca.us/school_facts',
		'https://chs.ceres.k12.ca.us/district_main',
	]
	mainfolder = 'ceres'
	school_name = 'ceres_chs'
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
				t1 = tiers[-6].capitalize()
				t2 = tiers[-5].capitalize()
				t3 = tiers[-4].capitalize()
				t4 = tiers[-3].capitalize()
				t5 = tiers[-2].capitalize()
				t6 = tiers[-1].capitalize()
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
