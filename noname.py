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

	if web_page != '#':
	# try:
		web_link = requests.get(web_page, timeout=5).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(class_='container').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='container').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='container').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='container').find_all(id='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='container').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='container').find_all(id='news-list') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='container') != None and web_soup.find(class_='container') != '':
			col1 = web_soup.find(class_='container')
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
		'https://www.danahall.org/about-us/wellesley-and-boston',
		'https://www.danahall.org/about-us/facilities-and-resources',
		'https://www.danahall.org/about-us/inclusion-and-diversity-statement',
		'https://www.danahall.org/about-us/mission-statement',
		'https://www.danahall.org/about-us/job-opportunities',
		'https://www.danahall.org/about-us/sustainability-at-dana-hall',
		'https://www.danahall.org/about-us/board-of-trustees',
		'https://vision2025.danahall.org/',
		'https://www.danahall.org/about-us/advocating-for-racial-justice',
		'https://www.danahall.org/academics/',
		'https://www.danahall.org/curriculum',
		'https://www.danahall.org/upper-school-classes/english',
		'https://www.danahall.org/upper-school-classes/mathematics',
		'https://www.danahall.org/upper-school-classes/science',
		'https://www.danahall.org/upper-school-classes/social-studies',
		'https://www.danahall.org/upper-school-classes/world-languages',
		'https://www.danahall.org/upper-school-classes/world-languages',
		'https://www.danahall.org/upper-school-classes/fitnessathletics',
		'https://www.danahall.org/upper-school-classes/performing-arts',
		'https://www.danahall.org/upper-school-classes/visual-arts',
		'https://www.danahall.org/middle-school-classes/english',
		'https://www.danahall.org/middle-school-classes/mathematics',
		'https://www.danahall.org/middle-school-classes/science',
		'https://www.danahall.org/middle-school-classes/social-studies',
		'https://www.danahall.org/middle-school-classes/world-languages',
		'https://www.danahall.org/middle-school-classes/engineering--computer-science',
		'https://www.danahall.org/middle-school-classes/fitnessathletics',
		'https://www.danahall.org/middle-school-classes/performing-arts',
		'https://www.danahall.org/middle-school-classes/visual-arts',
		'https://www.danahall.org/academic-advising-and-resources',
		'https://www.danahall.org/academics/global-education',
		'https://www.danahall.org/academics/girls-summer-entrepreneurship-program',
		'https://www.danahall.org/academics/college-counseling',
		'https://www.danahall.org/academics/college-counseling/meet-the-staff',
		'https://www.danahall.org/academics/college-counseling/matriculation-list',
		'https://www.danahall.org/academics/helen-temple-cooke-library',
		'https://www.danahall.org/about-us/why-dana-hall',
		'https://www.danahall.org/admission/inquire',
		'https://www.danahall.org/admission/how-to-apply',
		'https://www.danahall.org/admission/how-to-apply/information-for-international-students',
		'https://www.danahall.org/admission/how-to-apply/applicants-from-china',
		'https://www.danahall.org/admission',
		'https://www.danahall.org/admission/visit-dana',
		'https://www.danahall.org/admission/visit-dana/admission-staff',
		'https://www.danahall.org/admission/visit-dana/interview-faqs',
		'https://www.danahall.org/Admission/Visit-Dana/Places-to-Stay-and-Eat',
		'https://www.danahall.org/admission/tuition--financial-aid',
		'https://www.danahall.org/tuition-and-payment-plans',
		'https://www.danahall.org/admission/transportation',
		'https://www.danahall.org/information-for-new-families',
		'https://www.danahall.org/f-1-student-visa',
		'https://www.danahall.org/information-for-new-families/new-middle-school-students-faqs',
		'https://www.danahall.org/information-for-new-families/new-upper-school-students-day-faqs',
		'https://www.danahall.org/information-for-new-families/new-upper-school-students-boarding-faqs',
		'https://www.danahall.org/information-for-new-families/new-families-faqs',
		'https://www.danahall.org/arts',
		'https://www.danahall.org/arts/visual-arts',
		'https://www.danahall.org/arts/dance',
		'https://www.danahall.org/arts/choral-music',
		'https://www.danahall.org/arts/theater',
		'https://www.danahall.org/arts/school-of-music',
		'https://www.danahall.org/arts/school-of-music/listen-to-dana-hall-music',
		'https://www.danahall.org/arts/the-dana-hall-art-gallery',
		'https://www.danahall.org/arts/the-dana-hall-art-gallery/artist-in-residence-program',
		'https://www.danahall.org/athletics',
		'https://www.danahall.org/athletics/teams--schedules',
		'https://www.danahall.org/athletics/notable-alumnae-athletes',
		'https://www.danahall.org/athletics/athletic-facilities',
		'https://www.danahall.org/athletics/athletics-philosophy',
		'https://www.danahall.org/admission/inquire',
		'https://sideline.bsnsports.com/schools/massachusetts/wellesleyhills/dana-hall-school',
		'https://www.danahall.org/athletics/awards-and-championships',
		'https://www.danahall.org/athletics/fitness-program',
		'https://www.danahall.org/athletics/coaching-staff',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/ksec-staff',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/interscholastic-equestrian-team',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/boarders',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/internships-and-teams',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/lesson-program',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/faqs',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/ksec-summer-training-academy',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/ksec-summer-training-academy/apply-now-ksec-summer-training-academy',
		'https://www.danahall.org/donate-a-horse',
		'https://www.danahall.org/giving',
		'https://danahall.myschoolapp.com/page/giving/give-online?siteId=1055&ssl=1',
		'https://www.danahall.org/giving/meet-our-staff',
		'https://www.danahall.org/giving/ways-to-give',
		'https://www.danahall.org/giving/ways-to-give/stock-transfer-instructions',
		'https://www.danahall.org/giving/ways-to-give/wire-transfer-instructions',
		'https://www.danahall.org/giving/ways-to-give/donor-advised-fund-electronic-request',
		'https://www.danahall.org/giving/dana-dedicated',
		'https://www.danahall.org/giving/reunion-giving',
		'https://www.danahall.org/giving/the-dana-fund',
		'https://www.danahall.org/giving/dana-cares-fund',
		'https://www.danahall.org/giving/shades-alumnx-endowed-fund',
		'https://danahall.plannedgiving.org/',
		'https://www.danahall.org/giving/moon--stars-society',
		'https://www.danahall.org/student-life',
		'https://www.danahall.org/student-life/boarding-life',
		'https://www.danahall.org/student-life/community-service',
		'https://www.danahall.org/student-life/health-center',
		'https://www.danahall.org/student-life/diversity',
		'https://www.danahall.org/student-life/clubs-and-organizations',
		'https://www.danahall.org/student-life/health-and-wellness',
		'https://www.danahall.org/student-life/leadership',
		'https://www.danahall.org/external-programs',
		'https://www.danahall.org/external-programs/equestrian-summer-program',
		'https://www.danahall.org/external-programs/the-forum-spring-2019',
		'https://www.danahall.org/external-programs/girls-summer-leadership-program',
		'https://www.danahall.org/athletics/the-karen-stives-68-equestrian-center/ksec-summer-training-academy',
		'https://www.danahall.org/external-programs/womens-fitness-membership',
		'https://form.123formbuilder.com/712616?wwwNgRedir',
		'https://www.danahall.org/external-programs/school-of-music',
		'https://www.danahall.org/alumnae/welcome',
		'https://www.danahall.org/alumnae/alumnae-council-and-association',
		'https://www.danahall.org/alumnae/alumnae-awards',
		'https://www.danahall.org/alumnae-award-nomination',
		'https://www.danahall.org/alumnae/alumnae-directory',
		'https://www.danahall.org/alumnae/notable-alumnae',
		'https://www.danahall.org/alumnae/volunteer-opportunities',
		'https://www.danahall.org/alumnae/super-spring-reunion-2021',
		'https://www.danahall.org/alumnae/she-sails-2021',
	]
	# mainfolder = all_sites[0].split('.')[1]
	mainfolder = 'danahall'
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
		school_name = 'danahall'

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
