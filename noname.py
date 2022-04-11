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

		if web_soup.find(id='content_area').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='content_area').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='content_area').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='content_area').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='content_area').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='content_area').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='content_area') != None and web_soup.find(id='content_area') != '':
			col1 = web_soup.find(id='content_area')
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
		'https://www.lbschools.net/Departments/Business_Services/financial_documents.cfm',
		'https://www.lbschools.net/Departments/Business_Services/financial_documents_arc.cfm',
		'https://www.lbschools.net/Departments/Business_Services/accounting.cfm',
		'https://www.lbschools.net/Departments/Business_Services/payroll.cfm',
		'https://www.lbschools.net/Departments/Human_Resource_Services/',
		'https://www.lbschools.net/Departments/Personnel_Commission/',
		'https://www.lbschools.net/Departments/Local_Control/',
		'https://www.lbschools.net/Departments/Linked_Learning/index.cfm',
		'https://www.lbschools.net/Departments/Linked_Learning/pathways.cfm',
		'https://www.lbschools.net/Departments/Superintendent/index.cfm',
		'https://www.lbschools.net/Departments/Superintendent/goals.cfm',
		'https://www.lbschools.net/Departments/Superintendent/student-advisory-committee.cfm',
		'https://www.lbschools.net/Departments/Superintendent/supt-parent-connection.cfm',
		'https://www.lbschools.net/Departments/Superintendent/learning-acceleration-plan.cfm',
		'https://www.lbschools.net/Departments/Elementary_Schools/school_finder.cfm',
		'https://www.lbschools.net/Schools/calendars.cfm',
		'https://www.lbschools.net/Schools/sarcs.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/index.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/meal_app.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/menu_nutrient_info.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/special_diets.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/fitness.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/summer_programs.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/job_opps.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/staff_resources.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/vendor_resources.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/about.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/contact.cfm',
		'https://www.lbschools.net/Departments/Nutrition_Services/Bids/',
		'https://www.lbschools.net/Departments/Research/',
		'https://www.lbschools.net/Departments/Research/test_schedules.cfm',
		'https://www.lbschools.net/Departments/Research/Testing/state-wide.cfm',
		'https://www.lbschools.net/Departments/Research/Testing/prep-placement.cfm',
		'https://www.lbschools.net/Departments/Research/Accountability/state_account.cfm',
		'https://www.lbschools.net/Departments/Research/Accountability/federal_account.cfm',
		'https://www.lbschools.net/Departments/Research/parent_vue.cfm',
		'https://www.lbschools.net/Departments/Research/student_data.cfm',
		'https://www.lbschools.net/Departments/Research/Data/core_survey.cfm',
		'https://www.lbschools.net/Departments/Research/Data/sarc.cfm',
		'https://www.lbschools.net/Departments/Research/school-messenger.cfm',
		'https://www.lbschools.net/Departments/EEP/',
		'https://www.lbschools.net/Departments/Parent_U/',
		'https://www.lbschools.net/Departments/Parent_U/parent_workshops.cfm',
		'https://www.lbschools.net/Departments/Parent_U/enrollment.cfm',
		'https://www.lbschools.net/Departments/Parent_U/guidelines.cfm',
		'https://www.lbschools.net/Departments/Parent_U/online_resources.cfm',
		'https://www.lbschools.net/Departments/EEP/native_americans.cfm',
		'https://www.lbschools.net/Departments/EEP/translation-unit.cfm',
		'https://www.lbschools.net/Departments/EEP/college_aides.cfm',
		'https://www.lbschools.net/Departments/Education_Foundation/index.cfm',
		'https://www.lbschools.net/Departments/Education_Foundation/programs.cfm',
		'https://www.lbschools.net/Departments/High_Schools/index.cfm',
		'https://www.lbschools.net/Departments/High_Schools/hs_list.cfm',
		'https://www.lbschools.net/Departments/School_Choice/hs_choice.cfm',
		'https://www.lbschools.net/Departments/Counseling/index.cfm',
		'https://www.lbschools.net/Departments/Counseling/transcripts_current.cfm',
		'https://www.lbschools.net/Departments/Counseling/counseling_modules.cfm',
		'https://www.lbschools.net/Departments/Counseling/grad_requirements.cfm',
		'https://www.lbschools.net/Departments/Counseling/scholar.cfm',
		'https://www.lbschools.net/Departments/Records_Management/',
		'https://www.lbschools.net/Departments/Middle_K8_Schools/index.cfm',
		'https://www.lbschools.net/Departments/Middle_K8_Schools/school_choice.cfm',
		'https://www.lbschools.net/Departments/Middle_K8_Schools/sports.cfm',
		'https://www.lbschools.net/Departments/Middle_K8_Schools/school_finder.cfm',
		'https://www.lbschools.net/Departments/Curriculum/CTE/',
		'https://www.lbschools.net/Departments/Curriculum/CTE/standards.cfm',
		'https://www.lbschools.net/Departments/Curriculum/CTE/ctso.cfm',
		'https://www.lbschools.net/Departments/Curriculum/CTE/teacher_resources.cfm',
	]
	mainfolder = 'lbschools'
	school_name = 'lbschools'
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
