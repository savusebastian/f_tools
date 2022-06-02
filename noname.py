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

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='wh-content') != None and web_soup.find(class_='wh-content') != '':
			col1 = web_soup.find(class_='wh-content')
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
		'https://www.gpusd.org',
'https://www.gpusd.org/district',
'https://www.gpusd.org/district/about-us',
'https://www.gpusd.org/district/calendars',
'https://www.gpusd.org/district/contact-us',
'https://www.gpusd.org/district/district-school-boundaries-map',
'https://www.gpusd.org/district/lcap-local-control-accountability-plan',
'https://www.gpusd.org/school-accountability-report-card-sarc',
'https://www.gpusd.org/district/superintendents-message',
'https://www.gpusd.org/school-board',
'https://www.gpusd.org/past-board-agendas-and-minutes',
'https://www.gpusd.org/board-meetings',
'https://www.gpusd.org/board-members',
'https://www.gamutonline.net/district/goldenplains/',
'https://www.gpusd.org/trustee-area-maps',
'https://www.gpusd.org/board-meetings-special-announcements',
'https://www.gpusd.org/schools',
'https://sites.google.com/gpusd.org/cantua-elementary/home',
'https://drive.google.com/file/d/1cg2UDDaUjJeezQ42lRePSZmgo43_qKvq/view?usp=sharing',
'https://helm.gpusd.net/',
'https://drive.google.com/file/d/1yj3Pxg15NZVaBV2SO-o4jx7TC6FRf2Ub/view?usp=sharing',
'https://rdr.gpusd.net',
'https://sjes.gpusd.net',
'https://drive.google.com/file/d/1WG76iUVv0wW6tydaNAzXykA7KND2rHBT/view?usp=sharing',
'https://tes.gpusd.net',
'https://drive.google.com/file/d/15hfcpmoUZmqJZOZ1xUvapQOQdEzvzE5z/view?usp=sharing',
'https://ths.gpusd.net',
'https://drive.google.com/file/d/1uKp-bxaKPyqFH-cDIfcfW-C6WKeAC6o7/view?usp=sharing',
'https://www.gpusd.org/department-services',
'https://www.gpusd.org/department-services/academic-services',
'https://sites.google.com/gpusd.org/cantua-elementary/adult-education',
'https://www.gpusd.org/department-services/business-services',
'https://www.gpusd.org/department-services/business-services/post-3663',
'https://www.gpusd.org/department-services/food-services',
'https://drive.google.com/file/d/1UCpJDiOihyTGAESC6adPRitwgNorpabc/view?usp=sharing',
'https://www.gpusd.org/department-services/human-resources',
'https://www.gpusd.org/covid-19-information',
'https://www.gpusd.org/department-services/maintenance-operations-and-transportation',
'https://www.gpusd.org/department-services/special-education',
'https://www.gpusd.org/department-services/technology',
'https://www.gpusd.org/parentsquare',
'https://app.mytechdesk.org/signin',
'https://www.gpusd.org/department-services-technology-technology-resources',
'https://www.gpusd.org/department-services/superintendents-office',
'https://www.gpusd.org/resources',
'https://www.gpusd.org/anti-bullying-resources',
'https://www.gpusd.org/resources/for-parents',
'https://www.gpusd.org/resources/for-students',
'https://www.gpusd.org/resources/for-staff',
'https://www.gpusd.org/resources/policies-form',
'https://www.gpusd.org/contact',
		
