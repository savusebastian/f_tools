from pathlib import Path
from time import time
import csv

from bs4 import BeautifulSoup
import requests

from util import get_column


def get_content(web_page, splitter):
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

	try:
		web_link = requests.get(web_page, timeout=10).content
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

		if web_soup.find(id='sw-content-layout-wrapper').find_all(id='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='sw-content-layout-wrapper').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='sw-content-layout-wrapper').find_all(id='news-list') != []:
			news = 'news'

		# if web_soup.find(class_='cs-side-nav-t1') != None:
		# 	page_nav = web_soup.find(class_='cs-side-nav-t1').find_all('a')

		if web_soup.find(class_='main-inner').find(class_='content-zone') != None:
			col1 = web_soup.find(class_='main-inner').find(class_='content-zone')
			col1 = get_column(col1, splitter)
		else:
			issue_pages_counter = 1

		col1 = str(col1)
		col4 = str(col2) + str(col3) + str(col4)

		if len(col1) > 150000:
			col1 = 'Flagged'
			col2 = 'This page has too much content'
			col3 = ''
			col4 = ''
			col_num = '2'
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
	except:
		issue_pages_counter = 1

		return col1, col2, col3, col4, col_num, page_nav, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, issue_pages_counter


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		'https://www.ferndalesd.org',
		'https://www.ferndalesd.org/beach',
		'https://www.ferndalesd.org/cascadia',
		'https://www.ferndalesd.org/central',
		'https://www.ferndalesd.org/custer',
		'https://www.ferndalesd.org/eagleridge',
		'https://www.ferndalesd.org/ferndalehigh',
		'https://www.ferndalesd.org/horizonmiddle',
		'https://www.ferndalesd.org/skyline',
		'https://www.ferndalesd.org/vistamiddle',
	]
	mainfolder = all_sites[0].split('.')[1]
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open('../f_web_interface/static/files/' + mainfolder + '/report.csv', 'w', encoding='utf-8') as csv_report:
		csv_report = csv.writer(csv_report)

		for site in all_sites:
			page_counter = 0
			issue_pages_counter = 0

			splitter = site.split('/')
			page = requests.get(site).content
			soup = BeautifulSoup(page, 'html.parser')
			sitemap = soup.find(class_='cs-main-menu')
			list_items = sitemap.select('li.cs-mmenu-li')
			school = 'f_' + site.split('/')[-1]

			if len(school) > 30:
				school_name = str(school[:30]).lower().replace(' ', '_').replace('.', '')
			else:
				school_name = str(school).lower().replace(' ', '_').replace('.', '')

			csv_report.writerow(['School name', school_name])

			with open('../f_web_interface/static/files/' + mainfolder + '/' + school_name + '.csv', 'w', encoding='utf-8') as csv_main:
				csv_writer = csv.writer(csv_main)
				csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

				for item in list_items:
					group_links = item.find_all('a')

					for link in group_links:
						external_link = False

						if link.get('href')[0] == '#':
							page_link = '#'
						elif len(link.get('href')) > 1 and link.get('href')[:2] == '//':
							page_link = splitter[0] + link.get('href')
						elif link.get('href')[0] == '/':
							page_link = splitter[0] + '//' + splitter[2] + link.get('href')
						elif link.get('href')[:4] == 'http':
							page_link = link.get('href')

							if link.get('href').find(splitter[2].split('.')[1]) == -1:
								external_link = True
						else:
							page_link = splitter[0] + '//' + splitter[2] + '/' + link.get('href')

						if not external_link:
							page_counter += 1
							col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link, splitter)
							issue_pages_counter += content_ipc

							if group_links[0].get_text() != link.get_text():
								csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), '', '', col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])
							else:
								csv_writer.writerow([str(page_link), str(group_links[0].get_text()), '', '', '', col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

							if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
								csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])

							if nav_sec != None and nav_sec != '' and nav_sec != []:
								for nav_link in nav_sec:
									external_link = False

									if nav_link.get('href')[0] == '#':
										page_link = '#'
									elif len(nav_link.get('href')) > 1 and nav_link.get('href')[:2] == '//':
										page_link = splitter[0] + nav_link.get('href')
									elif nav_link.get('href')[0] == '/':
										page_link = splitter[0] + '//' + splitter[2] + nav_link.get('href')
									elif nav_link.get('href')[:4] == 'http':
										page_link = nav_link.get('href')

										if nav_link.get('href').find(splitter[2].split('.')[1]) == -1:
											external_link = True
									else:
										page_link = splitter[0] + '//' + splitter[2] + '/' + nav_link.get('href')

									if not external_link:
										page_counter += 1
										nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link, splitter)
										issue_pages_counter += content_ipc
										csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])

										if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
											csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])
									else:
										csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', '1', 'Linked page', '', '', '', '', '', ''])
						else:
							csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), '', '', '1', 'Linked page', '', '', '', '', '', ''])

				csv_report.writerow([])
				csv_report.writerow(['Pages scraped', page_counter])
				csv_report.writerow(['Issues', issue_pages_counter])
				csv_report.writerow([])
				csv_report.writerow([])
				csv_report.writerow([])

			print('Finished:', site)

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
