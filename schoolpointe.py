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

		if tag.contents == [] or (len(tag.contents) < 2 and tag.contents[0] == '\xa0'):
			tag.decompose()


def remove_tags(text):
	div = re.compile(r'<div[^>]+>')
	dive = re.compile(r'<div+>')
	divc = re.compile(r'</div+>')
	link = re.compile(r'<link[^>]+>')
	section = re.compile(r'<section[^>]+>')
	sectione = re.compile(r'<section+>')
	sectionc = re.compile(r'</section+>')
	article = re.compile(r'<article[^>]+>')
	articlee = re.compile(r'<article+>')
	articlec = re.compile(r'</article+>')
	span = re.compile(r'<span+>')
	spane = re.compile(r'<span[^>]+>')
	spanc = re.compile(r'</span+>')
	font = re.compile(r'<font+>')
	fonte = re.compile(r'<font[^>]+>')
	fontc = re.compile(r'</font+>')

	text = div.sub('', text)
	text = dive.sub('', text)
	text = divc.sub('', text)
	text = link.sub('', text)
	text = section.sub('', text)
	text = sectione.sub('', text)
	text = sectionc.sub('', text)
	text = article.sub('', text)
	text = article.sub('', text)
	text = articlec.sub('', text)
	text = span.sub('', text)
	text = spane.sub('', text)
	text = spanc.sub('', text)
	text = font.sub('', text)
	text = fonte.sub('', text)
	text = fontc.sub('', text)
	text = re.sub('<!--|-->', '', text)

	return text.strip()


def get_column(col):
	col_images = col.find_all('img')
	col_anchors = col.find_all('a')
	col_tags = col.find_all(['article', 'b', 'button', 'col', 'colgroup', 'div', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'ul', 'ol', 'li', 'p', 'table', 'td', 'th', 'tr', 'strong', 'input', 'label', 'legend', 'fieldset'])
	clean_tags(col_tags)

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
					anchor.string = f'INTERNAL LINK {anchor.string}'

		except:
			print('Anchor:', anchor)

	col = remove_tags(str(col))

	return col


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

	# if web_page != '#':
	try:
		web_link = requests.get(web_page, timeout=5).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(class_='body-content-container').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='body-content-container').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='body-content-container').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='body-content-container').find_all(id='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='body-content-container').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='body-content-container').find_all(id='news-list') != []:
			news = 'news'

		if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
			page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='body-content-container') != None and web_soup.find(class_='body-content-container') != '':
			col1 = web_soup.find(class_='body-content-container')
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
		'https://www.ashland.k12.ky.us',
		'https://www.ashland.k12.ky.us/10/Home', # ahsp
		'https://www.ashland.k12.ky.us/3/Home', # cres
		'https://www.ashland.k12.ky.us/4/Home', # ces
		'https://www.ashland.k12.ky.us/5/Home', # hes
		'https://www.ashland.k12.ky.us/7/Home', # oes
		'https://www.ashland.k12.ky.us/8/home', # pes
		'https://www.ashland.k12.ky.us/2/home', # ams
		'https://www.ashland.k12.ky.us/1/Home', # pgbhs
		'https://www.ashland.k12.ky.us/12/Home', # gtp
	]

	mainfolder = all_sites[0].split('.')[1]
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open(f'../f_web_interface/static/files/{mainfolder}/report.csv', 'w', encoding='utf-8') as csv_report:
		csv_report = csv.writer(csv_report)
		s = 0

		for site in all_sites:
			s += 1
			page_counter = 0
			issue_pages_counter = 0
			split_slash = site.split('/')
			split_dot = site.split('.')
			split_mixed = site.split('/')[2].split('.')

			page = requests.get(site, timeout=5).content
			soup = BeautifulSoup(page, 'html.parser')
			sitemap = soup.find(id='bs-example-navbar-collapse-1')

			list_items = sitemap.select('ul > li')
			# list_items1 = sitemap.select('ul > li')
			# sitemap2 = soup.find(class_='header-elements')
			# list_items2 = sitemap2.select('ul.quicklinks > li')
			# list_items = itertools.chain(list_items1, list_items2)
			# school = soup.find(id='ctl00_ctl00_header_ctl00_lnkSchoolHome2').get_text()
			school = f'{split_dot[1]}_{s}'

			if len(school) > 30:
				school_name = str(school[:30]).lower().replace(' ', '_').replace('.', '')
			else:
				school_name = str(school).lower().replace(' ', '_').replace('.', '')

			csv_report.writerow(['School name', school_name])

			with open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
				csv_writer = csv.writer(csv_main)
				csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

				for i, item in enumerate(list_items):
					group_links = item.find_all('a')
					t1 = str(group_links[0].get_text()) if len(group_links[0].get_text()) > 0 else f'No tier {i}'

					for link in group_links:
						href = link.get('href')

						if len(href) > 1 and href[:2] == '//':
							page_link = f'{split_slash[0]}{href}'
						elif len(href) > 0 and href[0] == '/':
							page_link = f'{split_slash[0]}//{split_slash[2]}{href}'
						elif len(href) > 4 and href[:4] == 'http':
							page_link = href
						else:
							page_link = f'{split_slash[0]}//{split_slash[2]}/{href}'

						if href.find('.pdf') > -1:
							csv_writer.writerow([str(page_link), t1, str(link.get_text()), '', '', '1', 'Linked file', '', '', '', '', '', ''])
						else:
							if href.find('http') > -1 and href.split('/')[2].find(split_dot[1]) == -1:
								csv_writer.writerow([str(page_link), t1, str(link.get_text()), '', '', '1', 'Linked page', '', '', '', '', '', ''])
							else:
								page_counter += 1
								col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
								issue_pages_counter += content_ipc

								if group_links[0].get_text() != link.get_text():
									csv_writer.writerow([str(page_link), t1, str(link.get_text()), '', '', col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])
								else:
									csv_writer.writerow([str(page_link), t1, '', '', '', col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

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

										if href.find('.pdf') > -1:
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