'https://www.gpusd.net/',
'https://helm.gpusd.net/about/',
'https://helm.gpusd.net/about/principals-message/',
'https://helm.gpusd.net/about/mission-statement/',
'https://helm.gpusd.net/about/staff-directory/',
'https://helm.gpusd.net/about/links/',
'https://helm.gpusd.net/academics/',
'https://helm.gpusd.net/academics/teacher-pages/',
'https://helm.gpusd.net/academics/grade-levels/',
'https://helm.gpusd.net/academics/counselors-corner/',
'https://helm.gpusd.net/academics/library-media-center/',
'https://helm.gpusd.net/academics/after-school-program/',
'https://helm.gpusd.net/students/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://helm.gpusd.net/students/classes-assignments/',
'https://helm.gpusd.net/students/student-handbook/',
'https://helm.gpusd.net/students/school-policies/',
'https://helm.gpusd.net/students/clubs-and-activities/',
'https://helm.gpusd.net/students/resources-quick-links/',
'https://helm.gpusd.net/parents/',
'https://helm.gpusd.net/parents/school-calendar/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://helm.gpusd.net/parents/newsletter/',
'https://helm.gpusd.net/parents/parent-resources/',
'https://goldenplainsusd.asp.aeries.net/air/Default.aspx',
'https://helm.gpusd.net/contact/',
'https://www.gpusd.net/',
'https://rdr.gpusd.net/about/',
'https://rdr.gpusd.net/about/principals-message/',
'https://rdr.gpusd.net/about/mission-statement/',
'https://rdr.gpusd.net/about/staff-directory/',
'https://rdr.gpusd.net/about/links/',
'https://rdr.gpusd.net/academics/',
'https://rdr.gpusd.net/academics/teacher-pages/',
'https://rdr.gpusd.net/academics/grade-levels/',
'https://rdr.gpusd.net/academics/counselors-corner/',
'https://rdr.gpusd.net/academics/library-media-center/',
'https://rdr.gpusd.net/academics/after-school-program/',
'https://rdr.gpusd.net/students/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://rdr.gpusd.net/students/classes-assignments/',
'https://rdr.gpusd.net/students/student-handbook/',
'https://rdr.gpusd.net/students/school-policies/',
'https://rdr.gpusd.net/students/clubs-and-activities/',
'https://rdr.gpusd.net/students/resources-quick-links/',
'https://rdr.gpusd.net/parents/',
'https://rdr.gpusd.net/parents/school-calendar/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://rdr.gpusd.net/parents/newsletter/',
'https://rdr.gpusd.net/parents/parent-resources/',
'https://goldenplainsusd.asp.aeries.net/air/Default.aspx',
'https://rdr.gpusd.net/contact/',
'https://www.gpusd.org/',
'https://sjes.gpusd.net/school-info/',
'https://sjes.gpusd.net/school-info/school-profile/',
'https://sjes.gpusd.net/principals-message/',
'https://sjes.gpusd.net/school-calendar/" class="sf-with-ul',
'https://www.gpusd.org/wp-content/uploads/2020/06/2020-2021-District-Calendar.pdf?x84156',
'https://sjes.gpusd.net/school-info/mission-statement/',
'https://sjes.gpusd.net/school-info/staff-directory/',
'https://sjes.gpusd.net/school-info/student-handbook/',
'https://www.gpusd.org/school-accountability-report-card-sarc',
'https://sjes.gpusd.net/staff/',
'https://goldenplainsusd.asp.aeries.net/Admin/Login.aspx',
'https://goldenplainsusd.asp.aeries.net/Teacher/Login.aspx',
'https://sjes.gpusd.net/staff/resources/',
'https://sjes.gpusd.net/students/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://sjes.gpusd.net/students/clubs-activities/',
'https://sjes.gpusd.net/students/counselors-corner/',
'https://sjes.gpusd.net/students/library-media-center/',
'https://sjes.gpusd.net/students/after-school-program/" class="sf-with-ul',
'https://sjes.gpusd.net/students/after-school-program/program-report-card/',
'https://sjes.gpusd.net/parents/',
'https://sjes.gpusd.net/wp-content/uploads/2018/02/Monthly-Calendar-for-October-2017.pdf',
'https://sjes.gpusd.net/parents/parent-resources/',
'https://goldenplainsusd.asp.aeries.net/air/Default.aspx',
'https://goldenplainsusd.asp.aeries.net/',
'https://sjes.gpusd.net/programs/',
'https://sjes.gpusd.net/programs-seal/',
'https://sjes.gpusd.net/programs-erwc/',
'https://sjes.gpusd.net/programs-dual-immersion/',
'https://sjes.gpusd.net/project-glad/',
'https://sjes.gpusd.net/contact/',
'https://www.gpusd.net/',
'https://tes.gpusd.net/our-school/',
'https://tes.gpusd.net/our-school/principals-message/',
'https://tes.gpusd.net/our-school/mission-statement/',
'https://tes.gpusd.net/our-school/staff-directory/',
'https://tes.gpusd.net/academics/resources/',
'https://tes.gpusd.net/academics/',
'https://tes.gpusd.net/academics/teacher-pages/',
'https://tes.gpusd.net/academics/counselors-corner/',
'https://tes.gpusd.net/academics/library-media-center/',
'https://tes.gpusd.net/academics/after-school-program/',
'https://tes.gpusd.net/students/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://tes.gpusd.net/students/student-handbook/',
'https://tes.gpusd.net/students/school-policies/',
'https://tes.gpusd.net/students/clubs-and-activities/',
'https://tes.gpusd.net/students/resources-quick-links/',
'https://tes.gpusd.net/parents/',
'https://tes.gpusd.net/our-school/school-calendar/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://tes.gpusd.net/parents/newsletter/',
'https://tes.gpusd.net/parents/parent-resource/',
'https://goldenplainsusd.asp.aeries.net/air/Default.aspx',
'https://tes.gpusd.net/contact/',
'https://www.gpusd.net/',
'https://ths.gpusd.net/about/',
'https://ths.gpusd.net/about/principals-message/',
'https://ths.gpusd.net/about/mission-statement/',
'https://ths.gpusd.net/about/staff-directory/',
'https://ths.gpusd.net/about/5240-2/',
'https://ths.gpusd.net/about/links/',
'https://ths.gpusd.net/academics/',
'https://ths.gpusd.net/academics/counseling-department/',
'https://all4youth.fcoe.org/covid-19-community-resources',
'https://ths.gpusd.net/cal-soap-services-english-version/',
'https://ths.gpusd.net/academics/counseling-department/work-permits/',
'https://ths.gpusd.net/academics/class-descriptions/',
'https://ths.gpusd.net/academics/class-descriptions/agriculture-department/',
'https://ths.gpusd.net/academics/class-descriptions/career-technical-education/',
'https://ths.gpusd.net/academics/class-descriptions/electives/',
'https://ths.gpusd.net/academics/class-descriptions/english-language-arts/',
'https://ths.gpusd.net/academics/class-descriptions/foreign-languages/',
'https://ths.gpusd.net/academics/class-descriptions/mathematics-department/',
'https://ths.gpusd.net/academics/class-descriptions/physical-education-department/',
'https://ths.gpusd.net/academics/class-descriptions/science-department/',
'https://ths.gpusd.net/academics/class-descriptions/social-sciences-department/',
'https://ths.gpusd.net/academics/class-descriptions/special-education-services/',
'https://ths.gpusd.net/academics/career-pathways-cte/',
'https://ths.gpusd.net/dual-enrollment/',
'https://ths.gpusd.net/academics/after-school-program/',
'https://ths.gpusd.net/students/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://ths.gpusd.net/category/school-life/',
'https://ths.gpusd.net/students/daily-life/',
'https://ths.gpusd.net/about/ths-activities-calendar/',
'https://ths.gpusd.net/students/clubs-and-activities/',
'https://ths.gpusd.net/students/clubs-and-activities/a-v-i-d/',
'https://ths.gpusd.net/students/clubs-and-activities/culture-club/',
'https://ths.gpusd.net/students/clubs-and-activities/csf-club/',
'https://ths.gpusd.net/students/clubs-and-activities/m-e-ch-a/',
'https://ths.gpusd.net/students/clubs-and-activities/mock-trial/',
'https://ths.gpusd.net/students/clubs-and-activities/spanish-club/',
'https://ths.gpusd.net/students/clubs-and-activities/tranquillity-car-club/',
'https://ths.gpusd.net/academics/career-pathways-cte/',
'https://ths.gpusd.net/dual-enrollment/',
'https://sites.google.com/gpusd.org/thssports',
'https://ths.gpusd.net/wp-content/uploads/2018/08/THS-2018-2019-Parents-HandBook.pdf',
'https://ths.gpusd.net/transcript-requests/',
'https://ths.gpusd.net/parents/',
'https://ths.gpusd.net/about/ths-activities-calendar/',
'https://goldenplainsusd.asp.aeries.net/Student/LoginParent.aspx?page=default.aspx',
'https://ths.gpusd.net/parents/parent-resources/',
'https://ths.gpusd.net/parents/online-registration-and-enrollment/',
'https://ths.gpusd.net/contact/',
	]
	mainfolder = 'gpusd'
	school_name = 'gpusd'
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
