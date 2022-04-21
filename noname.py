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

		if web_soup.find(id='sw-content-layout-wrapper').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='sw-content-layout-wrapper').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='sw-content-layout-wrapper').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='sw-content-layout-wrapper').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='sw-content-layout-wrapper').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='sw-content-layout-wrapper').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='sw-content-layout-wrapper') != None and web_soup.find(id='sw-content-layout-wrapper') != '':
			col1 = web_soup.find(id='sw-content-layout-wrapper')
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
		'https://www.whiteplainspublicschools.org/site/Default.aspx?PageID=14',
		'https://www.whiteplainspublicschools.org/Page/26',
		'https://www.whiteplainspublicschools.org/Page/36',
		'https://www.whiteplainspublicschools.org/Domain/10',
		'https://www.whiteplainspublicschools.org/Page/9',
		'https://www.whiteplainspublicschools.org/Page/22835',
		'https://www.whiteplainspublicschools.org/Page/739',
		'https://www.whiteplainspublicschools.org/Page/22441',
		'https://www.whiteplainspublicschools.org/cms/lib/NY01000029/Centricity/Domain/66/22%2023%20REGISTRATION%20REQUIREMENTS.pdf',
		'https://www.whiteplainspublicschools.org/Page/12987',
		'https://www.whiteplainspublicschools.org/domain/56',
		'https://www.whiteplainspublicschools.org/domain/63',
		'https://www.whiteplainspublicschools.org/domain/59',
		'https://www.whiteplainspublicschools.org/domain/58',
		'https://www.whiteplainspublicschools.org/domain/51',
		'https://www.whiteplainspublicschools.org/Page/13992',
		'https://www.whiteplainspublicschools.org/domain/1980',
		'https://www.whiteplainspublicschools.org/domain/55',
		'https://www.whiteplainspublicschools.org/domain/60',
		'https://www.whiteplainspublicschools.org/domain/57',
		'https://www.whiteplainspublicschools.org/Page/20166',
		'https://www.whiteplainspublicschools.org/domain/2271',
		'https://www.whiteplainspublicschools.org/Page/425',
		'https://www.whiteplainspublicschools.org/Page/6611',
		'https://www.whiteplainspublicschools.org/Page/302',
		'https://www.whiteplainspublicschools.org/Page/512',
		'https://www.whiteplainspublicschools.org/site/Default.aspx?PageID=1221',
		'https://library.wpcsd.k12.ny.us/',
		'https://www.whiteplainspublicschools.org/Page/342',
		'https://www.whiteplainspublicschools.org/Page/309',
		'https://www.whiteplainspublicschools.org/domain/2518',
		'https://www.whiteplainspublicschools.org/Page/382',
		'https://www.whiteplainspublicschools.org/Page/319',
		'https://www.whiteplainspublicschools.org/Page/333',
		'https://www.whiteplainspublicschools.org/domain/2547',
		'https://www.whiteplainspublicschools.org/Page/394',
		'https://www.whiteplainspublicschools.org/site/Default.aspx?PageID=1118',
		'https://www.whiteplainspublicschools.org/Page/19702',
		'https://www.whiteplainspublicschools.org/Page/19702',
		'http://www.theloucksgames.org/',
		'https://www.familyid.com/organizations/white-plains-city-school-district-athletics',
		'https://www.whiteplainspublicschools.org/Page/19995',
		'https://www.whiteplainspublicschools.org/Page/22906',
		'https://www.whiteplainspublicschools.org/Page/22359',
		'https://www.whiteplainspublicschools.org/Page/22362',
		'https://www.whiteplainspublicschools.org/Page/22707',
		'https://www.whiteplainspublicschools.org/Page/22715',
		'https://www.whiteplainspublicschools.org/Page/22701',
		'https://www.whiteplainspublicschools.org/Page/22705',
		'https://www.whiteplainspublicschools.org/Page/22713',
		'https://www.whiteplainspublicschools.org/Page/22704',
		'https://www.whiteplainspublicschools.org/Page/22700',
		'https://www.whiteplainspublicschools.org/Page/20166',
		'https://www.whiteplainspublicschools.org/Page/22706',
		'https://www.whiteplainspublicschools.org/Page/22711',
		'https://www.whiteplainspublicschools.org/Page/19996',
		'https://www.whiteplainspublicschools.org/Page/22710',
		'https://www.whiteplainspublicschools.org/Page/22036',
		'https://www.whiteplainspublicschools.org/Page/22805',
		'https://www.whiteplainspublicschools.org/Page/582',
		'https://www.whiteplainspublicschools.org/Page/22835',
		'https://www.whiteplainspublicschools.org/Page/22877',
		'https://www.whiteplainspublicschools.org/Page/22202',
		'https://www.whiteplainspublicschools.org/Page/22559',
		'https://www.whiteplainspublicschools.org/Page/21333',
		'https://www.whiteplainspublicschools.org/Page/21341',
		'https://www.whiteplainspublicschools.org/Page/13992',
		'https://www.whiteplainspublicschools.org/Page/19995',
		'https://www.whiteplainspublicschools.org/domain/63',
		'https://www.whiteplainspublicschools.org/Page/22198',
		'https://www.whiteplainspublicschools.org/Page/21345',
		'https://www.whiteplainspublicschools.org/domain/59',
		'https://www.whiteplainspublicschools.org/domain/60',
		'https://www.whiteplainspublicschools.org/Page/22750',
		'https://www.whiteplainspublicschools.org/Page/20555',
		'https://www.whiteplainspublicschools.org/cms/module/selectsurvey/TakeSurvey.aspx?SurveyID=1762',
		'https://www.whiteplainspublicschools.org/Page/22233',
		'https://portfolio.capitalregionboces.org/wp-content/uploads/2020/08/56312_Portflio-BusRts-infographic1.pdf',
		'https://www.whiteplainspublicschools.org/Page/22253',
		'https://www.whiteplainspublicschools.org/Page/22232',
		'https://www.whiteplainspublicschools.org/Page/627',
		'https://www.whiteplainspublicschools.org/Page/625',
		'https://www.whiteplainspublicschools.org/Page/630',
		'https://www.whiteplainspublicschools.org/Page/19509',
		'https://www.whiteplainspublicschools.org/Page/20561',
		'https://infofinderle11.transfinder.com/wpcsd.k12.ny.us/login.aspx',
		'https://www.whiteplainspublicschools.org/Page/21397',
		'https://www.whiteplainspublicschools.org/Page/21400',
		'https://www.whiteplainspublicschools.org/Page/21401',
		'https://www.whiteplainspublicschools.org/Page/21460',
		'https://www.whiteplainspublicschools.org/Page/21513',
		'https://www.whiteplainspublicschools.org/Page/22440',
		'https://www.whiteplainspublicschools.org/Page/22267',
		'https://www.whiteplainspublicschools.org/Page/616',
		'https://www.whiteplainspublicschools.org/Page/22278',
		'https://www.whiteplainspublicschools.org/Page/618',
		'https://www.whiteplainspublicschools.org/Page/619',
		'https://www.whiteplainspublicschools.org/Page/620',
		'https://www.whiteplainspublicschools.org/Page/621',
		'https://www.whiteplainspublicschools.org/domain/58',
		'https://www.whiteplainspublicschools.org/Page/22828',
		'https://www.whiteplainspublicschools.org/Page/22878',
		'https://www.whiteplainspublicschools.org/Page/22279',
		'https://www.whiteplainspublicschools.org/Page/21342',
		'https://www.whiteplainspublicschools.org/Page/21479',
		'https://www.whiteplainspublicschools.org/Page/21477',
		'https://www.whiteplainspublicschools.org/Page/21476',
		'https://www.whiteplainspublicschools.org/Page/21495',
		'https://www.whiteplainspublicschools.org/Page/21480',
		'https://www.whiteplainspublicschools.org/Page/20843',
		'https://www.whiteplainspublicschools.org/Page/21435',
		'https://www.whiteplainspublicschools.org/Page/606',
		'https://www.whiteplainspublicschools.org/Page/19700',
		'https://www.whiteplainspublicschools.org/Page/19701',
		'https://www.whiteplainspublicschools.org/Page/17069',
		'https://www.whiteplainspublicschools.org/Page/17066',
		'https://www.whiteplainspublicschools.org/Page/19144',
		'https://www.whiteplainspublicschools.org/Page/607',
		'https://www.whiteplainspublicschools.org/Page/610',
		'https://www.whiteplainspublicschools.org/Page/17067',
		'https://www.whiteplainspublicschools.org/Page/17068',
		'https://www.whiteplainspublicschools.org/Page/19777',
		'https://www.whiteplainspublicschools.org/Page/21457',
		'https://www.whiteplainspublicschools.org/Domain/51',
		'https://www.whiteplainspublicschools.org/Page/546',
		'https://www.whiteplainspublicschools.org/Page/21773',
		'https://www.whiteplainspublicschools.org/Page/21759',
		'https://www.whiteplainspublicschools.org/Page/548',
		'https://www.whiteplainspublicschools.org/Page/549',
		'https://www.whiteplainspublicschools.org/Page/547',
		'https://www.whiteplainspublicschools.org/Page/552',
		'https://www.whiteplainspublicschools.org/Page/553',
		'https://www.whiteplainspublicschools.org/Page/21323',
		'https://www.whiteplainspublicschools.org/Domain/55',
		'https://www.whiteplainspublicschools.org/Page/578',
		'https://www.whiteplainspublicschools.org/Page/12250',
		'https://www.whiteplainspublicschools.org/Page/18406',
		'https://www.whiteplainspublicschools.org/Page/18407',
		'https://www.whiteplainspublicschools.org/Page/18301',
		'https://www.whiteplainspublicschools.org/Page/18408',
		'https://www.whiteplainspublicschools.org/Page/18676',
		'https://www.whiteplainspublicschools.org/Page/19460',
		'https://www.whiteplainspublicschools.org/Page/9718',
		'https://www.whiteplainspublicschools.org/Page/573',
		'https://www.whiteplainspublicschools.org/Page/18405',
		'https://www.whiteplainspublicschools.org/Page/19392',
		'https://www.whiteplainspublicschools.org/Page/22124',
		'https://www.whiteplainspublicschools.org/Page/22190',
		'https://www.whiteplainspublicschools.org/Page/22269',
		'https://www.whiteplainspublicschools.org/Page/22860',
	]
	mainfolder = 'whiteplainspublicschools'
	school_name = 'whiteplainspublicschools'
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
