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
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126792&type=d&pREC_ID=583713',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126792&type=d&pREC_ID=2057236',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126792&type=d&pREC_ID=583776',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256186&type=d&pREC_ID=626009',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256419&type=d&pREC_ID=585306',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256419&type=d&pREC_ID=1357102',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256187&type=d&pREC_ID=585094',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257712&type=d&pREC_ID=586852',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1147013&type=d&pREC_ID=1408388',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126791&type=d&pREC_ID=2162432',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126791&type=d&pREC_ID=2252640',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126791&type=d&pREC_ID=584113',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126721&type=d&pREC_ID=625839',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126721&type=d&pREC_ID=669222',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126721&type=d&pREC_ID=765669',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126721&type=d&pREC_ID=584072',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126721&type=d&pREC_ID=1131236',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126721&type=d&pREC_ID=1735841',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=583777',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=583781',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=591058',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=583779',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=583780',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=1270563',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=2288644',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256219&type=d&pREC_ID=592088',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=2288320',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=2288293',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=584134',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=985346',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=591528',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=584132',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=591523',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=2288496',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126968&type=d&pREC_ID=2288515',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1054657&type=d&pREC_ID=1351193',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=1072737',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=1325385',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=591513',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=1328117',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=2257908',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=1382947',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=1701186',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126965&type=d&pREC_ID=584137',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1848823&type=d&pREC_ID=592216',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1848823&type=d&pREC_ID=2168531',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1848823&type=d&pREC_ID=1389078',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1848823&type=d&pREC_ID=2168533',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256220&type=d&pREC_ID=625865',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=460845&type=d&pREC_ID=1010716',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256220&type=d&pREC_ID=1389106',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256220&type=d&pREC_ID=1745488',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256220&type=d&pREC_ID=2099425',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1614217&type=d&pREC_ID=1747257',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1396436&type=d&pREC_ID=1575212',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1396436&type=d&pREC_ID=1575219',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1396436&type=d&pREC_ID=1615591',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=594984',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=594918',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=594980',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=594989',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=594992',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=594995',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=595000',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262857&type=d&pREC_ID=595003',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=584077',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663870',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663870',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663876',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663929',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663885',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663891',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663895',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=2161277',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=663906',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256217&type=d&pREC_ID=2263406',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=497952&type=d&pREC_ID=1025963',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=498232&type=d&pREC_ID=1026062',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=497952&type=d&pREC_ID=1026004',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=497952&type=d&pREC_ID=1026537',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=497952&type=d&pREC_ID=1026245',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256221&type=d&pREC_ID=583378',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256221&type=d&pREC_ID=1762894',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256221&type=d&pREC_ID=links',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256221&type=d&pREC_ID=768757',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2187907&type=d&pREC_ID=592372',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2187907&type=d&pREC_ID=781123',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2187907&type=d&pREC_ID=1841442',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2187907&type=d&pREC_ID=1841443',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2187907&type=d&pREC_ID=781124',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2192131&type=d&pREC_ID=585065',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2192131&type=d&pREC_ID=1671492',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2192131&type=d&pREC_ID=1671489',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2192131&type=d&pREC_ID=2260557',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2187904&type=d&pREC_ID=1278248',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2145085&type=d&pREC_ID=1690264',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2145085&type=d&pREC_ID=654604',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2212792&type=d&pREC_ID=584163',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2212792&type=d&pREC_ID=1065597',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2212792&type=d&pREC_ID=584166',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2209572&type=d&pREC_ID=2194933',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2209572&type=d&pREC_ID=2194923',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=438037&type=d&pREC_ID=948573',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1560902&type=d&pREC_ID=1686868',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1560902&type=d&pREC_ID=1734539',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257735&type=d&pREC_ID=586931',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256220&type=d&pREC_ID=592188',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1147013&type=d&pREC_ID=1408388',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1147013&type=d&pREC_ID=1410645',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256216&type=d&pREC_ID=584070',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256216&type=d&pREC_ID=948963',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256216&type=d&pREC_ID=948970',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256216&type=d&pREC_ID=948965',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=300427&type=d&pREC_ID=693624',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259944&type=d&pREC_ID=590185',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259944&type=d&pREC_ID=590186',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=278666&type=d&pREC_ID=1389068',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257736&type=d&pREC_ID=586957',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256222&type=d&pREC_ID=584105',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256222&type=d&pREC_ID=1725255',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256222&type=d&pREC_ID=809461',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256222&type=d&pREC_ID=809714',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256222&type=d&pREC_ID=809429',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=334593&type=d&pREC_ID=742411',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1204351&type=d&pREC_ID=1443457',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1535600&type=d&pREC_ID=1666580',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2126721&type=d&pREC_ID=584072',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262854&type=d&pREC_ID=594891',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262854&type=d&pREC_ID=594895',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=262854&type=d&pREC_ID=594896',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2145085&type=d&pREC_ID=1710597',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2096779&type=d&pREC_ID=2141433',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2096779&type=d&pREC_ID=2141519',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2096779&type=d&pREC_ID=2141441',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2096779&type=d&pREC_ID=2141459',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2096779&type=d&pREC_ID=2141461',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259706&type=d&pREC_ID=589725',

		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=591062',
		'https://www.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256218&type=d&pREC_ID=2202242',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060779&type=d&pREC_ID=2124292',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060779&type=d&pREC_ID=2248747',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060768&type=d&pREC_ID=2124274',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060768&type=d&pREC_ID=2124277',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060768&type=d&pREC_ID=2124279',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060768&type=d&pREC_ID=2124280',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060768&type=d&pREC_ID=2124282',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2060791&type=d&pREC_ID=2124305',
		'https://intranet.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2212685&type=d&pREC_ID=2204160',

		'https://bbes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=487512&type=d&pREC_ID=1528645',

		'https://bbes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=458006&type=d&pREC_ID=996969',

		'https://les.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=2443630&type=d&pREC_ID=2233246',

		'https://mes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259103&type=d&pREC_ID=656054',
		'https://mes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256561&type=d&pREC_ID=585366',
		'https://mes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256563&type=d&pREC_ID=585370',
		'https://mes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256562&type=d&pREC_ID=585368',

		'https://mpes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257096&type=d&pREC_ID=1344880',
		'https://mpes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1246588&type=d&pREC_ID=1473136',
		'https://mpes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1785196&type=u&pREC_ID=2293260',
		'https://mpes.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=288912&type=d&pREC_ID=664741',

		'https://nse.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259227&type=d&pREC_ID=828211',

		'https://ses.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=258907&type=d&pREC_ID=794755',

		'https://bbis.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256394&type=d&pREC_ID=982820',
		'https://bbis.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256399&type=d&pREC_ID=585222',

		'https://mis.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1388671&type=d&pREC_ID=1568937',

		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1004137&type=d&pREC_ID=1316024',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257399&type=d&pREC_ID=586364',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257399&type=d&pREC_ID=838087',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257399&type=d&pREC_ID=843755',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257399&type=d&pREC_ID=2133541',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1014821&type=d&pREC_ID=1322385',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1011150&type=d&pREC_ID=1320458',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257379&type=d&pREC_ID=586290',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=736348&type=d&pREC_ID=1151290',
		'https://bbjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=736348&type=d&pREC_ID=1853068',

		'https://mjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=796668&type=d&pREC_ID=1187463',
		'https://mjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256587&type=d&pREC_ID=1054946',
		'https://mjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256752&type=d&pREC_ID=585780',
		'https://mjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256752&type=d&pREC_ID=641687',
		'https://mjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256752&type=d&pREC_ID=1016655',
		'https://mjh.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256752&type=d&pREC_ID=585783',

		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=380569&type=d&pREC_ID=862971',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=256746&type=d&pREC_ID=585666',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=280704&type=d&pREC_ID=2249470',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707614',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707615',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707623',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1913699',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707625',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707627',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1913544',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707628',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1780120',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707629',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707631',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707632',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707659',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707638',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1707634',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=2294520',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=2294535',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=2294516',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1579864&type=d&pREC_ID=1781409',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=683731',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=2255128',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=1093035',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=2038154',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=683743',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=1083315',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=690378',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=296098&type=d&pREC_ID=690070',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=284173&type=d&pREC_ID=649178',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1253420&type=u&pREC_ID=1729210',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1253420&type=u&pREC_ID=1734667',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1253420&type=u&pREC_ID=2123575',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1629513&type=d&pREC_ID=1771114',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1629513&type=d&pREC_ID=2047897',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1629513&type=d&pREC_ID=2047907',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=425415&type=u&pREC_ID=1575239',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257682&type=d&pREC_ID=586801',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257682&type=d&pREC_ID=855481',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257682&type=d&pREC_ID=729410',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257682&type=d&pREC_ID=842120',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257682&type=d&pREC_ID=809453',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=298278&type=d&pREC_ID=687839',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=298263&type=d&pREC_ID=698108',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=298255&type=d&pREC_ID=864233',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=298255&type=d&pREC_ID=2103414',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=298255&type=d&pREC_ID=1780728',
		'https://mhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259403&type=d&pREC_ID=751253',

		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674933',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=675439',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=673924',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674266',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674292',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=2082278',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=677086',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674290',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674922',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=762946',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674274',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674798',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=674282',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=1109518',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=292623&type=d&pREC_ID=815982',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1617919&type=d&pREC_ID=1752856',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=1615425&type=d&pREC_ID=1748951',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1248808',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=543414&type=d&pREC_ID=611369',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=605678',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=609540',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=824514',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=609569',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=609576',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=609583',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=632614',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=609577',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=274632&type=d&pREC_ID=889020',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1248024',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1903564',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1248355',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1248470',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1248474',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1248747',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=259264&type=d&pREC_ID=1248757',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257733&type=d&pREC_ID=645815',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257733&type=d&pREC_ID=586918',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257733&type=d&pREC_ID=586924',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257733&type=d&pREC_ID=586925',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257733&type=d&pREC_ID=586926',
		'https://mwhs.magnoliaisd.org/apps/pages/index.jsp?uREC_ID=257733&type=d&pREC_ID=586954',
	]
	mainfolder = 'metrotech'
	school_name = 'metrotech_foundation'
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
