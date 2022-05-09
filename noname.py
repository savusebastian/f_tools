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

		if web_soup.find(class_='grid-section').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='grid-section').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='grid-section').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='grid-section').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='grid-section').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='grid-section').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='grid-section') != None and web_soup.find(class_='grid-section') != '':
			col1 = web_soup.find(class_='grid-section')
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
		'https://www.compton.k12.ca.us/district/about-us/about-us',
'https://www.compton.k12.ca.us/lcap',
'https://www.compton.k12.ca.us/district/about-us/doing-business',
'https://www.compton.k12.ca.us/district/about-us/instructional-calendars',
'https://www.compton.k12.ca.us/departments/human-resources/non-discrimination/english',
'https://www.compton.k12.ca.us/departments/human-resources/non-discrimination/spanish',
'https://www.compton.k12.ca.us/district/contacts/executive-directors',
'https://www.compton.k12.ca.us/district/contacts/directors',
'https://www.compton.k12.ca.us/district/contacts/contacts',
'https://www.compton.k12.ca.us/district/contacts/other-contacts',
'https://www.compton.k12.ca.us/district/administration/administration',
'https://www.compton.k12.ca.us/district/contacts/administrators',
'https://www.compton.k12.ca.us/district/contacts/senior-directors',
'https://www.compton.k12.ca.us/district/administration/superintendent',
'https://www.compton.k12.ca.us/district/administration/executive-cabinet',
'https://www.compton.k12.ca.us/district/enrollment/registration',
'https://www.compton.k12.ca.us/district/about-us/common-core',
'https://www.compton.k12.ca.us/district/headline-feed-ii/announcements-events',
'https://www.compton.k12.ca.us/district/reopeningfaqs/reopening-faqs',
'https://www.compton.k12.ca.us/district/parents',
'https://www.compton.k12.ca.us/district/students',
'https://www.compton.k12.ca.us/district/staff',
'https://www.compton.k12.ca.us/news-release/news/2020/august/reopen-protocols',
'https://www.compton.k12.ca.us/board/members/micah-ali',
'https://www.compton.k12.ca.us/board/members/members',
'https://www.compton.k12.ca.us/board/members/satra-zurita',
'https://www.compton.k12.ca.us/board/members/charles-davis',
'https://www.compton.k12.ca.us/board/members/alma-pleasant',
'https://www.compton.k12.ca.us/board/members/mae-thomas',
'https://www.compton.k12.ca.us/board/members/lowanda-green',
'https://www.compton.k12.ca.us/board/members/sandra-moss',
'https://www.compton.k12.ca.us/board/meeting-schedule',
'https://www.compton.k12.ca.us/board/agendas-and-minutes/current-year',
'https://www.compton.k12.ca.us/departments/business-services/home',
'https://www.compton.k12.ca.us/departments/business-services/facilities/home',
'https://www.compton.k12.ca.us/departments/business-services/facilities/team',
'https://www.compton.k12.ca.us/departments/business-services/facilities/energy-management/energy-management',
'https://www.compton.k12.ca.us/departments/business-services/facilities/pre-qualification',
'https://www.compton.k12.ca.us/departments/business-services/facilities/measure-s-webpage/home',
'https://www.compton.k12.ca.us/departments/business-services/facilities/measure-s-webpage/cboc-community-page',
'https://www.compton.k12.ca.us/departments/business-services/facilities/measure-s-webpage/resolution',
'https://www.compton.k12.ca.us/departments/business-services/financial-information',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/home',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/staff',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/documents-and-forms',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/carpenter-shop/home',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/lock-shop/home',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/paint-shop/paint-shop',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/electrical/home',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/welding-and-fencing/home',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/hvac/home',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/ground-department/ground-department',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/irrigation/home',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/documents-and-forms',
'https://www.compton.k12.ca.us/departments/business-services/maintenance-and-operations/pest-management/home',
'https://www.compton.k12.ca.us/departments/business-services/payroll-and-risk-management/home',
'https://www.compton.k12.ca.us/departments/business-services/purchasing-and-contracts/staff',
'https://www.compton.k12.ca.us/departments/business-services/purchasing-and-contracts/bulletins',
'https://www.compton.k12.ca.us/departments/business-services/purchasing-and-contracts/forms-and-links',
'https://www.compton.k12.ca.us/departments/business-services/purchasing-and-contracts/jit-product-list',
'https://www.compton.k12.ca.us/departments/business-services/purchasing-and-contracts/home',
'https://www.compton.k12.ca.us/departments/business-services/student-nutrition-services/home',
'https://www.compton.k12.ca.us/departments/business-services/student-nutrition-services/nondiscrimination-statement',
'https://www.compton.k12.ca.us/departments/business-services/student-nutrition-services/menus',
'https://www.compton.k12.ca.us/departments/business-services/transportation/home',
'https://www.compton.k12.ca.us/departments/business-services/transportation/staff',
'https://www.compton.k12.ca.us/departments/business-services/warehouse/home',
'https://www.compton.k12.ca.us/departments/business-services/warehouse/staff',
'https://www.compton.k12.ca.us/departments/business-services/warehouse/forms',
'https://www.compton.k12.ca.us/departments/business-services/fiscal-services/home',
'https://www.compton.k12.ca.us/departments/business-services/fiscal-services/staff',
'https://www.compton.k12.ca.us/departments/educational-services/ases/ases-home',
'https://www.compton.k12.ca.us/departments/educational-services/ases/ases-pbis-brochure',
'https://www.compton.k12.ca.us/departments/educational-services/ases/student-sign-inout-policy',
'https://www.compton.k12.ca.us/departments/educational-services/ases/organization-chart',
'https://www.compton.k12.ca.us/departments/educational-services/ases/ases-policy',
'https://www.compton.k12.ca.us/departments/educational-services/ases/ases-school-websites',
'https://www.compton.k12.ca.us/departments/educational-services/ases/resource-links',
'https://www.compton.k12.ca.us/departments/educational-services/ases/contact-information',
'https://www.compton.k12.ca.us/departments/educational-services/black-student-achievement/home',
'https://www.compton.k12.ca.us/departments/educational-services/career-technical-education/career-technical-education',
'https://www.compton.k12.ca.us/departments/educational-services/college-and-career/home',
'https://www.compton.k12.ca.us/departments/educational-services/early-childhood-education/home',
'https://www.compton.k12.ca.us/departments/educational-services/early-childhood-education/distant-learning-staff-contact-information/distant-learning',
'https://www.compton.k12.ca.us/departments/educational-technology/home',
'https://www.compton.k12.ca.us/departments/educational-services/prek-12-education-services/home',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/tips',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/mission',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/vision',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/grievance-policies-procedures',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/teach-out-plan',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/requirements',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/program-calendar',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/candidates-journey',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/mentors',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/site-administrators',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/resources',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/technical-support',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/contacts',
'https://www.compton.k12.ca.us/departments/educational-services/tips-induction-program/slideshows',
'https://www.compton.k12.ca.us/departments/educational-services/research-evaluation/home',
'https://www.compton.k12.ca.us/departments/educational-services/special-projects/home',
'https://www.compton.k12.ca.us/departments/educational-services/special-projects/categorical-programs',
'https://www.compton.k12.ca.us/departments/educational-services/special-projects/school-site-council-forms',
'https://www.compton.k12.ca.us/departments/educational-services/special-projects/parent-center',
'https://www.compton.k12.ca.us/departments/educational-services/special-projects/volunteer-information',
'https://www.compton.k12.ca.us/departments/educational-services/special-projects/federal-program-monitoring-fpm',
'https://www.compton.k12.ca.us/departments/educational-services/special-projects/categorical-forms',
'https://www.compton.k12.ca.us/departments/educational-services/career-technical-education/career-technical-education',
'https://www.compton.k12.ca.us/departments/educational-services/career-technical-education/staff',
'https://www.compton.k12.ca.us/departments/educational-services/career-technical-education/cte-esports',
'https://www.compton.k12.ca.us/departments/educational-services/prek-12-education-services/our-staff',
'https://www.compton.k12.ca.us/departments/educational-services/career-technical-education/industry-sectors',
'https://www.compton.k12.ca.us/athletics',
'https://www.compton.k12.ca.us/departments/educational-services/prek-12-education-services/textbook-services',
'https://www.compton.k12.ca.us/departments/human-resources/home',
'https://www.compton.k12.ca.us/departments/human-resources/staff',
'https://www.compton.k12.ca.us/departments/human-resources/credential-information',
'https://www.compton.k12.ca.us/departments/human-resources/non-discrimination/english',
'https://www.compton.k12.ca.us/departments/human-resources/non-discrimination/spanish',
'https://www.compton.k12.ca.us/departments/human-resources/uniform-complaint-procedure/ucp',
'https://www.compton.k12.ca.us/departments/human-resources/salary-and-benefits',
'https://www.compton.k12.ca.us/departments/human-resources/families-first-coronavirus-response-act',
'https://www.compton.k12.ca.us/departments/human-resources/uniform-complaint-procedure/uniform-complaint-procedures-annual-notice-and-documents',
'https://www.compton.k12.ca.us/departments/human-resources/annual-notifications',
'https://www.compton.k12.ca.us/departments/human-resources/cusd-policies-2020-2021',
'https://www.compton.k12.ca.us/departments/human-resources/for-current-employees',
'https://www.compton.k12.ca.us/departments/human-resources/community-information',
'https://www.compton.k12.ca.us/departments/human-resources/employment-opportunities',
'https://www.compton.k12.ca.us/departments/human-resources/substitute-information',
'https://www.compton.k12.ca.us/departments/human-resources/credential-information',
'https://www.compton.k12.ca.us/departments/human-resources/bargaining-union-agreements',
'https://www.compton.k12.ca.us/departments/human-resources/job-descriptions',
'https://www.compton.k12.ca.us/departments/information-technology/home',
'https://www.compton.k12.ca.us/techsupport',
'https://www.compton.k12.ca.us/departments/information-technology/our-staff',
'https://www.compton.k12.ca.us/departments/personnel-commission/home',
'https://www.compton.k12.ca.us/departments/personnel-commission/staff',
'https://www.compton.k12.ca.us/departments/personnel-commission/agendas-and-minutes/current-year',
'https://www.compton.k12.ca.us/departments/personnel-commission/union-bargaining-agreements',
'https://www.compton.k12.ca.us/departments/personnel-commission/for-current-employees',
'https://www.compton.k12.ca.us/departments/personnel-commission/salary-schedules-21-22',
'https://www.compton.k12.ca.us/departments/personnel-commission/frequently-asked-questions',
'https://www.compton.k12.ca.us/departments/personnel-commission/annual-reports',
'https://www.compton.k12.ca.us/departments/personnel-commission/commissioner-members',
'https://www.compton.k12.ca.us/departments/school-police/home',
'https://www.compton.k12.ca.us/departments/school-police/chiefs-message',
'https://www.compton.k12.ca.us/departments/school-police/code-of-ethics',
'https://www.compton.k12.ca.us/departments/school-police/commendations',
'https://www.compton.k12.ca.us/departments/school-police/recognition',
'https://www.compton.k12.ca.us/departments/school-police/safety-resources',
'https://www.compton.k12.ca.us/departments/pupil-services/home',
'https://www.compton.k12.ca.us/departments/pupil-services/staff',
'https://www.compton.k12.ca.us/departments/pupil-services/foster-youth-services',
'https://www.compton.k12.ca.us/departments/pupil-services/homeless-youth',
'https://www.compton.k12.ca.us/departments/pupil-services/registration',
'https://www.compton.k12.ca.us/departments/pupil-services/permits-and-transfer',
'https://www.compton.k12.ca.us/departments/pupil-services/attendance/attendance-home',
'https://www.compton.k12.ca.us/departments/pupil-services/bullying-page/district-bullying',
'https://www.compton.k12.ca.us/departments/communications/home',
'https://www.compton.k12.ca.us/departments/communications/staff',
'https://www.compton.k12.ca.us/departments/communications/electronic-forms',
'https://www.compton.k12.ca.us/departments/educational-services/special-education/home',
'https://www.compton.k12.ca.us/departments/educational-services/special-education/about-us',
'https://www.compton.k12.ca.us/departments/educational-services/special-education/sped-newsletters',
'https://www.compton.k12.ca.us/departments/educational-services/special-education/community-advisory-committee',
'https://www.compton.k12.ca.us/departments/educational-services/special-education/parent-resources',
'https://www.compton.k12.ca.us/departments/educational-services/special-education/downloads',
'https://www.compton.k12.ca.us/departments/educational-services/special-education/local-plans',
'https://www.compton.k12.ca.us/district/newcomptonhigh/new-compton-high',
'https://www.compton.k12.ca.us/district/summer2022/summer2022',
'https://www.compton.k12.ca.us/newchs',
'https://www.compton.k12.ca.us/district/classof2021/cusd-class-of-2021',
'https://www.compton.k12.ca.us/district/classof2022/cusd-class-of-2022-graduation',
'https://www.compton.k12.ca.us/district/classof2022/cusd-class-of-2022-graduation-spanish',
'https://www.compton.k12.ca.us/schools/high-schools',
'https://www.compton.k12.ca.us/schools/middle-school',
'https://www.compton.k12.ca.us/schools/elementary-school',
'https://www.compton.k12.ca.us/schools/adult-school',
'https://www.compton.k12.ca.us/schools/charter-school',
	]
	mainfolder = 'compton'
	school_name = 'compton'
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
