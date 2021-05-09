from pathlib import Path
from time import time
import csv
import glob
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
	# print(web_page)

	try:
		web_link = requests.get(web_page, timeout=10).content
		web_soup = BeautifulSoup(re.sub('<!--|-->', '', page), 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(id='page').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='page').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='page').find_all('iframe') != []:
			iframe = 'iframe'

		# if web_soup.find(id='page').find_all(id='calendar') != []:
		# 	calendar = 'calendar'
		#
		# if web_soup.find(id='page').find_all(class_='DIR-card') != []:
		# 	staff = 'staff'
		#
		# if web_soup.find(id='page').find_all(id='news-list') != []:
		# 	news = 'news'

		# if web_soup.find(class_='cs-side-nav-t1') != None:
		# 	page_nav = web_soup.find(class_='cs-side-nav-t1').find_all('a')

		# First column
		if web_soup.find(class_='pageContent') != None and web_soup.find(class_='pageContent') != '':
			col1 = web_soup.find(class_='pageContent')
			col1 = get_column(col1, splitter)
		# elif web_soup.find(id='subpage_right_sidebar') != None:
		# 	col1 = web_soup.find(id='subpage_right_sidebar')
		# 	col1 = get_column(col1, splitter)
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

	except:
		issue_pages_counter = 1

		return col1, col2, col3, col4, col_num, page_nav, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, issue_pages_counter


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		'http://www.lockhartisd.org',
		'http://abs.lockhartisd.org',
		'http://bes.lockhartisd.org',
		'http://cfes.lockhartisd.org',
		'http://ck.lockhartisd.org',
		'http://dmc.lockhartisd.org',
		'http://lhs.lockhartisd.org',
		'http://ljh.lockhartisd.org',
		'http://nes.lockhartisd.org',
		'http://ples.lockhartisd.org',
		'http://phs.lockhartisd.org',
		# 'https://cantiague.jerichoschools.org',
		# 'https://jackson.jerichoschools.org',
		# 'https://hs.jerichoschools.org',
		# 'https://ms.jerichoschools.org',
		# 'https://seaman.jerichoschools.org'

		# 'https://www.vbschools.com',
		# 'https://alantones.vbschools.com',
		# 'https://arrowheades.vbschools.com',
		# 'https://baysidees.vbschools.com',
		# 'https://birdneckes.vbschools.com',
		# 'https://brookwoodes.vbschools.com',
		# 'https://centervillees.vbschools.com',
		# 'https://christopherfarmses.vbschools.com',
		# 'https://collegeparkes.vbschools.com',
		# 'https://cookees.vbschools.com',
		# 'https://corporatelandinges.vbschools.com',
		# 'https://creedses.vbschools.com',
		# 'https://deyes.vbschools.com',
		# 'https://diamondspringses.vbschools.com',
		# 'https://fairfieldes.vbschools.com',
		# 'https://glenwoodes.vbschools.com',
		# 'https://greenrunes.vbschools.com',
		# 'https://hermitagees.vbschools.com',
		# 'https://hollandes.vbschools.com',
		# 'https://indianlakeses.vbschools.com',
		# 'https://kempsvillees.vbschools.com',
		# 'https://kempsvillemeadowses.vbschools.com',
		# 'https://kingsgrantes.vbschools.com',
		# 'https://kingstones.vbschools.com',
		# 'https://landstownes.vbschools.com',
		# 'https://linkhornparkes.vbschools.com',
		# 'https://luxfordes.vbschools.com',
		# 'https://lynnhavenes.vbschools.com',
		# 'https://malibues.vbschools.com',
		# 'https://newcastlees.vbschools.com',
		# 'https://newtownes.vbschools.com',
		# 'https://northlandinges.vbschools.com',
		# 'https://oceanlakeses.vbschools.com',
		# 'https://parkwayes.vbschools.com',
		# 'https://pembrokees.vbschools.com',
		# 'https://pembrokemeadowses.vbschools.com',
		# 'https://pointoviewes.vbschools.com',
		# 'https://princessannees.vbschools.com',
		# 'https://providencees.vbschools.com',
		# 'https://redmilles.vbschools.com',
		# 'https://rosemontes.vbschools.com',
		# 'https://rosemontforestes.vbschools.com',
		# 'https://salemes.vbschools.com',
		# 'https://seatackes.vbschools.com',
		# 'https://sheltonparkes.vbschools.com',
		# 'https://strawbridgees.vbschools.com',
		# 'https://tallwoodes.vbschools.com',
		# 'https://thaliaes.vbschools.com',
		# 'https://thoroughgoodes.vbschools.com',
		# 'https://threeoakses.vbschools.com',
		# 'https://trantwoodes.vbschools.com',
		# 'https://whiteoakses.vbschools.com',
		# 'https://williamses.vbschools.com',
		# 'https://windsoroakses.vbschools.com',
		# 'https://windsorwoodses.vbschools.com',
		# 'https://woodstockes.vbschools.com',
		# 'https://baysidems.vbschools.com',
		# 'https://bayside6ms.vbschools.com',
		# 'https://brandonms.vbschools.com',
		# 'https://corporatelandingms.vbschools.com',
		# 'https://greatneckms.vbschools.com',
		# 'https://independencems.vbschools.com',
		# 'https://kempsvillems.vbschools.com',
		# 'https://landstownms.vbschools.com',
		# 'https://larkspurms.vbschools.com',
		# 'https://lynnhavenms.vbschools.com',
		# 'https://olddonationschool.vbschools.com',
		# 'https://plazams.vbschools.com',
		# 'https://princessannems.vbschools.com',
		# 'https://salemms.vbschools.com',
		# 'https://virginiabeachms.vbschools.com',
		# 'https://baysidehs.vbschools.com',
		# 'https://coxhs.vbschools.com',
		# 'https://firstcolonialhs.vbschools.com',
		# 'https://greenruncollegiate.vbschools.com',
		# 'https://greenrunhs.vbschools.com',
		# 'https://kellamhs.vbschools.com',
		# 'https://kempsvillehs.vbschools.com',
		# 'https://landstownhs.vbschools.com',
		# 'https://oceanlakeshs.vbschools.com',
		# 'https://princessannehs.vbschools.com',
		# 'https://salemhs.vbschools.com',
		# 'https://tallwoodhs.vbschools.com',
		# 'https://adultlearning.vbschools.com',
		# 'https://advancedtechnologycenter.vbschools.com',
		# 'https://renaissanceacademy.vbschools.com',
		# 'https://techcenter.vbschools.com',
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
			sitemap = soup.find(class_='rmRootGroup')
			list_items = sitemap.select('li.rmItem')
			school = site.split('/')[-1].split('.')[0]

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

							# if nav_sec != None and nav_sec != '' and nav_sec != []:
							# 	for nav_link in nav_sec:
							# 		external_link = False
							#
							# 		if nav_link.get('href')[0] == '#':
							# 			page_link = '#'
							# 		elif len(nav_link.get('href')) > 1 and nav_link.get('href')[:2] == '//':
							# 			page_link = splitter[0] + nav_link.get('href')
							# 		elif nav_link.get('href')[0] == '/':
							# 			page_link = splitter[0] + '//' + splitter[2] + nav_link.get('href')
							# 		elif nav_link.get('href')[:4] == 'http':
							# 			page_link = nav_link.get('href')
							#
							# 			if nav_link.get('href').find(splitter[2].split('.')[1]) == -1:
							# 				external_link = True
							# 		else:
							# 			page_link = splitter[0] + '//' + splitter[2] + '/' + nav_link.get('href')
							#
							# 		if not external_link:
							# 			page_counter += 1
							# 			nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link, splitter)
							# 			issue_pages_counter += content_ipc
							# 			csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])
							#
							# 			if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
							# 				csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])
							# 		else:
							# 			csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', '1', 'Linked page', '', '', '', '', '', ''])
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
