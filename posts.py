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
