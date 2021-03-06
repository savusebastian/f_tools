from pathlib import Path
from time import time
import csv
import multiprocessing

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

		if web_soup.find(class_='section-navigation') != None:
			page_nav = web_soup.find(class_='section-navigation').find_all('a')
		elif web_soup.find(class_='page-navigation') != None:
			page_nav = web_soup.find(class_='page-navigation').find_all('a')

		# First column
		if web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container1') != None and web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container1') != '':
			col1 = web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container1')
			col1 = get_column(col1, splitter)
		else:
			issue_pages_counter = 1

		if web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container2') != None and web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container2') != '':
			col2 = web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container2')
			col2 = get_column(col2, splitter)

		if web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container3') != None and web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container3') != '':
			col3 = web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container3')
			col3 = get_column(col3, splitter)

		if web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container4') != None and web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container4') != '':
			col4 = web_soup.find(id='sw-content-layout-wrapper').find(id='sw-content-container4')
			col4 = get_column(col4, splitter)

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


def parallel_schools(site, mainfolder, csv_report):
	page_counter = 0
	issue_pages_counter = 0

	splitter = site.split('/')
	page = requests.get(site).content
	soup = BeautifulSoup(page, 'html.parser')
	sitemap = soup.find(id='sw-sitemap')
	list_items = sitemap.select('li.sw-sitemap-channel-item')
	school = soup.find(id='sw-sitemap-sitelist').find('option', selected='selected').get_text()

	if len(school) > 30:
		school_name = str(school[:30]).lower().replace(' ', '_').replace('.', '')
	else:
		school_name = str(school).lower().replace(' ', '_').replace('.', '')

	csv_report.writerow(['School name', school_name])

	with open('../f_web_interface/static/files/' + mainfolder + '/' + school_name + '.csv', 'w', encoding='utf-8') as csv_main:
		csv_writer = csv.writer(csv_main)
		csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

		for item in list_items[1:]:
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


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		# 'https://www.satsumaschools.com/site/default.aspx?pagetype=15&SiteID=8&DirectoryType=6&SectionMax=15',
		# 'https://www.satsumaschools.com/site/default.aspx?pagetype=15&SiteID=9&DirectoryType=6&SectionMax=15'
		'https://www.mooreschools.com/site/Default.aspx?PageType=15&SiteID=1&SectionMax=15&DirectoryType=6',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=4848&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=2244&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=135&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=190&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=255&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=311&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=362&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=421&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=469&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=519&DirectoryType=6&SectionMax=15',
		'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=582&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=2269&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=633&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=680&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=732&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=779&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=2323&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=824&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=875&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=931&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=989&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1045&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1101&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=3198&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=3200&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=79&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1171&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1233&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1328&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1408&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1486&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1563&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=3199&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1655&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=2075&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=1858&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=2054&DirectoryType=6&SectionMax=15',
	]
	mainfolder = all_sites[0].split('.')[1]
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)
	processes = []

	with open('../f_web_interface/static/files/' + mainfolder + '/report.csv', 'w', encoding='utf-8') as csv_report:
		csv_report = csv.writer(csv_report)

		for site in all_sites:
			p = multiprocessing.Process(target=parallel_schools, args=[site, mainfolder, csv_report])
			p.start()
			processes.append(p)

		for process in processes:
			process.join()

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
