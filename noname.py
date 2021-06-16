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

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

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
		'https://www.mpspk12.org/domain/304',
		'https://www.mpspk12.org/domain/290',
		'https://www.mpspk12.org/domain/12',
		'https://www.mpspk12.org/domain/312',
		'https://www.mpspk12.org/domain/16',
		'https://www.mpspk12.org/domain/248',
		'https://www.mpspk12.org/domain/10',
		'https://www.mpspk12.org/domain/11',
		'https://www.mpspk12.org/domain/17',
		'https://www.mpspk12.org/domain/227',
		'https://www.mpspk12.org/domain/245',
		'https://www.mpspk12.org/domain/22',
		'https://www.mpspk12.org/domain/23',
		'https://www.mpspk12.org/Page/39',
		'https://www.mpspk12.org/domain/25',
		'https://www.mpspk12.org/domain/26',
		'https://www.mpspk12.org/domain/27',
		'https://sites.google.com/mpspk12.org/mpsfood-services/home',
		'https://www.mpspk12.org/domain/30',
		'https://www.mpspk12.org/domain/33',
		'https://www.mpspk12.org/domain/33',
		'https://www.mpspk12.org/domain/31',
		'https://www.mpspk12.org/domain/234',
		'https://www.mpspk12.org/domain/35',
		'https://z2policy.ctspublish.com/masc/browse/mashpeeset/welcome/root',
		'https://www.mpspk12.org/domain/37',
		'https://www.mpspk12.org/domain/38',
		'https://www.mpspk12.org/domain/260',
		'https://www.mpspk12.org/domain/267',
		'https://www.mpspk12.org/domain/264',
		'https://www.mpspk12.org/domain/32',
		'https://www.mpspk12.org/domain/39',
		'https://sites.google.com/mpspk12.org/indianeducation',
		'https://www.mpspk12.org/domain/306',
		'https://calendar.google.com/calendar/u/0/embed?src=mpspk12.org_a8g96k8at7ei3g0njnb1qjr184@group.calendar.google.com&ctz=America/New_York',
		'https://drive.google.com/file/d/1pMwUaYMv2Fk-o9EtxXQQvD0kV2NI6Xth/view',
		'https://www.mpspk12.org/domain/259',
		'https://www.mpspk12.org/Page/18',
		'https://www.mpspk12.org/Page/15',
		'https://www.mpspk12.org/Page/18',
		'https://www.mpspk12.org/domain/257',
		'https://www.mpspk12.org/domain/45',
		'https://mashpee.powerschool.com/public/',
		'https://www.mpspk12.org/domain/315',
		'https://www.mpspk12.org/domain/46',
		'https://www.mpspk12.org/site/Default.aspx?PageID=1410',
		'https://www.mpspk12.org/domain/287',
		'https://sites.google.com/mpspk12.org/mpsstaffresources',
		'https://app.smartedu.net/mashpee/pd/default.cfm?',
		'https://sites.google.com/mpspk12.org/wearemashpee/home',
		'https://sites.google.com/mpspk12.org/wearemashpee/online-store?authuser=0',
		'https://www.mpspk12.org/domain/312',
		'https://www.mpspk12.org/Page/83',
		'https://www.mpspk12.org/Page/82',
		'https://www.mpspk12.org/Page/81',
		'https://www.mashpeerec.com/info/default.aspx',
		'https://www.mashpeema.gov/',
		'https://mashpeetv.com/',
		'https://sites.google.com/mpspk12.org/mashpeealumni/home',
		'https://sites.google.com/d/1E7W9zY5_6bPnNDu_y65IyumpdN05ozvy/p/1yda5nHpfMInB19HGIHCrAJ2CpkSkR6bn/edit',
		'https://www.mpspk12.org/domain/66',
		'https://www.mpspk12.org/Page/1439',
		'https://www.mpspk12.org/Page/2503',
		'https://www.mpspk12.org/Page/2546',
		'https://www.mpspk12.org/Page/1415',
		'https://www.mpspk12.org/Page/2542',
		'https://sites.google.com/mpspk12.org/mpsblendedlearning/home',
		'https://www.mpspk12.org/domain/274',
		'https://www.mpspk12.org/domain/301',
		'https://www.mpspk12.org/Page/14',
		'https://www.mpspk12.org/domain/57',
		'https://docs.google.com/document/d/1gpq2arAM5JHFK9ppjDOkIQOBbVz-TZ6iVVzxtTc-xBM/edit',
		'https://www.mpspk12.org/domain/16',
		'https://www.mpspk12.org/Page/1422',
		'https://www.mpspk12.org/Page/1423',
		'https://www.mpspk12.org/',
		'https://docs.google.com/document/d/1Cv1DL0XbMhsmDKHYJjao_0ZdXp8Xsypyc1E7CaEKzvM/edit',
		'https://docs.google.com/document/d/1nRDF_zh96lOxXYpIKFBNao6eEBVnBWvbCUB4x-pK3Qk/edit',
		'https://docs.google.com/document/d/1tZN8eeTHQKclZvIGY34Thwmy6U8koEXC237rsMAKSaQ/edit',
	]
	# mainfolder = all_sites[0].split('.')[1]
	mainfolder = 'mpspk12'
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open(f'../f_web_interface/static/files/{mainfolder}/report.csv', 'w', encoding='utf-8') as csv_report:
		csv_report = csv.writer(csv_report)

		page_counter = 0
		issue_pages_counter = 0
		split_slash = all_sites[0].split('/')
		split_dot = all_sites[0].split('.')
		split_mixed = all_sites[0].split('/')[2].split('.')
		all_links = []
		school_name = 'mpspk12'

		csv_report.writerow(['School name', school_name])

		with open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
			csv_writer = csv.writer(csv_main)
			csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Tier 6', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

			for link in all_sites:
				tiers = link.split('/')
				t1, t2, t3, t4, t5, t6 = '', '', '', '', '', ''
				if len(tiers) == 4:
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
					print(len(tiers))

				page_link = link

				page_counter += 1
				col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
				issue_pages_counter += content_ipc

				csv_writer.writerow([str(page_link), t1, t2, t3, t4, t5, t6, col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

				if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
					csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])

				# if nav_sec != None and nav_sec != '' and nav_sec != []:
				# 	for nav_link in nav_sec:				#
				# 		page_counter += 1
				# 		nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
				# 		issue_pages_counter += content_ipc
				# 		csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])
				#
				# 		if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
				# 			csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])

			csv_report.writerow([])
			csv_report.writerow(['Pages scraped', page_counter])
			csv_report.writerow(['Issues', issue_pages_counter])
			csv_report.writerow([])
			csv_report.writerow([])
			csv_report.writerow([])

			# print('Finished:', site)

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
