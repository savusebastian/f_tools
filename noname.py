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

		if web_soup.find(class_='PAGE').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='PAGE').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='PAGE').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='PAGE').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='PAGE').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='PAGE').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='PAGE') != None and web_soup.find(class_='PAGE') != '':
			col1 = web_soup.find(class_='PAGE')
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
		'http://www.hibbing.k12.mn.us/district',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe762x1x68',
		'http://www.hibbing.k12.mn.us/our-schools',
		'http://www.hibbing.k12.mn.us/enrollment-procedures',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe766x1x68y1xe8cax1x68',
		'http://www.hibbing.k12.mn.us/superintendent-s-office',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xeb8ex1x68y1xeb95x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xeb8ex1x68y1xeb9bx1x68',
		'http://www.hibbing.k12.mn.us/2012-mca-test-results',
		'http://www.hibbing.k12.mn.us/mde-report-card',
		'http://www.hibbing.k12.mn.us/teacher-quality',
		'http://www.hibbing.k12.mn.us/school-board',
		'http://www.hibbing.k12.mn.us/members',
		'http://www.hibbing.k12.mn.us/agenda-and-minutes-2020-2021',
		'http://www.hibbing.k12.mn.us/agenda-and-minutes-2021-2022',
		'http://www.hibbing.k12.mn.us/committees',
		'http://www.hibbing.k12.mn.us/election-information',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe772x1x68y1xe970x1x68',
		'http://www.hibbing.k12.mn.us/business-office',
		'http://www.hibbing.k12.mn.us/benefits-information',
		'http://www.hibbing.k12.mn.us/certified-payroll',
		'http://www.hibbing.k12.mn.us/non-certified-payroll',
		'http://www.hibbing.k12.mn.us/accounts-payable',
		'http://www.hibbing.k12.mn.us/financial-information',
		'http://www.hibbing.k12.mn.us/employment-information',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe77cx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe77cx1x68y1xfbdfx1x68',
		'http://www.hibbing.k12.mn.us/referral-process-for-special-education',
		'http://www.hibbing.k12.mn.us/section-504-of-the-rehabilitation-act',
		'http://www.hibbing.k12.mn.us/oversight-committee',
		'http://www.hibbing.k12.mn.us/technology',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe77ex1x68y1xf91fx1x68',
		'http://www.hibbing.k12.mn.us/services',
		'http://www.hibbing.k12.mn.us/support',
		'http://www.hibbing.k12.mn.us/infrastructure',
		'http://www.hibbing.k12.mn.us/digital-learning',
		'http://www.hibbing.k12.mn.us/district-technology-vision',
		'http://www.hibbing.k12.mn.us/interactive-whiteboards',
		'http://www.hibbing.k12.mn.us/ipad-initiative',
		'http://www.hibbing.k12.mn.us/applications-services',
		'http://www.hibbing.k12.mn.us/photo-gallery',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe768x1x68',
		'http://www.hibbing.k12.mn.us/pseo',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe768x1x68y1xf7f0x1x68',
		'http://www.hibbing.k12.mn.us/english-language-learners',
		'http://www.hibbing.k12.mn.us/indian-education',
		'http://www.hibbing.k12.mn.us/educational-rights-of-homeless-children',
		'http://www.hibbing.k12.mn.us/testing-schedule',
		'http://www.hibbing.k12.mn.us/21-22-testing',
		'http://www.hibbing.k12.mn.us/buildings-and-grounds',
		'http://www.hibbing.k12.mn.us/crisis-management-plan',
		'http://www.hibbing.k12.mn.us/health-and-safety',
		'http://www.hibbing.k12.mn.us/bloodborne-pathogens',
		'http://www.hibbing.k12.mn.us/architectural-services-rfp',
		'http://www.hibbing.k12.mn.us/annual-notifications',
		'http://www.hibbing.k12.mn.us/health-service',
		'http://www.hibbing.k12.mn.us/immunization-notices',
		'http://www.hibbing.k12.mn.us/food-service',
		'http://www.hibbing.k12.mn.us/our-program',
		'http://www.hibbing.k12.mn.us/2021-2022-menus-and-prices',
		'http://www.hibbing.k12.mn.us/lunch-account-balances',
		'http://www.hibbing.k12.mn.us/free-reduced-application',
		'http://www.hibbing.k12.mn.us/transportation',
		'http://www.hibbing.k12.mn.us/bus-routes',
		'http://www.hibbing.k12.mn.us/bus-expectations',
		'http://www.hibbing.k12.mn.us/bus-rules-and-discipline',
		'http://www.hibbing.k12.mn.us/title-ix',
		'http://www.hibbing.k12.mn.us/office-of-civil-rights-information',
		'http://www.hibbing.k12.mn.us/definitions-of-federal-programs',
		'http://www.hibbing.k12.mn.us/vocational-opportunities',
		'http://www.hibbing.k12.mn.us/grievance-procedure-for-complaints-of-discrimination',
		'http://www.hibbing.k12.mn.us/school-resource-officer',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a1x1x68y1xe76ex1x68',
		'http://www.hibbing.k12.mn.us/historic-hibbing-high-school',
		'http://www.hibbing.k12.mn.us/high-school-auditorium',
		'http://www.hibbing.k12.mn.us/educational-organizations',
		'http://www.hibbing.k12.mn.us/local-area-links',
		'http://www.hibbing.k12.mn.us/schools',
		'http://www.hibbing.k12.mn.us/greenhaven-elementary-grades-k-2',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe413x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe420x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe420x1x68y1xe423x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe420x1x68y1xe426x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe420x1x68y1xe428x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe420x1x68y1xe42ax1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe420x1x68y1xe42cx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe420x1x68y1xe42ex1x68',
		'http://www.hibbing.k12.mn.us/polices',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe430x1x68y1xe432x1x68',
		'http://www.hibbing.k12.mn.us/district-policies-ges',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe55bx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe55bx1x68y1xe55fx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe55bx1x68y1xe561x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe55bx1x68y1xe567x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe55bx1x68y1xe569x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe570x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe576x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe576x1x68y1xe584x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe576x1x68y1xe586x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe576x1x68y1xe588x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe576x1x68y1xe58cx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe576x1x68y1xe58ex1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe411x1x68y1xe576x1x68y1xfe14x1x68',
		'http://www.hibbing.k12.mn.us/washington-elementary-grades-k-2',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5a0x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5adx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5adx1x68y1xe5b0x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5adx1x68y1xe5b3x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5adx1x68y1xe5b5x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5adx1x68y1xe5b7x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5adx1x68y1xe5b9x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5adx1x68y1xe5bbx1x68',
		'http://www.hibbing.k12.mn.us/district-school-policies',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5bex1x68y1xe5c0x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe5bex1x68y1xe5cdx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe708x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe708x1x68y1xe70fx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe708x1x68y1xe711x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe708x1x68y1xe713x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe708x1x68y1xe715x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe719x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe71fx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe71fx1x68y1xe72dx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe71fx1x68y1xe72fx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe71fx1x68y1xe731x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe71fx1x68y1xe735x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ax1x68y1xe71fx1x68y1xe737x1x68',
		'http://www.hibbing.k12.mn.us/lincoln-elementary-grades-3-6',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf089x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf089x1x68y1xf08cx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf089x1x68y1xf08fx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf089x1x68y1xf091x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf089x1x68y1xf093x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf089x1x68y1xf096x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf089x1x68y1xf098x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf09bx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf0a8x1x68',
		'http://www.hibbing.k12.mn.us/go-to-district-policies',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1bfx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1bfx1x68y1xf1c4x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1bfx1x68y1xf1c6x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1bfx1x68y1xf397x1x68',
		'http://www.hibbing.k12.mn.us/homework-helper',
		'http://www.hibbing.k12.mn.us/mathcounts',
		'http://www.hibbing.k12.mn.us/knowledge-bowl',
		'http://www.hibbing.k12.mn.us/health-services',
		'http://www.hibbing.k12.mn.us/pto',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1d2x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1d2x1x68y1xf1d3x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1dfx1x68',
		'http://www.hibbing.k12.mn.us/courses-of-study',
		'http://www.hibbing.k12.mn.us/supplies-list',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59cx1x68y1xf1dfx1x68y1xfc22x1x68',
		'http://www.hibbing.k12.mn.us/high-school-grades-7-12',
		'http://www.hibbing.k12.mn.us/tours-at-the-historic-hibbing-high-school',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xee61x1x68y1xee65x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xee61x1x68y1xee71x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xee61x1x68y1xee74x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xee61x1x68y1xee7dx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xee61x1x68y1xee80x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xee61x1x68y1xee85x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xee61x1x68y1xeea0x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeea7x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeeb3x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeeb3x1x68y1xeeb9x1x68',
		'http://www.hibbing.k12.mn.us/counseling-dept',
		'http://www.hibbing.k12.mn.us/new-student-info',
		'http://www.hibbing.k12.mn.us/college-planning',
		'http://www.hibbing.k12.mn.us/act-sat-info',
		'http://www.hibbing.k12.mn.us/scholarships',
		'http://www.hibbing.k12.mn.us/financial-aid-information',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeeb3x1x68y1xeee0x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeeb3x1x68y1xeee2x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeeb3x1x68y1xeee4x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeee2x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeee4x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeeedx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeeefx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeef1x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeef3x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeef5x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeef9x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeefbx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeefdx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xeeffx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xef01x1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xeee8x1x68y1xeeeax1x68y1xef03x1x68',
		'http://www.hibbing.k12.mn.us/theater',
		'http://www.hibbing.k12.mn.us/postsecondary-enrollment-options-pseo',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xef5bx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xef5bx1x68y1xef5cx1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a3x1x68y1xe59ex1x68y1xef70x1x68',
		'http://www.hibbing.k12.mn.us/see-district-policies',
		'http://www.hibbing.k12.mn.us/community-education',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a5x1x68y1xe1afx1x68',
		'http://www.hibbing.k12.mn.us/meet-the-staff',
		'http://www.hibbing.k12.mn.us/hce-policies',
		'http://www.hibbing.k12.mn.us/early-learning-center',
		'http://www.hibbing.k12.mn.us/early-childhood-screening',
		'http://www.hibbing.k12.mn.us/adults-with-disabilities',
		'http://www.hibbing.k12.mn.us/after-school-child-care',
		'http://www.hibbing.k12.mn.us/adult-education-ged',
		'http://www.hibbing.k12.mn.us/instructor-forms',
		'http://www.hibbing.k12.mn.us/bluejacket-pride',
		'http://www.hibbing.k12.mn.us/district-wellness',
		'http://www.hibbing.k12.mn.us/activities',
		'http://www.hibbing.k12.mn.us/activities-department',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xec05x1x68y1xec30x1x68',
		'http://www.hibbing.k12.mn.us/athletic-and-fine-arts-activities',
		'http://www.hibbing.k12.mn.us/athletic-schedules-and-scores',
		'http://www.hibbing.k12.mn.us/participation-fees',
		'http://www.hibbing.k12.mn.us/links',
		'http://www.hibbing.k12.mn.us/parents',
		'http://www.hibbing.k12.mn.us/calendars-athletic-schedules',
		'http://www.hibbing.k12.mn.us/enrollment-procedure',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a9x1x68y1xe208x1x68y1xe218x1x68y1xe8cax1x68',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a9x1x68y1xe208x1x68y1xe23fx1x68',
		'http://www.hibbing.k12.mn.us/ipad-tips-for-parents',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a9x1x68y1xe208x1x68y1xe768x1x68',
		'http://www.hibbing.k12.mn.us/pseo',
		'http://www.hibbing.k12.mn.us/ittrium/visit/A1x264x1x82y1x26cx1x7fy1xe1a9x1x68y1xe208x1x68y1xe768x1x68y1xf7f0x1x68',
		'http://www.hibbing.k12.mn.us/english-language-learners',
		'http://www.hibbing.k12.mn.us/indian-education',
		'http://www.hibbing.k12.mn.us/educational-rights-of-homeless-children',
		'http://www.hibbing.k12.mn.us/testing-schedule',
		'http://www.hibbing.k12.mn.us/21-22-testing',
		'http://www.hibbing.k12.mn.us/students',
		'http://www.hibbing.k12.mn.us/library-card-catalogs',
		'http://www.hibbing.k12.mn.us/research-databases',
		'http://www.hibbing.k12.mn.us/on-line-reference',
		'http://www.hibbing.k12.mn.us/careers-colleges',
		'http://www.hibbing.k12.mn.us/search-tips',
		'http://www.hibbing.k12.mn.us/staff',
		'http://www.hibbing.k12.mn.us/create-single-sign-on-parent-account',
		'http://www.hibbing.k12.mn.us/superintendent-search-community-letter',
		'http://www.hibbing.k12.mn.us/superintendent-search-calendar',
		'http://www.hibbing.k12.mn.us/superintendent-posting',
		'http://www.hibbing.k12.mn.us/superintendent-profile',
		'http://www.hibbing.k12.mn.us/2013-mshsl-sports-health',
		'http://www.hibbing.k12.mn.us/2013-waivers',
		'http://www.hibbing.k12.mn.us/athletic-profile',
		'http://www.hibbing.k12.mn.us/2013-student-survey',
		'http://www.hibbing.k12.mn.us/2013sportsurveythanks',
		'http://www.hibbing.k12.mn.us/2013-parent-survey',
		'http://www.hibbing.k12.mn.us/2013sportparentsurveythanks',
		'http://www.hibbing.k12.mn.us/section-training',
		'http://www.hibbing.k12.mn.us/thank-you',
		'http://www.hibbing.k12.mn.us/foundation-donation',
		'http://www.hibbing.k12.mn.us/calendar-testing',
		'http://www.hibbing.k12.mn.us/calendar-testing-wide',
		'http://www.hibbing.k12.mn.us/iron-range-summer-institute',
	]
	mainfolder = 'hibbing'
	school_name = 'hibbing'
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
