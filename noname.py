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

		if web_soup.find(class_='pages-left-column-wrapper').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='pages-left-column-wrapper').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='pages-left-column-wrapper').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='pages-left-column-wrapper').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='pages-left-column-wrapper').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='pages-left-column-wrapper').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='pages-left-column-wrapper') != None and web_soup.find(class_='pages-left-column-wrapper') != '':
			col1 = web_soup.find(class_='pages-left-column-wrapper')
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
		'http://www.stpsb.org/parents_intro.php',
		'http://www.stpsb.org/transportation/index.htm',
		'http://www.stpsb.org/parents_curriculum.php',
		'http://www.stpsb.org/../districthandbook/DistrictHandbook.pdf',
		'http://www.stpsb.org/PDFFiles/emergencyDLplan.pdf',
		'http://www.stpsb.org/parents_emergency.php',
		'http://www.stpsb.org/PDFFiles/ebb-infographic.pdf',
		'http://www.stpsb.org/childnutrition/childnutritionindex.htm',
		'http://www.stpsb.org/childnutrition/freeandreducedmenu.htm',
		'http://stpsb.org/files/graduationdates2022.pdf',
		'http://www.stpsb.org/graduationrates.php',
		'https://www.louisianabelieves.com/academics/graduation-requirements',
		'http://virtualacademy.stpsb.org/summer.html',
		'http://www.stpsb.org/../homeworkhelp.php',
		'http://www.stpsb.org/KIT/index.htm',
		'http://www.stpsb.org/forms/index.html',
		'http://www.stpsb.org/../prek/index.htm',
		'http://www.stpsb.org/PreservationPlaza/plazaindex.htm',
		'http://www.stpsb.org/../files/pupil_progressionplan.pdf',
		'http://www.stpsb.org/register/index.html',
		'http://www.stpsb.org/parents_resources.php',
		'http://www.stpsb.org/calendar.php',
		'http://www.stpsb.org/schools_directory.php',
		'http://www.stpsb.org/schoolfastfacts/schoolfastfacts.html',
		'http://www.stpsb.org/../StudentInsurance/index.htm',
		'http://www.stpsb.org/../SupplyLists/supplylistmenu.htm',
		'http://www.stpsb.org/file.php?file_id=10 target=_blank',
		'http://www.stpsb.org/../specialed/index.html',
		'http://www.stpsb.org/athletics_intro.php',
		'http://www.stpsb.org/parents_studentfees.php',
		'http://www.stpsb.org/../summerreading.html',
		'http://virtualacademy.stpsb.org/summer.html',
		'http://www.stpsb.org/coronavirus/techguides.html',

		'http://www.stpsb.org/students_intro.php',
		'http://northshorecollege.edu',
		'http://www.stpsb.org/otherpages/CareerTech/careerpathways.html',
		'http://www.stpsb.org/students_crimestoppers.php',
		'http://www.stpsb.org/../districthandbook/DistrictHandbook.pdf',
		'http://www.stpsb.org/PDFFiles/emergencyDLplan.pdf',
		'http://stpsb.org/files/graduationdates2022.pdf',
		'https://www.louisianabelieves.com/academics/graduation-requirements',
		'http://www.stpsb.org/../homeworkhelp.php',
		'http://www.stpsb.org/PreservationPlaza/plazaindex.htm',
		'http://www.stpsb.org/students_resources.php',
		'http://www.stpsb.org/calendar.php',
		'http://www.stpsb.org/files/schooluniformpolicy.pdf',
		'http://www.stpsb.org/athletics_intro.php',
		'http://stpsb.org/staracademy/index.htm',
		'http://www.stpsb.org/../summerreading.html',
		'http://virtualacademy.stpsb.org/summer.html',
		'http://www.stpsb.org/coronavirus/techguides.html',
		'http://www.laworks.net/ORS_teentext.asp',
		'https://www2.laworks.net/Downloads/WFD/MinorApplicationToEmployForm.pdf',

		'http://www.stpsb.org/schools_directory.php',
		'http://www.stpsb.org/calendar.php',
		'http://www.stpsb.org/file.php?file_id=26',
		'http://www.stpsb.org/accountability/StandardizedTestResults.htm',
		'http://www.stpsb.org/2019LetterGrades.html',
		'http://www.stpsb.org/../schoolfastfacts/schoolfastfacts.html',
		'http://www.stpsb.org/register/index.html',
		'http://www.stpsb.org/childnutrition/freeandreducedmenu.htm',
		'http://maps.stpsb.org',

		'http://www.stpsb.org/staff_intro.php',
		'https://moodle.stpsb.org',
		'http://www.stpsb.org/calendar.php',
		'http://www.stpsb.org/CollectiveBargaining/index.html',
		'http://www.stpsb.org/../Jobs/benefitinformation.htm',
		'http://www.stpsb.org/employeehandbook',
		'http://www.stpsb.org/Jobs/index.htm',
		'http://www.stpsb.org/Jobs/LegalDocuments/LegalDocumentsBinder.pdf',
		'http://stpsb.org/Ethics/ethicsindex.htm',
		'http://www.stpsb.org/schoolboard_policies2.php',
		'http://www.stpsb.org/PreservationPlaza/plazaindex.htm',
		'http://www.stpsb.org/file.php?file_id=8',
		'http://www.stpsb.org/staff_resources.php',
		'http://www.stpsb.org/staff_salary.php',
		'http://www.stpsb.org/../athletics_intro.php',
		'http://www.stpsb.org/../Personnel/StudentTeacherInternPolicyHandbook/StudentTeacherandInternHandbook.pdf',
		'http://www.stpsb.org/substitutes',
		'http://www.stpsb.org/TitleIX.php',

		'http://www.stpsb.org/contact.php',
		'http://www.stpsb.org/contact_administration.php',
		'http://www.stpsb.org/contact_civil.php',
		'http://www.stpsb.org/contact_crimestoppers.php',
		'http://www.stpsb.org/contact_custodianofrecords.php',
		'http://www.stpsb.org/contact.php',
		'http://www.stpsb.org/contact_members.php',
		'http://www.stpsb.org/contact_harassment.php',

		'http://www.stpsb.org/schoolboard_members.php',
		'http://www.stpsb.org/schoolboard_mtgwebcasts.php',
		'http://www.stpsb.org/schoolboard_meetings.php',
		'http://www.stpsb.org/schoolboard_guidelines.php',
		'http://www.stpsb.org/schoolboard_minutes.php',
		'http://www.stpsb.org/schoolboard_members.php',
		'http://www.stpsb.org/schoolboard_policies2.php',
		'http://www.stpsb.org/../PDFFiles/strategicplan.pdf',

		'http://www.stpsb.org/about_admin.php',
		'http://www.stpsb.org/about_admin.php',
		'http://www.stpsb.org/http://nfussd.org',
		'http://www.stpsb.org/../BidDocs/bidinfomenupage.htm',
		'http://www.stpsb.org/../contact.php',
		'http://www.stpsb.org/../PDFFiles/strategicplan.pdf',
		'http://www.stpsb.org/about_finance.php',
		'http://www.stpsb.org/../PhotoArchives/index.htm',
		'http://www.stpsb.org/../PDFFiles/districtfastfacts.pdf',
		'http://www.stpsb.org/../schoolboard_members.php',
		'http://www.stpsb.org/TitleIX.php',

		'http://virtualacademy.stpsb.org',
		'http://www.stpsb.org/21stCentury/21stCenturyIndex.htm',
		'http://www.stpsb.org/PhotoArchives/index.htm',
	]
	mainfolder = 'stpsb'
	school_name = 'stpsb'
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
