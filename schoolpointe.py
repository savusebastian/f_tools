from pathlib import Path
from time import time
import csv
import glob
import itertools
import re

from bs4 import BeautifulSoup
import requests


def clean_tags(tags):
	for tag in tags:
		tag.attrs.clear()

		if tag.contents == []:
			tag.decompose()


def remove_tags(text):
	div = re.compile(r'<div[^>]+>')
	dive = re.compile(r'<div+>')
	divc = re.compile(r'</div+>')
	span = re.compile(r'<span+>')
	spane = re.compile(r'<span[^>]+>')
	spanc = re.compile(r'</span+>')
	font = re.compile(r'<font+>')
	fonte = re.compile(r'<font[^>]+>')
	fontc = re.compile(r'</font+>')

	text = div.sub('', text)
	text = dive.sub('', text)
	text = divc.sub('', text)
	text = span.sub('', text)
	text = spane.sub('', text)
	text = spanc.sub('', text)
	text = font.sub('', text)
	text = fonte.sub('', text)
	text = fontc.sub('', text)
	text = re.sub('<!--|-->', '', text)

	return text.strip()


def get_column(col, splitter):
	col_images = col.find_all('img')
	col_anchors = col.find_all('a')
	col_tags = col.find_all(['article', 'b', 'button', 'col', 'colgroup', 'div', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'ul', 'ol', 'li', 'p', 'table', 'td', 'th', 'tr', 'strong', 'input', 'label', 'legend', 'fieldset'])
	clean_tags(col_tags)

	while col.link != None:
		col.link.decompose()

	while col.script != None:
		col.script.decompose()

	while col.style != None:
		col.style.decompose()

	while col.nav != None:
		col.nav.decompose()

	for image in col_images:
		try:
			if image.get('src') != None and image.get('src') != '':
				src = image['src']

				if 'alt' in image.attrs:
					alt = image['alt']
					image.attrs.clear()
					image['alt'] = alt
				else:
					image.attrs.clear()
					image['alt'] = 'alt-text'

				image['src'] = src

			else:
				image.attrs.clear()

			image['id'] = ''
			image['role'] = 'presentation'
			image['style'] = ''
			image['width'] = '250'

		except:
			print('Image:', image)

	for anchor in col_anchors:
		try:
			if anchor.get('href') != None and anchor.get('href') != '':
				href = anchor['href']
				anchor.attrs.clear()
				anchor['href'] = href

				if anchor.get('href')[:4] != 'http' and anchor.get('href').find('.pdf') == -1 and anchor.get('href').find('.txt') == -1\
				and anchor.get('href').find('.xls') == -1 and anchor.get('href').find('.xlsx') == -1\
				and anchor.get('href').find('.doc') == -1 and anchor.get('href').find('.docx') == -1\
				and anchor.get('href').find('.ppt') == -1 and anchor.get('href').find('.pptx') == -1:
					anchor.string = 'INTERNAL LINK ' + anchor.string

		except:
			print('Anchor:', anchor)

	col = remove_tags(str(col))

	return col


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

	# if web_page != '#':
	try:
		web_link = requests.get(web_page, timeout=10).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(class_='maincontentsection').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='maincontentsection').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='maincontentsection').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='maincontentsection').find_all(id='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='maincontentsection').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='maincontentsection').find_all(id='news-list') != []:
			news = 'news'

		if len(web_soup.find(class_='quicklinks')) != None:
			page_nav = web_soup.find(class_='quicklinks').find_all('a')

		# First column
		if web_soup.find_all(class_='maincontentsection')[0] != None and web_soup.find_all(class_='maincontentsection')[0] != '':
			col1 = web_soup.find_all(class_='maincontentsection')[0]
			col1 = get_column(col1, splitter)
		else:
			issue_pages_counter = 1

		# Second Column
		if web_soup.find(class_='col-xs-12 col-sm-12 col-md-3 col-lg-3 backgroundcolor') != None and web_soup.find(class_='col-xs-12 col-sm-12 col-md-3 col-lg-3 backgroundcolor') != '':
			col4 = web_soup.find(class_='col-xs-12 col-sm-12 col-md-3 col-lg-3 backgroundcolor')
			col4 = get_column(col4, splitter)
		# elif web_soup.find(class_='col-xs-12 col-sm-3') != None and web_soup.find(class_='col-xs-12 col-sm-3') != '':
		# 	col4 = web_soup.find(class_='col-xs-12 col-sm-3')
		# 	col4 = get_column(col4, splitter)

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
		'https://www.perry.kyschools.us',
		# 'https://www.warrencountyschools.org/greenwood/home',
		# 'https://www.warrencountyschools.org/CTE/home',
		# 'https://www.warrencountyschools.org/lostriver/home',
		# 'https://www.warrencountyschools.org/natcher/home',
		# 'https://www.warrencountyschools.org/northwarren/home',
		# 'https://www.warrencountyschools.org/oakland/home',
		# 'https://www.warrencountyschools.org/plano/home',
		# 'https://www.warrencountyschools.org/richpond/home',
		# 'https://www.warrencountyschools.org/richardsville/home',
		# 'https://www.warrencountyschools.org/rockfield/home',
		# 'https://www.warrencountyschools.org/22/home',
		# 'https://www.warrencountyschools.org/24/home',
		# 'https://www.warrencountyschools.org/25/home',
		# 'https://www.warrencountyschools.org/27/home',
		# 'https://www.warrencountyschools.org/28/home',
		# 'https://www.warrencountyschools.org/29/home',
		# 'https://www.warrencountyschools.org/31/home',
		# 'https://www.warrencountyschools.org/32/home',
		# 'https://www.warrencountyschools.org/jenningscreek/home',
		# 'https://www.warrencountyschools.org/swhs/home',
		# 'https://www.warrencountyschools.org/3/home',
		# 'https://www.warrencountyschools.org/warreneasthigh/home',
		# 'https://www.warrencountyschools.org/dcms/home',
		# 'https://www.warrencountyschools.org/henrymossmiddle/home',
		# 'https://www.warrencountyschools.org/swms/home',
		'https://www.warrencountyschools.org/WEMS/home',
		'https://www.warrencountyschools.org/alvaton/home',
		'https://www.warrencountyschools.org/briarwood/home',
		'https://www.warrencountyschools.org/bristow/home',
	]
	mainfolder = all_sites[0].split('.')[1]
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open('../f_web_interface/static/files/' + mainfolder + '/report.csv', 'w', encoding='utf-8') as csv_report:
		csv_report = csv.writer(csv_report)
		m = 0

		for site in all_sites:
			m += 1
			page_counter = 0
			issue_pages_counter = 0

			splitter = site.split('/')
			page = requests.get(site).content
			soup = BeautifulSoup(page, 'html.parser')
			# list_items = soup.find_all(class_='without-image')
			sitemap = soup.find(id='bs-example-navbar-collapse-1')
			list_items = sitemap.select('ul > li')
			# sitemap2 = soup.find(id='header-resources')
			# list_items2 = sitemap.select('ul > li')
			# list_items = itertools.chain(list_items1, list_items2)
			# school = soup.find(id='ctl00_ctl00_header_ctl00_lnkSchoolHome2').get_text()
			school = f'school_{m}'

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

						if len(link.get('href')) > 0 and link.get('href')[0] == '#':
							page_link = '#'
						elif len(link.get('href')) > 1 and link.get('href')[:2] == '//':
							page_link = splitter[0] + link.get('href')
						elif len(link.get('href')) > 0 and link.get('href')[0] == '/':
							page_link = splitter[0] + '//' + splitter[2] + link.get('href')
						elif len(link.get('href')) > 4 and link.get('href')[:4] == 'http':
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

									if len(nav_link.get('href')) > 0 and nav_link.get('href')[0] == '#':
										page_link = '#'
									elif len(nav_link.get('href')) > 1 and nav_link.get('href')[:2] == '//':
										page_link = splitter[0] + nav_link.get('href')
									elif len(nav_link.get('href')) > 0 and nav_link.get('href')[0] == '/':
										page_link = splitter[0] + '//' + splitter[2] + nav_link.get('href')
									elif len(nav_link.get('href')) > 4 and  nav_link.get('href')[:4] == 'http':
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
