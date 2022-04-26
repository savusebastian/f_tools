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

	try:
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
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

		if web_soup.find(id='sw-content-layout-wrapper').find_all(class_='staffdirectorydiv') != []:
			staff = 'staff'

		if web_soup.find(id='sw-content-layout-wrapper').find_all(class_='headlines') != []:
			news = 'news'

		if web_soup.find(class_='section-navigation') != None:
			page_nav = web_soup.find(class_='section-navigation').find_all('a')
		elif web_soup.find(class_='page-navigation') != None:
			page_nav = web_soup.find(class_='page-navigation').find_all('a')

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
		# 'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=4&DirectoryType=6&SectionMax=6',
		# 'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=8&DirectoryType=6&SectionMax=6',
		# 'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=9&DirectoryType=6&SectionMax=6',
		# 'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=10&DirectoryType=6&SectionMax=6',
		# 'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=11&DirectoryType=6&SectionMax=6',
		# 'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=12&DirectoryType=6&SectionMax=6',
		'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=13&DirectoryType=6&SectionMax=6',
		'https://www.normandysc.org/site/default.aspx?pagetype=15&SiteID=15&DirectoryType=6&SectionMax=6',
	]
	mainfolder = all_sites[0].split('.')[1]
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open(f'../f_web_interface/static/files/{mainfolder}/report.csv', 'w', encoding='utf-8') as csv_report:
		csv_report = csv.writer(csv_report)

		for site in all_sites:
			page_counter = 0
			issue_pages_counter = 0
			split_slash = site.split('/')
			split_dot = site.split('.')
			split_mixed = site.split('/')[2].split('.')
			all_links = []

			headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
			page = requests.get(site, headers=headers).content
			soup = BeautifulSoup(page, 'html.parser')
			sitemap = soup.find(id='sw-sitemap')
			list_items = sitemap.select('li.sw-sitemap-channel-item')
			school = soup.find(id='sw-sitemap-sitelist').find('option', selected='selected').get_text()

			if len(school) > 30:
				school_name = str(school[:30]).lower().replace(' ', '_').replace('.', '')
			else:
				school_name = str(school).lower().replace(' ', '_').replace('.', '')

			csv_report.writerow(['School name', school_name])

			with open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
				csv_writer = csv.writer(csv_main)
				csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

				for item in list_items[1:]:
					group_links = item.find_all('a')
					t1 = str(group_links[0].get_text()) if len(group_links) > 0 and len(group_links[0].get_text()) > 0 else f'No tier'

					for link in group_links:
						href = link.get('href')
						t2 = str(link.get_text()) if group_links[0].get_text() != link.get_text() else ''

						if len(href) > 1 and href[:2] == '//':
							page_link = f'{split_slash[0]}{href}'
						elif len(href) > 0 and href[0] == '/':
							page_link = f'{split_slash[0]}//{split_slash[2]}{href}'
						elif len(href) > 4 and href[:4] == 'http':
							page_link = href
						else:
							page_link = f'{split_slash[0]}//{split_slash[2]}/{href}'

						if page_link not in all_links:
							all_links.append(page_link)

							if href.find('.pdf') > -1 or href.find('.mp3') > -1 or href.find('.wmv') > -1 or href.find('.mp4') > -1 or href.find('.docx') > -1 or href.find('.xlsx') > -1 or href.find('.pptx') > -1\
							or href.find('.doc') > -1 or href.find('.xls') > -1 or href.find('.ppt') > -1 or href.find('.jsp') > -1 or href.find('.m4v') > -1 or href.find('.mkv') > -1:
								csv_writer.writerow([str(page_link), school, t1, t2, '', '1', 'Linked file', '', '', '', '', '', ''])
							else:
								if href.find('http') > -1 and href.split('/')[2].find(split_dot[1]) == -1:
									csv_writer.writerow([str(page_link), school, t1, t2, '', '1', 'Linked page', '', '', '', '', '', ''])
								else:
									page_counter += 1
									col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
									issue_pages_counter += content_ipc

									csv_writer.writerow([str(page_link), school, t1, t2, '', col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

									if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
										csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])

									if nav_sec != None and nav_sec != '' and nav_sec != []:
										for nav_link in nav_sec:
											href = nav_link.get('href')

											if len(href) > 1 and href[:2] == '//':
												page_link = f'{split_slash[0]}{href}'
											elif len(href) > 0 and href[0] == '/':
												page_link = f'{split_slash[0]}//{split_slash[2]}{href}'
											elif len(href) > 4 and href[:4] == 'http':
												page_link = href
											else:
												page_link = f'{split_slash[0]}//{split_slash[2]}/{href}'

											if href.find('.pdf') > -1 or href.find('.mp3') > -1 or href.find('.wmv') > -1 or href.find('.mp4') > -1 or href.find('.docx') > -1 or href.find('.xlsx') > -1 or href.find('.pptx') > -1\
											or href.find('.doc') > -1 or href.find('.xls') > -1 or href.find('.ppt') > -1 or href.find('.jsp') > -1 or href.find('.m4v') > -1 or href.find('.mkv') > -1:
												csv_writer.writerow([str(page_link), t1, str(link.get_text()), '', '', '1', 'Linked file', '', '', '', '', '', ''])
											else:
												if href.find('http') > -1 and href.split('/')[2].find(split_dot[1]) == -1:
													csv_writer.writerow([str(page_link), t1, str(link.get_text()), '', '', '1', 'Linked page', '', '', '', '', '', ''])
												else:
													page_counter += 1
													nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
													issue_pages_counter += content_ipc
													csv_writer.writerow([str(page_link), t1, str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])

													if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
														csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])

				csv_report.writerow([])
				csv_report.writerow(['Pages scraped', page_counter])
				csv_report.writerow(['Issues', issue_pages_counter])
				csv_report.writerow([])
				csv_report.writerow([])
				csv_report.writerow([])

			print('Finished:', site)

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
