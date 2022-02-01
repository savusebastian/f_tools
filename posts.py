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
	# print(web_page)

	# web_link = requests.get(web_page, timeout=10).content
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
	web_link = requests.get(web_page, headers=headers, timeout=10).content
	web_soup = BeautifulSoup(web_link, 'html.parser')
	# with open('x.txt', 'w', encoding='utf-8') as target:
	# 	target.write(str(web_soup))
	# print(web_soup)

	col1 = web_soup.find(class_='articleContentWrapper')
	col1 = get_column(col1)

	col1 = str(col1)

	if len(col1) > 150000:
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


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		'https://www.stonarschool.com/news/2021-05-14/THE-STONAR-WAY-14-MAY-2021'
	]

	with open('posts.csv', 'w', encoding='utf-8') as csv_main:
		csv_writer = csv.writer(csv_main)
		csv_writer.writerow(['Link to page', 'Column count', 'Column 1', 'Column 2', 'Column 3', 'Column 4'])

		for site in all_sites:
			col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(site)
			csv_writer.writerow([str(site), col_num, col1, col2, col3, col4])

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
