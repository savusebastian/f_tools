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


def clean_src(src):
	split = src.split('/')[3:]
	out = ''

	for x in split:
		out += f'/{x}'

	return out


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

				if src[0] != '/' and src[:4] != 'http':
					image['src'] = f'/{src}'
				elif src[:4] == 'http':
					image['src'] = clean_src(src)
				else:
					image['src'] = src

			else:
				image.attrs.clear()

			image['id'] = ''
			image['role'] = 'presentation'
			image['style'] = ''
			image['width'] = '250'

		except:
			pass
			# print('Image:', image)

	for anchor in col_anchors:
		try:
			if anchor.get('href') != None and anchor.get('href') != '':
				href = anchor['href']
				anchor.attrs.clear()

				if href[0] != '/' and href[:4] != 'http':
					anchor['href'] = f'/{href}'
				else:
					anchor['href'] = href

				if anchor.get('href')[:4] != 'http' and anchor.get('href').find('.pdf') == -1 and anchor.get('href').find('.txt') == -1\
				and anchor.get('href').find('.xls') == -1 and anchor.get('href').find('.xlsx') == -1\
				and anchor.get('href').find('.doc') == -1 and anchor.get('href').find('.docx') == -1\
				and anchor.get('href').find('.ppt') == -1 and anchor.get('href').find('.pptx') == -1:
					anchor.string = f'INTERNAL LINK {anchor.string}'

		except:
			pass
			# print('Anchor:', anchor)

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
	print(web_page)

	# if web_page != '#':
	try:
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/80.0'}
		web_link = requests.get(web_page, headers=headers, timeout=5).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find('main').find_all('form') != []:
			form = 'form'

		if web_soup.find('main').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find('main').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find('main').find_all(class_='fsCalendar') != []:
			calendar = 'calendar'

		if web_soup.find('main').find_all(class_='fsDirEntry') != []:
			staff = 'staff'

		if web_soup.find('main').find_all(class_='fsPost') != []:
			news = 'news'

		# if web_soup.find(class_='menu-ec-pages-menu-container') != None:
		# 	page_nav = web_soup.find(class_='menu-ec-pages-menu-container').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find('main') != None and web_soup.find('main') != '':
			col1 = web_soup.find('main')
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
		'https://www.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://acprep.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://banneker.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://borderstar.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://central.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://cms.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://eca.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://east.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://faxon.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://fla.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://garfield.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://melcher.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://carver.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://gladstone.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://halecook.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://holliday.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://james.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://rogers.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://hartman.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://lcpa.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://lcpams.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://longfellow.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://manual.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://king.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://northeast.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://nems.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://paseo.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://wheatley.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://pitcher.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://garcia.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://richardson.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://southeast.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://anderson.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://knotts.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://trailwoods.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://troost.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://phillips.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://whittier.kcpublicschools.org/fs/pages/sitemap.xml',
		'https://woodland.kcpublicschools.org/fs/pages/sitemap.xml',
	]
	schools = [
		'district',
		'acprep',
		'banneker',
		'borderstar',
		'central',
		'cms',
		'eca',
		'east',
		'faxon',
		'fla',
		'garfield',
		'melcher',
		'carver',
		'gladstone',
		'halecook',
		'holliday',
		'james',
		'rogers',
		'hartman',
		'lcpa',
		'lcpams',
		'longfellow',
		'manual',
		'king',
		'northeast',
		'nems',
		'paseo',
		'wheatley',
		'pitcher',
		'garcia',
		'richardson',
		'southeast',
		'anderson',
		'knotts',
		'trailwoods',
		'troost',
		'phillips',
		'whittier',
		'woodland',
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
			all_links = []

			page = requests.get(site, headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/80.0'}).content
			soup = BeautifulSoup(page, 'html.parser')
			sitemap = soup.find_all('loc')
			list_items = sitemap

			school_name = f'{split_dot[1]}_{schools[s - 1]}'
			csv_report.writerow(['School name', school_name])

			with open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
				csv_writer = csv.writer(csv_main)
				csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

				for i, item in enumerate(list_items):
					link = item.get_text().replace('-', ' ')
					tiers = link.split('/')
					t1, t2, t3, t4, t5, t6 = '', '', '', '', '', ''
					if len(tiers) == 4:
						t1 = tiers[-1].title()
					elif len(tiers) == 5:
						t1 = tiers[-2].title()
						t2 = tiers[-1].title()
					elif len(tiers) == 6:
						t1 = tiers[-3].title()
						t2 = tiers[-2].title()
						t3 = tiers[-1].title()
					elif len(tiers) == 7:
						t1 = tiers[-4].title()
						t2 = tiers[-3].title()
						t3 = tiers[-2].title()
						t4 = tiers[-1].title()
					# elif len(tiers) == 8:
					# 	t1 = tiers[-5].title()
					# 	t2 = tiers[-4].title()
					# 	t3 = tiers[-3].title()
					# 	t4 = tiers[-2].title()
					# 	t5 = tiers[-1].title()
					# elif len(tiers) == 9:
					# 	t1 = tiers[-6].title()
					# 	t2 = tiers[-5].title()
					# 	t3 = tiers[-4].title()
					# 	t4 = tiers[-3].title()
					# 	t5 = tiers[-2].title()
					# 	t6 = tiers[-1].title()
					else:
						print(len(tiers))

					page_counter += 1
					col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(item.get_text())
					issue_pages_counter += content_ipc

					csv_writer.writerow([str(item.get_text()), t1, t2, t3, t4, col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

					if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
						csv_report.writerow([str(item.get_text()), form, embed, iframe, calendar, staff, news])

				csv_report.writerow([])
				csv_report.writerow(['Pages scraped', page_counter])
				csv_report.writerow(['Issues', issue_pages_counter])
				csv_report.writerow([])
				csv_report.writerow([])
				csv_report.writerow([])

			print('Finished:', site)

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
