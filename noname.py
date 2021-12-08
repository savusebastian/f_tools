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
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'}
		# web_link = requests.get(web_page, headers=headers, timeout=20, verify=False).content
		web_link = requests.get(web_page, headers=headers, timeout=20).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(id='main').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='main').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='main').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='main').find_all(class_='calendargrid') != []:
			calendar = 'calendar'

		if web_soup.find(id='main').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='main').find_all(class_='news-info-cont') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='main') != None and web_soup.find(id='main') != '':
			col1 = web_soup.find(id='main')
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
		'https://www.adams12.org/district',
		'https://www.adams12.org/district/history-district',
		'https://www.adams12.org/initiatives/bond-proposal/11311/projects',
		'https://www.adams12.org/initiatives/2016-bond-program',
		'https://www.adams12.org/2016-bond-program/projects/arapahoe-ridge-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/centennial-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/century-middle-school',
		'https://www.adams12.org/2016-bond-program/projects/charter-schools',
		'https://www.adams12.org/2016-bond-program/projects/cherry-drive-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/coronado-hills-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/cotton-creek-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/coyote-ridge-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/eagleview-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/early-childhood-education-center',
		'https://www.adams12.org/2016-bond-program/projects/federal-heights-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/five-star-stadium',
		'https://www.adams12.org/2016-bond-program/projects/futureforward-bollman',
		'https://www.adams12.org/2016-bond-program/projects/futureforwardcampus',
		'https://www.adams12.org/2016-bond-program/projects/glacier-peak-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/hillcrest-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/horizon-high-school',
		'https://www.adams12.org/2016-bond-program/projects/hulstrom-k-8',
		'https://www.adams12.org/2016-bond-program/projects/hunters-glen-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/legacy-high-school',
		'https://www.adams12.org/2016-bond-program/projects/leroy-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/malley-drive-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/mcelwain-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/meridian-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/mountain-range-high-school',
		'https://www.adams12.org/2016-bond-program/projects/mountain-view-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/north-mor-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/north-star-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/northglenn-high-school',
		'https://www.adams12.org/2016-bond-program/projects/northglenn-middle-school',
		'https://www.adams12.org/2016-bond-program/projects/pathways-future-center-school',
		'https://www.adams12.org/2016-bond-program/projects/prairie-hills-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/riverdale-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/rocky-mountain-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/rocky-top-middle-school',
		'https://www.adams12.org/2016-bond-program/projects/shadow-ridge-middle-school',
		'https://www.adams12.org/2016-bond-program/projects/silver-creek-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/silver-hills-middle-school',
		'https://www.adams12.org/2016-bond-program/projects/skyview-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/stellar-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/stem-lab',
		'https://www.adams12.org/2016-bond-program/projects/stem-launch-k-8',
		'https://www.adams12.org/2016-bond-program/projects/student-family-resource-center',
		'https://www.adams12.org/2016-bond-program/projects/stukey-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/tarver-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/studio-school',
		'https://www.adams12.org/2016-bond-program/projects/thornton-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/thornton-high-school',
		'https://www.adams12.org/2016-bond-program/projects/thornton-middle-school',
		'https://www.adams12.org/2016-bond-program/projects/thunder-vista-p-8',
		'https://www.adams12.org/2016-bond-program/projects/vantage-point-high-school',
		'https://www.adams12.org/2016-bond-program/projects/westlake-middle-school',
		'https://www.adams12.org/2016-bond-program/projects/westview-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/woodglen-elementary-school',
		'https://www.adams12.org/2016-bond-program/projects/futureforwardcampus',
		'https://www.adams12.org/2016-bond-program/school-connectivity-project',
		'https://www.adams12.org/community-wide-investment-plan',
		'https://www.adams12.org/timeline-and-considerations',
		'https://www.adams12.org/initiatives/2016-bond-program/road-bond',
		'https://www.adams12.org/initiatives/2016-bond-program/need',
		'https://www.adams12.org/initiatives/2016-bond-program/what-you-told-us',
		'https://www.adams12.org/initiatives/2016-bond-program/plan',
		'https://www.adams12.org/initiatives/2016-bond-program/ballot-issue-3d',
		'https://www.adams12.org/bondcommunications',
		'https://www.adams12.org/2016-bond-program/bond-project-signs',
		'https://www.adams12.org/2016-bond-program/media-mentions',
		'https://www.adams12.org/2016-bond-program/annual-community-bond-update',
		'https://www.adams12.org/2016-bond-program/faq',
		'https://www.adams12.org/timeline-and-considerations',
		'https://www.adams12.org/admissions/boundary-maps',
		'https://www.adams12.org/admissions/boundary-process',
		'https://www.adams12.org/human-resources/careers',
		'https://www.adams12.org/human-resources/apply-job',
		'https://www.adams12.org/human-resources/now-hiring',
		'https://www.adams12.org/human-resources/now-hiring-base',
		'https://www.adams12.org/human-resources/job-fairs-and-events',
		'https://www.adams12.org/human-resources/working-adams-12-five-star-schools',
		'https://www.adams12.org/human-resources/job-descriptions',
		'https://www.adams12.org/human-resources/salary-schedules',
		'https://www.adams12.org/human-resources/benefits-overview',
		'https://www.adams12.org/human-resources/license-information',
		'https://www.adams12.org/human-resources/substitute-services',
		'https://www.adams12.org/human-resources/substitute-teachers-pay-rates',
		'https://www.adams12.org/human-resources/new-employees',
		'https://www.adams12.org/human-resources/new-educators',
		'https://www.adams12.org/human-resources/new-classified-employees',
		'https://www.adams12.org/human-resources/new-administrators',
		'https://www.adams12.org/human-resources/new-athleticactivity-coaches',
		'https://www.adams12.org/human-resources/new-guest-teachers',
		'https://www.adams12.org/human-resources/new-classified-substitutes',
		'https://www.adams12.org/human-resources/student-teaching',
		'https://www.adams12.org/human-resources/interest-based-strategies-ibs-and-classified-contract-negotiations',
		'https://www.adams12.org/human-resources/employee-recognition',
		'https://www.adams12.org/human-resources/2020-21-employees-year',
		'https://www.adams12.org/departments/communications',
		'https://www.adams12.org/communications/share-your-story',
		'https://www.adams12.org/departments/communications/media-resources',
		'https://www.adams12.org/communications/brand-guidelines',
		'https://www.adams12.org/communications/five-star-journal',
		'https://www.adams12.org/communications/social-media',
		'https://www.adams12.org/community-expectations',
		'https://www.adams12.org/communications/messaging-system',
		'https://www.adams12.org/communications/website-accessibility',
		'https://www.adams12.org/departments/communications/3/news',
		'https://www.adams12.org/departments/communications/3/documents',
		'https://www.adams12.org/communications/contact-communications',
		'https://www.adams12.org/safety-security/process-school-closures-and-2-hour-delayed-starts',
		'https://www.adams12.org/delayed-start-faqs',
		'https://www.adams12.org/district/contact',
		'https://www.adams12.org/district-policies',
		'https://www.adams12.org/initiatives/equity-review',
		'https://www.adams12.org/equity-review/frequently-asked-questions',
		'https://www.adams12.org/departments/financial-services',
		'https://www.adams12.org/financial-services/financial-transparency',
		'https://www.adams12.org/financial-services/district-adopted-budget',
		'https://www.adams12.org/financial-services/district-financial-audit',
		'https://www.adams12.org/financial-services/salary-schedules',
		'https://www.adams12.org/financial-services/individual-school-site-financial-information',
		'https://www.adams12.org/financial-services/other-district-specific-financial-information',
		'https://www.adams12.org/financial-services/charter-school-financial-transparency',
		'https://www.adams12.org/departments/financial-services/accounts-payable-accounts-receivable',
		'https://www.adams12.org/departments/financial-services/insufficient-funds-policy',
		'https://www.adams12.org/financial-services/payroll',
		'https://www.adams12.org/financial-services/student-fees',
		'https://www.adams12.org/departments/financial-services/billing',
		'https://www.adams12.org/financial-services/charter-school-helpful-links',
		'https://www.adams12.org/payment',
		'https://www.adams12.org/community/funding-101',
		'https://www.adams12.org/community/funding-101/where-does-marijuana-money-go',
		'https://www.adams12.org/community/funding-101/contact-your-representatives',
		'https://www.adams12.org/funding-mythbusters',
		'https://www.adams12.org/departments/board-education',
		'https://go.boarddocs.com/co/adams12/Board.nsf/Public',
		'https://www.adams12.org/board-education/meeting-minutes',
		'https://www.adams12.org/board-education/board-education-policies',
		'https://www.adams12.org/board-education/monitoring-reports',
		'https://www.adams12.org/board-education/board-resolutions-platform',
		'https://www.adams12.org/departments/board-education/director-districts',
		'https://www.adams12.org/board-education/board-elections',
		'https://www.adams12.org/departments/board-education/260/agenda',
		'https://www.adams12.org/departments/board-education/260/documents',
		'https://www.adams12.org/departments/board-education/260/events',
		'https://www.adams12.org/board-education/contact-board-education',
		'https://www.adams12.org/departments/superintendents-office',
		'https://www.adams12.org/superintendents-office/superintendent-chris-gdowski',
		'https://www.adams12.org/superintendents-office/multiple-pathways-student-learning',
		'https://www.adams12.org/district-policies',
		'https://www.adams12.org/departments/superintendents-office/contact-superintendents-office',
		'https://www.adams12.org/initiatives/blueprint-2032',
		'https://www.adams12.org/blueprint-2032/facilities-long-range-plan',
		'https://www.adams12.org/blueprint-2032/how-will-plan-be-created',
		'https://www.adams12.org/blueprint-2032/long-range-facilities-plan-timeline',
		'https://www.adams12.org/blueprint-2032/blueprint-2032-task-force-meeting-materials',
		'https://www.adams12.org/blueprint-2032/blueprint-2032-community-dialogue-sessions-fall-2021',
		'https://www.adams12.org/blueprint-2032/frequently-asked-questions',
		'https://www.adams12.org/blueprint-2032/glossary-terms',
		'https://www.adams12.org/programs/non-discrimination',
		'https://www.adams12.org/non-discrimination/district-policy-8400-definitions',
		'https://www.adams12.org/non-discrimination/non-discrimination-resolution-process',
		'https://www.adams12.org/non-discrimination/reporting-federal-or-state-agency',
		'https://www.adams12.org/non-discrimination/sexual-harassment-title-ix',
		'https://www.adams12.org/non-discrimination/what-sexual-harassment',
		'https://www.adams12.org/non-discrimination/reporting-obligations-allegations-sexual-harassment',
		'https://www.adams12.org/non-discrimination/filing-formal-complaint',
		'https://www.adams12.org/non-discrimination/resolution-process',
		'https://www.adams12.org/non-discrimination/phases-grievance-process',
		'https://www.adams12.org/non-discrimination/rights-parties',
		'https://www.adams12.org/non-discrimination/role-advisor',
		'https://www.adams12.org/non-discrimination/supportive-measures',
		'https://www.adams12.org/non-discrimination/violence-risk-analysis-vra',
		'https://www.adams12.org/non-discrimination/reporting-options',
		'https://www.adams12.org/non-discrimination/training-materials',
		'https://www.adams12.org/initiatives/elevate',
		'https://www.adams12.org/elevate/process',
		'https://www.adams12.org/elevate/process/elevate-strengths',
		'https://www.adams12.org/elevate-survey-results',
		'https://www.adams12.org/elevate-core-team',
		'https://www.adams12.org/elevate/challenge-reality',
		'https://www.adams12.org/elevate/strategic-plan',
		'https://www.adams12.org/elevate/funding-plan',
		'https://www.adams12.org/elevate-investment-plans',
		'https://www.adams12.org/elevate/say-thank-you',
		'https://www.adams12.org/initiatives/elevate/19926/documents',
		'https://www.adams12.org/initiatives/elevate/19926/news',
		'https://www.adams12.org/community/elevate-stories',
		'https://www.adams12.org/programs/astar',
		'https://www.adams12.org/programs/independence-academy',
		'https://www.adams12.org/independence-academy/mission-vision',
		'https://www.adams12.org/independence-academy/program-expectations',
		'https://www.adams12.org/independence-academy/courses-schedules',
		'https://www.adams12.org/programs/vista-view',
		'https://www.adams12.org/departments/assessments',
		'https://www.adams12.org/assessments/accountability',
		'https://www.adams12.org/departments/assessments/assessment-approach',
		'https://www.adams12.org/state-assessments',
		'https://www.adams12.org/departments/assessments/alternate-assessments',
		'https://www.adams12.org/assessments/cmas',
		'https://www.adams12.org/assessments/english-language-proficiency',
		'https://www.adams12.org/departments/assessments/pals',
		'https://www.adams12.org/satpsat',
		'https://www.adams12.org/assessments/teaching-strategies-gold',
		'https://www.adams12.org/district-assessments',
		'https://www.adams12.org/assessments/research',
		'https://www.adams12.org/initiatives/bell-times-adjustment-2020-21',
		'https://www.adams12.org/bell-times-adjustment-2020-21/bell-times-challenge',
		'https://www.adams12.org/bell-times-adjustment-2020-21/bell-times-process',
		'https://www.adams12.org/bell-times-adjustment-2020-21/bell-times-solution',
		'https://www.adams12.org/bell-times-adjustment-2020-21/bell-times-faqs',
		'https://www.adams12.org/programs/career-and-college-success',
		'https://www.adams12.org/career-and-college-success/career-pathways-success',
		'https://www.adams12.org/career-and-college-success/alternatives-college',
		'https://www.adams12.org/career-and-college-success/futureforward-career-and-technical-education',
		'https://www.adams12.org/career-and-college-success/career-pathways-after-high-school',
		'https://www.adams12.org/career-and-college-success/college-pathways-success',
		'https://www.adams12.org/career-and-college-success/international-baccalaureate-and-advanced-placement-courses',
		'https://www.adams12.org/career-and-college-success/ascent',
		'https://www.adams12.org/career-and-college-success/concurrent-and-dual-enrollment',
		'https://www.adams12.org/career-and-college-success/financial-aid',
		'https://www.adams12.org/career-and-college-success/resources-first-generation-college-students',
		'https://www.adams12.org/career-and-college-success/resources-students-who-are-undocumented',
		'https://www.adams12.org/career-and-college-success/college-preparation',
		'https://www.adams12.org/career-and-college-success/postsecondary-readiness',
		'https://www.adams12.org/career-and-college-success/alternative-education-options',
		'https://www.adams12.org/career-and-college-success/individual-career-and-academic-plan',
		'https://www.adams12.org/career-and-college-success/seal-biliteracy',
		'https://www.adams12.org/programs/career-technical-education',
		'https://www.adams12.org/career-technical-education/washington-square-campus',
		'https://www.adams12.org/career-technical-education/registration',
		'https://www.adams12.org/career-technical-education/faqs',
		'https://www.adams12.org/counseling/career-college-counseling',
		'https://www.adams12.org/career-and-college-success/alternatives-college',
		'https://www.adams12.org/counseling/applying-college',
		'https://www.adams12.org/departments/counseling/choosing-right-college',
		'https://www.adams12.org/counseling/first-generation-college-student',
		'https://www.adams12.org/counseling/paying-college',
		'https://www.adams12.org/career-and-college-success/individual-career-and-academic-plan',
		'https://www.adams12.org/counseling/undocumented-students',
		'https://www.adams12.org/departments/charter-schools',
		'https://www.adams12.org/charter-schools/charter-renewals',
		'https://www.adams12.org/charter-schools/new-charter-applications',
		'https://www.adams12.org/charter-schools/district-policy',
		'https://www.adams12.org/charter-schools/faqs',
		'https://www.adams12.org/departments/curriculum-instruction',
		'https://www.adams12.org/learning-services/strategic-literacy-plan',
		'https://www.adams12.org/curriculum-instruction/policy-and-process',
		'https://www.adams12.org/curriculum-instruction/digital-literacy-instruction',
		'https://www.adams12.org/curriculum-instruction/internet-safety',
		'https://www.adams12.org/libraries',
		'https://www.adams12.org/departments/curriculum-instruction/resources',
		'https://www.adams12.org/departments/curriculum-instruction/world-book',
		'https://www.adams12.org/curriculum-instruction/dyslexia-resources',
		'https://www.adams12.org/learning-services/five-star-schools-supports-students-dyslexia',
		'https://www.adams12.org/departments/english-language-learners',
		'https://www.adams12.org/english-language-learners/translation-and-interpretation',
		'https://www.adams12.org/departments/extended-learning',
		'https://www.adams12.org/programs/federal-programs',
		'https://www.adams12.org/federal-programs/title-i-part',
		'https://www.adams12.org/programs/homeless-education-title-x',
		'https://www.adams12.org/homeless-education-title-x/dispute-resolution',
		'https://www.adams12.org/homeless-education-title-x/rights-homeless-children',
		'https://www.adams12.org/homeless-education-title-x/transportation-options',
		'https://www.adams12.org/programs/migrant-education-title-i-c',
		'https://www.adams12.org/programs/native-education-title-vii',
		'https://www.adams12.org/cultural-enrichment-programs',
		'https://www.adams12.org/after-school-program',
		'https://www.adams12.org/cultural-enrichment-night',
		'https://www.adams12.org/programs/native-education-title-vii/native-american-athletic-club',
		'https://www.adams12.org/programs/native-education-title-vii/tipi-society',
		'https://www.adams12.org/native-education-title-vii/american-indian-parent-advisory-committee-aipac',
		'https://www.adams12.org/native-education-title-vii/student-counselor-resources',
		'https://www.adams12.org/native-education-title-vii/scholarships',
		'https://www.adams12.org/native-education-title-vii/summer-programs',
		'https://www.adams12.org/programs/native-education-title-vii/educational-organizations',
		'https://www.adams12.org/native-education-title-vii/family-resources',
		'https://www.adams12.org/native-education-title-vii/cultural-and-educational-resources',
		'https://www.adams12.org/departments/gifted-advanced-academics',
		'https://www.adams12.org/gifted-advanced-academics/identification-assessment',
		'https://www.adams12.org/gifted-advanced-academics/assessments-body-evidence',
		'https://www.adams12.org/gifted-advanced-academics/creative-or-productive-thinking',
		'https://www.adams12.org/gifted-advanced-academics/intellectual-abilityacademic-aptitude',
		'https://www.adams12.org/gifted-advanced-academics/leadership-abilities',
		'https://www.adams12.org/gifted-advanced-academics/transfer-gt-identifications',
		'https://www.adams12.org/gifted-advanced-academics/universal-screener',
		'https://www.adams12.org/gifted-advanced-academics/visual-arts-specific-talent-aptitude',
		'https://www.adams12.org/gifted-advanced-academics/programming',
		'https://www.adams12.org/gifted-advanced-academics/acceleration',
		'https://www.adams12.org/gifted-advanced-academics/advanced-learning-plans',
		'https://www.adams12.org/gifted-advanced-academics/early-access',
		'https://www.adams12.org/gifted-advanced-academics/resources',
		'https://www.adams12.org/gifted-advanced-academics/resource-library',
		'https://www.adams12.org/gifted-advanced-academics/supporting-emotional-needs-gifted',
		'https://www.adams12.org/programs/soar-honors-program',
		'https://www.adams12.org/programs/high-school-business',
		'https://www.adams12.org/programs/international-baccalaureate',
		'https://www.adams12.org/programs/legacy-2000',
		'https://www.adams12.org/programs/ptech',
		'https://www.adams12.org/career-and-college-success/graduation-requirements',
		'https://www.adams12.org/programs/kindergarten',
		'https://www.adams12.org/kindergarten/kindergarten-faqs',
		'https://www.adams12.org/kindergarten/countdown-kindergarten',
		'https://www.adams12.org/programs/preschool',
		'https://www.adams12.org/preschool/early-childhood-philosophy',
		'https://www.adams12.org/preschool/getting-started',
		'https://www.adams12.org/preschool/preschool-locations',
		'https://www.adams12.org/preschool/family-resources',
		'https://www.adams12.org/preschool/frequently-asked-questions-faq',
		'https://www.adams12.org/departments/records-requests',
		'https://www.adams12.org/departments/records-requests/colorado-open-records-act-cora-request',
		'https://www.adams12.org/records-requests/transcripts-and-academic-records',
		'https://www.adams12.org/departments/special-education',
		'https://www.adams12.org/special-education/parent-special-ed-record-request',
		'https://www.adams12.org/special-education/school-work-alliance-program-swap',
		'https://www.adams12.org/health-services/section-504',
		'https://www.adams12.org/special-education/special-education-parent-resources',
		'https://www.adams12.org/special-education/staff-special-ed-record-request',
		'https://www.adams12.org/special-education/transition-services',
		'https://www.adams12.org/special-education/adult-agency-partnerships',
		'https://www.adams12.org/special-education/contact-transition-services',
		'https://www.adams12.org/programs/stem',
		'https://www.adams12.org/programs/summer-school',
		'https://www.adams12.org/summer-school/high-school-summer-credit-recovery',
		'https://www.adams12.org/summer-school/middle-school-summer-program',
		'https://www.adams12.org/athletics-activities/athletic-facilities',
		'https://www.adams12.org/athletics-activities/high-school-athletics',
		'https://www.adams12.org/departments/athletics-activities/middle-school-activities',
		'https://www.adams12.org/athletics-activities/sports-medicine',
		'https://www.adams12.org/athletics-activities/athletic-trainers',
		'https://www.adams12.org/athletics-activities/concussion-protocol',
		'https://www.adams12.org/programs/base',
		'https://www.adams12.org/base/base-sites',
		'https://www.adams12.org/base/faqs',
		'https://www.adams12.org/base/school-year-base',
		'https://www.adams12.org/base/break-programs',
		'https://www.adams12.org/base/full-day-programs',
		'https://www.adams12.org/base/summer-base',
		'https://www.adams12.org/departments/facilities',
		'https://www.adams12.org/departments/maintenance-and-operations',
		'https://www.adams12.org/services/community-use-facilities',
		'https://www.adams12.org/maintenance-and-operations/custodial-services',
		'https://www.adams12.org/maintenance-and-operations/energy-and-sustainability',
		'https://www.adams12.org/facilities/esc-ev-charging-station',
		'https://www.adams12.org/maintenance-and-operations/greenhouse-gas-inventory-brief',
		'https://www.adams12.org/maintenance-and-operations/sustainability-report',
		'https://www.adams12.org/maintenance-and-operations/environmental-services',
		'https://www.adams12.org/maintenance-and-operations/stormwater',
		'https://www.adams12.org/maintenance-and-operations/water-sampling',
		'https://www.adams12.org/maintenance-and-operations/water-sampling-results',
		'https://www.adams12.org/departments/central-warehouse',
		'https://www.adams12.org/facilities/planning',
		'https://www.adams12.org/facilities/oil-and-gas-info',
		'https://www.adams12.org/facilities/2015-mineral-rights-leases-approved',
		'https://www.adams12.org/facilities/2017-mineral-rights-leases-approved',
		'https://www.adams12.org/facilities/2018-mineral-rights-leases-approved',
		'https://www.adams12.org/facilities/2019-mineral-rights-leases-rejected',
		'https://www.adams12.org/facilities/2019-mineral-rights-leases-rejected',
		'https://www.adams12.org/facilities/design-and-construction',
		'https://www.adams12.org/services/community-use-facilities',
		'https://www.adams12.org/services/community-use-facilities/athletics',
		'https://www.adams12.org/services/community-use-facilities/five-star-stadium',
		'https://www.adams12.org/services/community-use-facilities/north-stadium',
		'https://www.adams12.org/services/community-use-facilities/veterans-memorial-aquatics-center',
		'https://www.adams12.org/services/conference-center',
		'https://www.adams12.org/services/conference-center/conference-center-reservations',
		'https://www.adams12.org/services/conference-center/conference-center-rates-policies',
		'https://www.adams12.org/services/community-use-facilities/aspen',
		'https://www.adams12.org/services/community-use-facilities/blue-spruce',
		'https://www.adams12.org/services/community-use-facilities/cottonwood',
		'https://www.adams12.org/services/community-use-facilities/dogwood',
		'https://www.adams12.org/services/community-use-facilities/pi%C3%B1on-pine',
		'https://www.adams12.org/getinvolved',
		'https://www.adams12.org/getinvolved/volunteering',
		'https://www.adams12.org/parent-groups',
		'https://www.adams12.org/parent-groups/adams-12-kid',
		'https://www.adams12.org/parent-groups/aipac',
		'https://www.adams12.org/dac',
		'https://www.adams12.org/district-accountability-committee/meeting-dates',
		'https://www.adams12.org/parent-groups/district-health-advisory-committee',
		'https://www.adams12.org/parent-groups/finance-and-audit-committee',
		'https://www.adams12.org/parent-groups/gt-parents-group',
		'https://www.adams12.org/parent-groups/hispanic-advisory-council',
		'https://www.adams12.org/parent-groups/leadership-academy',
		'https://www.adams12.org/leadership-academy/fsla-2020-21-materials',
		'https://www.adams12.org/parent-groups/lrpac',
		'https://www.adams12.org/parent-groups/parent-leader-action-network',
		'https://www.adams12.org/parent-leader-action-network/resources-parent-leaders',
		'https://www.adams12.org/parent-groups/special-education-advisory-committee',
		'https://www.adams12.org/departments/health-services',
		'https://www.adams12.org/health-services/health-conditions',
		'https://www.adams12.org/health-services/allergies-and-anaphylaxis',
		'https://www.adams12.org/health-services/asthma',
		'https://www.adams12.org/health-services/diabetes',
		'https://www.adams12.org/health-services/seizure-disorders-and-epilepsy',
		'https://www.adams12.org/health-services/immunizations',
		'https://www.adams12.org/health-services/medications',
		'https://www.adams12.org/health-services/what-do-if-your-child-sick',
		'https://www.adams12.org/health-services/coronavirus-covid-19',
		'https://www.adams12.org/health-services/flu',
		'https://www.adams12.org/departments/health-services/flu-prevention',
		'https://www.adams12.org/health-services/home-based-programs',
		'https://www.adams12.org/health-services/section-504',
		'https://www.adams12.org/departments/nutrition',
		'https://www.adams12.org/nutrition/free-and-reduced-meals',
		'https://www.adams12.org/nutrition/free-and-reduced-meal-questions',
		'https://www.adams12.org/nutrition/menus',
		'https://www.adams12.org/nutrition/special-dietary-needs',
		'https://www.adams12.org/nutrition/wellness-policy',
		'https://www.adams12.org/nutrition/usda-nondiscrimination-statement',
		'https://www.adams12.org/nutrition/civil-rights-policy-and-complaint-form',
		'https://www.adams12.org/departments/student-wellness',
		'https://www.adams12.org/student-wellness/keeping-you-and-your-family-well',
		'https://www.adams12.org/student-wellness/school-wellness-initiatives',
		'https://www.adams12.org/student-wellness/school-based-health-center',
		'https://www.adams12.org/health-strategic-plan',
		'https://www.adams12.org/student-wellness/health-wellness',
		'https://www.adams12.org/student-wellness/whole-school-whole-community-whole-child-wscc',
		'https://www.adams12.org/departments/safety-security',
		'https://www.adams12.org/safety-security/emergency-preparedness',
		'https://www.adams12.org/safety-security/emergency-communications',
		'https://www.adams12.org/safety-security/parent-resources-school-safety',
		'https://www.adams12.org/safety-security/threat-assessment-information-families',
		'https://www.adams12.org/first-responder-partnerships',
		'https://www.adams12.org/counseling/support-students-and-families',
		'https://www.adams12.org/bullying-prevention',
		'https://www.adams12.org/grief-and-loss-resources',
		'https://www.adams12.org/resources-after-tragedy',
		'https://www.adams12.org/counseling/suicide-prevention',
		'https://www.adams12.org/counseling/talking-children-about-gender-identity',
		'https://www.adams12.org/counseling/talking-children-and-youth-about-race-and-racism',
		'https://www.adams12.org/counseling/talking-children-about-violence',
		'https://www.adams12.org/crisis-support-numbers',
		'https://www.adams12.org/programs/student-family-outreach',
		'https://www.adams12.org/student-family-outreach/community-resources',
		'https://www.adams12.org/student-family-outreach/community-resource-directory-links',
		'https://www.adams12.org/student-family-outreach/resources-and-homeless-referral',
		'https://www.adams12.org/programs/homeless-education-title-x',
		'https://www.adams12.org/student-family-outreach/immigration',
		'https://www.adams12.org/departments/information-technology',
		'https://www.adams12.org/data-privacy',
		'https://www.adams12.org/information-technology/data-we-collect-and-why',
		'https://www.adams12.org/information-technology/resources-policies-and-laws',
		'https://www.adams12.org/information-technology/third-party-providers',
		'https://www.adams12.org/information-technology/staff-community-technology-purchase-programs',
		'https://www.adams12.org/departments/intervention-services',
		'https://www.adams12.org/intervention-services/attendance',
		'https://www.adams12.org/intervention-services/chronic-absenteeism',
		'https://www.adams12.org/intervention-services/behavior',
		'https://www.adams12.org/intervention-services/alternative-suspension',
		'https://www.adams12.org/intervention-services/expulsion',
		'https://www.adams12.org/intervention-services/re-engagement',
		'https://www.adams12.org/departments/print-studio',
		'https://www.adams12.org/print-studio/services',
		'https://www.adams12.org/departments/purchasing',
		'https://www.adams12.org/rocky-mountain-e-purchasing-system-bidnet',
		'https://www.adams12.org/departments/purchasing/purchasing-faq',
		'https://www.adams12.org/departments/transportation',
		'https://www.adams12.org/bus-pass',
		'https://www.adams12.org/transportation/spaceavailability',
		'https://www.adams12.org/transportation/safety-procedures',
		'https://www.adams12.org/departments/admissions',
		'https://www.adams12.org/departments/admissions/boundary-locator',
		'https://www.adams12.org/admissions/boundary-maps',
		'https://www.adams12.org/admissions/boundary-process',
		'https://www.adams12.org/admissions/enrollment-questions',
		'https://www.adams12.org/admissions/enrollment-requirements',
		'https://www.adams12.org/admissions/proof-residence',
		'https://www.adams12.org/departments/admissions/home-school',
		'https://www.adams12.org/admissions/international-foreign-exchange-students',
		'http://www.adams12.org/programs/kindergarten',
		'https://www.adams12.org/programs/preschool',
		'https://www.adams12.org/departments/admissions/online-check-in',
		'https://www.adams12.org/online-check/online-check-faqs',
		'https://www.adams12.org/admissions/schools-of-choice-program',
		'https://www.adams12.org/admissions/choice-questions',
		'https://www.adams12.org/admissions/choice-schools',
		'https://www.adams12.org/admissions/choice-windows',
		'https://www.adams12.org/admissions/school-tours',
		'https://www.adams12.org/admissions/school-programs',
		'https://www.adams12.org/admissions/school-transfers',
	]
	# mainfolder = all_sites[0].split('.')[1]
	mainfolder = 'adams12'
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
		school_name = 'adams12'

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
