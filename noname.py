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
		if web_soup.find(class_='l-main-page-content-inner') != None and web_soup.find(class_='l-main-page-content-inner') != '':
			col1 = web_soup.find(class_='l-main-page-content-inner')
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
		'https://www.smfcsd.net/en/about-smfcsd/about-smfcsd.html',
'https://www.smfcsd.net/en/about-smfcsd/superintendent/local-control-accountability-plan-lcap.html',
'https://www.smfcsd.net/en/about-smfcsd/superintendent/superintendents-welcome.html',
'https://www.smfcsd.net/en/our-district/smfcsd-strategic-plan.html',
'https://www.smfcsd.net/en/our-district/district-departments/',
'https://www.smfcsd.net/en/news/community-programs.html',
'https://www.smfcsd.net/en/news/onesmfc-podcast.html',
'https://www.smfcsd.net/en/news/newsletter/',
'https://www.smfcsd.net/en/calendar/district-calendar.html',
'https://docs.google.com/document/d/1RxG_NwFUYTizbCXJAAi5uZq8IAeNL2yeVcwdyNECsqA/edit?usp=sharing',
'https://docs.google.com/document/d/1cp4gQs_D7MpXAsJnG_DZsVPJSpp_-dtZ9Tdd0xVdh1o/edit?usp=sharing',
'https://docs.google.com/document/d/1w68ygMt8lMWkaz_JagA7G3P3QL4MwNPCMlFeYUx8d0c/edit?usp=sharing',
'https://www.smfcsd.net/en/special-education/special-education.html',
'https://www.smfcsd.net/en/special-education/sedac-special-education-district-advisory-committee.html',
'https://docs.google.com/document/d/1H6E6ZUDi9WSSMTiouP5mxRRMIYBhTfwueY08OxxDDU4/edit?usp=sharing',
'https://www.smfcsd.net/en/parent-reference/wellness/california-healthy-kids-survey-(chks).html',
'https://www.smfcsd.net/en/parent-reference/wellness/tobacco-use-prevention-(tupe).html',
'https://docs.google.com/document/d/1IUwbVuC8KtWtjKGXs5sJR9PPIZmGhZkSMBLkNNBrYTk/edit?usp=sharing',
'https://www.smfcsd.net/en/parent-reference/wellness/wellness-program.html',
'https://www.smfcsd.net/en/parent-reference/wellness/wellness-resources.html',
'https://www.smfcsd.net/en/parent-reference/wellness/wellness-parent-education.html',
'https://www.smfcsd.net/en/parent-reference/wellness/wellness-newsletters.html',
'https://www.smfcsd.net/en/parent-reference/wellness/snack-guide.html',
'https://www.smfcsd.net/en/parent-reference/authorizations-for-2020-2021.html',
'https://www.smfcsd.net/en/nutrition-and-school-meals/breakfast-and-lunch-info-2021-22.html',
'https://www.smfcsd.net/en/nutrition-and-school-meals/free-reduced-price-meals.html',
'https://www.smfcsd.net/en/nutrition-and-school-meals/nutrition-info.html',
'https://www.smfcsd.net/en/nutrition-and-school-meals/menu.html',
'https://www.smfcsd.net/en/our-district/district-departments/technology-department.html',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/fiscal-services-department/overview.html',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/fiscal-services-department/payroll-department.html',
'https://docs.google.com/document/d/1AlnqEa7NrBkbZqTS8nogWlP3heHDCktqirWzNef_ru4/edit?usp=sharing',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/facilities-and-constrution/bond-measures/',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/facilities-and-constrution/bond-measures/bond-oversight-committee.html',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/facilities-and-constrution/bond-measures/notice-to-contractors.html',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/facilities-and-constrution/bond-measures/upcoming-construction-projects.html',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/facilities-and-constrution/bond-measures/measure-x-and-t-projects.html',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/maintenance-operations-and-transportation/m-o-t-overview.html',
'https://www.smfcsd.net/en/our-district/district-departments/business-services/maintenance-operations-and-transportation/civic-permits-and-facilities-usage.html',
'https://docs.google.com/document/d/1_an9iLfCRs7bLNuXgfv5hTexMRVInodkcRjUtYBa2ws/edit?usp=sharing',
'https://docs.google.com/document/d/1BwNK8-wFL0B88YA6ksHpdpCKv-R4VNm-ybQf3q-FCSc/edit?usp=sharing',
'https://www.smfcsd.net/en/board-of-trustees/board-of-trustees.html',
'https://www.smfcsd.net/en/board-of-trustees/board-meeting-agendas-minutes-and-summaries.html',
'https://www.smfcsd.net/en/board-of-trustees/board-of-trustees-%E2%80%93-members.html',
'https://www.smfcsd.net/en/board-of-trustees/smfc-adopts-by-trustee-areas.html',
'https://www.smfcsd.net/en/board-of-trustees/public-records.html',
'https://www.smfcsd.net/en/enrollment-student-registration/how-to-register-for-the-2022-2023-school-year.html',
'https://www.smfcsd.net/en/enrollment-student-registration/school-assignments.html',
'https://www.smfcsd.net/en/enrollment-student-registration/transfers-and-school-choice.html',
'https://www.smfcsd.net/en/enrollment-student-registration/interdistrict-transfer-requests.html',
'https://www.smfcsd.net/en/enrollment-student-registration/faqs-school-choice.html',
'https://www.smfcsd.net/en/enrollment-student-registration/6th-grade-re-registration-for-current-5th-grade-students.html',
'https://www.smfcsd.net/en/enrollment-student-registration/registration-information-for-the-new-elementary-school-in-foster-city-2020-2021.html',
'https://www.smfcsd.net/en/schools-and-preschool-programs/what-is-a-magnet-school.html',
'https://www.smfcsd.net/en/news/archives/news-2021-2022/footsteps2brilliance.html',
'https://www.smfcsd.net/en/news/archives/news-2021-2022/st-math.html',
	]
	mainfolder = 'smfcsd'
	school_name = 'district'
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
