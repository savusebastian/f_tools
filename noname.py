from pathlib import Path
from time import time
import csv
# import glob
# import re

from bs4 import BeautifulSoup
import requests

from util import get_column


# def clean_tags(tags):
# 	for tag in tags:
# 		tag.attrs.clear()
#
# 		if tag.contents == [] or (len(tag.contents) < 2 and tag.contents[0] == '\xa0'):
# 			tag.decompose()
#
#
# def remove_tags(text):
# 	div = re.compile(r'<div[^>]+>')
# 	dive = re.compile(r'<div+>')
# 	divc = re.compile(r'</div+>')
# 	link = re.compile(r'<link[^>]+>')
# 	section = re.compile(r'<section[^>]+>')
# 	sectione = re.compile(r'<section+>')
# 	sectionc = re.compile(r'</section+>')
# 	article = re.compile(r'<article[^>]+>')
# 	articlee = re.compile(r'<article+>')
# 	articlec = re.compile(r'</article+>')
# 	span = re.compile(r'<span+>')
# 	spane = re.compile(r'<span[^>]+>')
# 	spanc = re.compile(r'</span+>')
# 	font = re.compile(r'<font+>')
# 	fonte = re.compile(r'<font[^>]+>')
# 	fontc = re.compile(r'</font+>')
#
# 	text = div.sub('', text)
# 	text = dive.sub('', text)
# 	text = divc.sub('', text)
# 	text = link.sub('', text)
# 	text = section.sub('', text)
# 	text = sectione.sub('', text)
# 	text = sectionc.sub('', text)
# 	text = article.sub('', text)
# 	text = article.sub('', text)
# 	text = articlec.sub('', text)
# 	text = span.sub('', text)
# 	text = spane.sub('', text)
# 	text = spanc.sub('', text)
# 	text = font.sub('', text)
# 	text = fonte.sub('', text)
# 	text = fontc.sub('', text)
# 	text = re.sub('<!--|-->', '', text)
#
# 	return text.strip()
#
#
# def clean_src(src):
# 	split = src.split('/')[3:]
# 	out = ''
#
# 	for x in split:
# 		out += f'/{x}'
#
# 	return out
#
#
# def get_column(col):
# 	col_images = col.find_all('img')
# 	col_anchors = col.find_all('a')
# 	col_tags = col.find_all(['article', 'b', 'button', 'col', 'colgroup', 'div', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'ul', 'ol', 'li', 'p', 'table', 'td', 'th', 'tr', 'strong', 'input', 'label', 'legend', 'fieldset'])
# 	clean_tags(col_tags)
#
# 	while col.script != None:
# 		col.script.decompose()
#
# 	while col.style != None:
# 		col.style.decompose()
#
# 	while col.nav != None:
# 		col.nav.decompose()
#
# 	for image in col_images:
# 		try:
# 			if image.get('src') != None and image.get('src') != '':
# 				src = image['src']
#
# 				if 'alt' in image.attrs:
# 					alt = image['alt']
# 					image.attrs.clear()
# 					image['alt'] = alt
# 				else:
# 					image.attrs.clear()
# 					image['alt'] = 'alt-text'
#
# 				if src[0] != '/' and src[:4] != 'http':
# 					image['src'] = f'/{src}'
# 				elif src[:4] == 'http':
# 					image['src'] = clean_src(src)
# 				else:
# 					image['src'] = src
#
# 			else:
# 				image.attrs.clear()
#
# 			image['id'] = ''
# 			image['role'] = 'presentation'
# 			image['style'] = ''
# 			image['width'] = '250'
#
# 		except:
# 			pass
# 			# print('Image:', image)
#
# 	for anchor in col_anchors:
# 		try:
# 			if anchor.get('href') != None and anchor.get('href') != '':
# 				href = anchor['href']
# 				src = anchor['src']
# 				anchor.attrs.clear()
#
# 				# if href[0] != '/' and href[:4] != 'http':
# 				# 	anchor['href'] = f'/{href}'
# 				# else:
# 				# 	anchor['href'] = href
#
# 				if href[0] != '/' and href[:4] != 'http':
# 					anchor['href'] = f'/{src}'
# 				else:
# 					anchor['href'] = src
#
# 				if anchor.get('href')[:4] != 'http' and anchor.get('href').find('.pdf') == -1 and anchor.get('href').find('.txt') == -1\
# 				and anchor.get('href').find('.xls') == -1 and anchor.get('href').find('.xlsx') == -1\
# 				and anchor.get('href').find('.doc') == -1 and anchor.get('href').find('.docx') == -1\
# 				and anchor.get('href').find('.ppt') == -1 and anchor.get('href').find('.pptx') == -1:
# 					anchor.string = f'INTERNAL LINK {anchor.string}'
# 			else:
# 				anchor.attrs.clear()
#
# 		except:
# 			pass
# 			# print('Anchor:', anchor)
#
# 	col = remove_tags(str(col))
#
# 	return col


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

	if web_page != '#':
	# try:
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}
		# web_link = requests.get(web_page, headers=headers, timeout=10, verify=False).content
		web_link = requests.get(web_page, headers=headers, timeout=10).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(class_='pages-left-column').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='pages-left-column').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='pages-left-column').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='pages-left-column').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='pages-left-column').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='pages-left-column').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='pages-left-column') != None and web_soup.find(class_='pages-left-column') != '':
			col1 = web_soup.find(class_='pages-left-column')
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

	else:
	# except Exception:
		issue_pages_counter = 1

		return col1, col2, col3, col4, col_num, page_nav, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, issue_pages_counter


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=779501&type=d&pREC_ID=1182807',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=779501&type=d&pREC_ID=1177324',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=931438&type=d&pREC_ID=1399827',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=931438&type=d&pREC_ID=1400233',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=931438&type=d&pREC_ID=1803144',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=931438&type=d&pREC_ID=2090762',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=931438&type=d&pREC_ID=2090721',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=779501&type=d&pREC_ID=1182822',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090110',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090121',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090367',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090368',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090369',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090370',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090371',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090373',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090374',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090375',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090378',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2210033',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2210042',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2090462',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808892&type=d&pREC_ID=2251064',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808887&type=d&pREC_ID=1183280',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808887&type=d&pREC_ID=1183298',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808887&type=d&pREC_ID=1183314',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808887&type=d&pREC_ID=1183359',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808887&type=d&pREC_ID=1183360',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808887&type=d&pREC_ID=1808427',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=808887&type=d&pREC_ID=2095719',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=1180544',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=1047453&type=d&pREC_ID=1183296',
		'https://www.deperek12.org/apps/pages/district_enrollment',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=977371&type=d&pREC_ID=1297195',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=1179827&type=d&pREC_ID=1427237',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=1180073',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=1179999',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=1183376',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=1655669',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=1359754',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=1649391',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=782637&type=d&pREC_ID=2183361',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=1179827&type=d&pREC_ID=1427262',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=1179827&type=d&pREC_ID=1427271',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=1179827&type=d&pREC_ID=1428863',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2183516',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2118637',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2118827',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2181202',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2177816',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2118839',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2118846',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2118948',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2120604',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2118876',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2177812',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2120625',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2177791',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2177792',
		'https://www.deperek12.org/apps/pages/index.jsp?uREC_ID=2050023&type=d&pREC_ID=2177807',

		'https://www.deperek12.org/apps/pages/elementary_reading_goals',
		'https://drive.google.com/file/d/1bLh8A39blz3kNKY0Fn02iSYPNjZGu4EE/view',
		'https://altmayer.deperek12.org/apps/pages/index.jsp?uREC_ID=789277&type=d&pREC_ID=1182729',
		'https://altmayer.deperek12.org/apps/pages/volunteers',
		'https://docs.google.com/forms/d/e/1FAIpQLSdwS3uFEpkju0rLe69JYXWRM2Rlawe2aSFLbUS1EnD92cOzAg/viewform',
		'https://global-zone08.renaissance-go.com/welcomeportal/153322',
		'https://sites.google.com/depere.k12.wi.us/distancelearningforstudents/start-here',
		'https://classroom.google.com/h',
		'https://drive.google.com/file/d/1DZgOdRUgBCR-segSCweIWtWsupI0NDsS/view',
		'https://www.origoslate.com/slatecast',
		'https://altmayer.deperek12.org/apps/pages/index.jsp?uREC_ID=913298&type=d&pREC_ID=1182747',
		'https://app.typingagent.com/site/login?domain=depere',
		'https://www.brainpop.com/?panel=login',
		'https://sso.rumba.pk12ls.com/sso/login?service=https://cat.easybridge.pk12ls.com/ca/dashboard.htm&EBTenant=DPUSD-WI&profile=eb',
		'https://sites.google.com/depere.k12.wi.us/susie-c-altmayer-library/home?authuser=0',
		'https://app.seesaw.me/#/login',
		'https://idp-awsprod1.education.scholastic.com/idp/',
		'https://docs.google.com/document/d/112S5-8iAqptTAnvjfjsPzlktLWh3DLUYMfx5V_TzIjw/edit',
		'https://studio.code.org/users/sign_in',
		'https://student.freckle.com/#/login',
		'https://altmayer.deperek12.org/apps/pages/hour-of-code',
		'https://suite.smarttech-prod.com/student/login',
		'https://www.sumdog.com/sch/altmayer',
		'https://altmayer.deperek12.org/apps/pages/grade1',
		'https://altmayer.deperek12.org/apps/pages/grade2',
		'https://altmayer.deperek12.org/apps/pages/grade3',
		'https://altmayer.deperek12.org/apps/pages/grade4',

		'https://foxview.deperek12.org/apps/pages/index.jsp?uREC_ID=783501&type=d&pREC_ID=1180531',
		'https://foxview.deperek12.org/apps/pages/index.jsp?uREC_ID=783501&type=d&pREC_ID=1180525',
		'https://sites.google.com/depere.k12.wi.us/fx-4thgrade-orientation/home',
		'https://foxview.deperek12.org/apps/pages/index.jsp?uREC_ID=783501&type=d&pREC_ID=2154492',
		'https://4.files.edl.io/915a/07/29/21/175210-db7ee1ef-aa61-4940-a796-8b9471e9634d.pdf',
		'https://sites.google.com/depere.k12.wi.us/dpenrichmenttagk12',
		'https://foxview.deperek12.org/apps/pages/index.jsp?uREC_ID=783536&type=d&pREC_ID=1180572',
		'https://sites.google.com/a/depere.k12.wi.us/usdd-rti/',

		'https://sites.google.com/depere.k12.wi.us/dpms-counselors/meet-your-counselors',
		'https://dpms.deperek12.org/apps/pages/index.jsp?uREC_ID=783335&type=d&pREC_ID=1180365',
		'https://docs.google.com/document/d/1_cfF17_P7NOSPObu4XJlDL9NhomcZ7VL6dzzqQGteLM/edit',
		'https://4.files.edl.io/6094/08/24/21/180019-f2def7d5-1dd7-433d-97e1-16a9b8b897f7.pdf',
		'https://dpms.deperek12.org/apps/pages/index.jsp?uREC_ID=783337&type=d&pREC_ID=1180372',
		'https://dpms.deperek12.org/apps/pages/index.jsp?uREC_ID=783434&type=d&pREC_ID=1180444',
		'https://docs.google.com/forms/d/e/1FAIpQLSfmCQ8tUmVjGiOzoaWOPVCv6-I3Sg5zF35Ar9dLnQgBQmcE3g/viewform',
		'https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&access_type=online&approval_prompt=auto&client_id=803448468987-k6ojjvm1aoapljnsogf6ldgnkjctoelo.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fauth.xello.world%2Fgoogle%2Fstudent%2Fcallback&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fplus.me&include_granted_scopes=true&state=194549BA-F117-43C3-8B01-84CD84445629&flowName=GeneralOAuthFlow',
		'https://dpms.edf.school/',
		'https://dpms.deperek12.org/apps/pages/index.jsp?uREC_ID=783434&type=d&pREC_ID=1180450',
		'https://dpms.deperek12.org/apps/pages/index.jsp?uREC_ID=783434&type=d&pREC_ID=1180453',
		'https://sites.google.com/depere.k12.wi.us/dpms-extracurriculars/home',
		'https://dpms.deperek12.org/apps/bell_schedules/',

		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=1028787&type=d&pREC_ID=1332811',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782602&type=d&pREC_ID=1179993',
		'https://docs.google.com/document/d/1seZSldE3T_TVpH88_0akseDZJ98EwamOoPu7fEwTh90/edit',
		'https://sideline.bsnsports.com/schools/wisconsin/depere/de-pere-high-school/',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782636&type=d&pREC_ID=1775037',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782636&type=d&pREC_ID=1775266',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782636&type=d&pREC_ID=2279392',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782636&type=d&pREC_ID=1179998',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782855&type=d&pREC_ID=1180098',
		'https://www.deperek12.org/apps/news/article/1538568',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782855&type=d&pREC_ID=2147147',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782855&type=d&pREC_ID=2200185',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782855&type=d&pREC_ID=1243506',
		'https://dphscurrguide.weebly.com/',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=1191331&type=d&pREC_ID=1434778',
		'https://deperehsnewspaper.com/category/opinions/',
		'https://dphs.edf.school/',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782855&type=d&pREC_ID=1327073',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782855&type=d&pREC_ID=2248006',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782855&type=d&pREC_ID=1180102',
		'https://dphs.deperek12.org/apps/departments/index.jsp?show=TDE',
		'https://athletics.deperek12.org/',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782903&type=d&pREC_ID=1180111',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782903&type=d&pREC_ID=1309168',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782903&type=d&pREC_ID=1309169',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782903&type=d&pREC_ID=1309172',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782903&type=d&pREC_ID=1309166',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782636&type=d&pREC_ID=1180113',
		'https://dphs.deperek12.org/apps/pages/index.jsp?uREC_ID=782602&type=d&pREC_ID=1485037',
		'https://athletics.deperek12.org/apps/pages/index.jsp?uREC_ID=783065&type=d&pREC_ID=1180181',
		'https://athletics.deperek12.org/apps/pages/index.jsp?uREC_ID=783065&type=d&pREC_ID=2281148',
		'https://athletics.deperek12.org/apps/pages/index.jsp?uREC_ID=783065&type=d&pREC_ID=1180183',
		'https://athletics.deperek12.org/apps/pages/index.jsp?uREC_ID=783065&type=d&pREC_ID=1180184',
		'https://athletics.deperek12.org/apps/pages/index.jsp?uREC_ID=783065&type=d&pREC_ID=1767984',
		'https://docs.google.com/document/d/1bwSvV4Y3eMxiXd-JPQRklJpryf2QYeIezwysZvtKy5k/edit',
		'https://sites.google.com/depere.k12.wi.us/coaches-information/home',
		'https://sites.google.com/depere.k12.wi.us/coaches-information/logos-colors-guidelines',
		'https://sites.google.com/depere.k12.wi.us/coaches-information/forms',
	]
	mainfolder = 'deperek12'
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
		school_name = 'deperek12'

		csv_report.writerow(['School name', school_name])

		with open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
			csv_writer = csv.writer(csv_main)
			csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Tier 6', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

			for link in all_sites:
				tiers = link.split('/')
				t1, t2, t3, t4, t5, t6 = '', '', '', '', '', ''

				if len(tiers) == 3:
					t1 = tiers[-1].capitalize()
				elif len(tiers) == 4:
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
					t1 = tiers[-6].capitalize()
					t2 = tiers[-5].capitalize()
					t3 = tiers[-4].capitalize()
					t4 = tiers[-3].capitalize()
					t5 = tiers[-2].capitalize()
					t6 = tiers[-1].capitalize()
					print(len(tiers))

				page_counter += 1

				if link.split('/')[2].find(mainfolder) == -1:
					csv_writer.writerow([link, t1, t2, t3, t4, t5, t6, '1', 'Linked page', '', '', '', '', '', ''])
				else:
					col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(link)
					issue_pages_counter += content_ipc

					csv_writer.writerow([link, t1, t2, t3, t4, t5, t6, col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

					if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
						csv_report.writerow([link, form, embed, iframe, calendar, staff, news])

					# if nav_sec != None and nav_sec != '' and nav_sec != []:
					# 	for nav_link in nav_sec:
					# 		page_counter += 1
					# 		nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(link)
					# 		issue_pages_counter += content_ipc
					# 		csv_writer.writerow([link, str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])
					#
					# 		if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
					# 			csv_report.writerow([link, form, embed, iframe, calendar, staff, news])

			csv_report.writerow([])
			csv_report.writerow(['Pages scraped', page_counter])
			csv_report.writerow(['Issues', issue_pages_counter])
			csv_report.writerow([])
			csv_report.writerow([])
			csv_report.writerow([])

			# print('Finished:', site)

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
