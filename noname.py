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

		if web_soup.find(id='main-content').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='main-content').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='main-content').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='main-content').find_all(id='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='main-content').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='main-content').find_all(id='news-list') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='main-content') != None and web_soup.find(id='main-content') != '':
			col1 = web_soup.find(id='main-content')
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
		'https://ossiningufsd.org/',
		'https://ossiningufsd.org/contact/',
		'https://ossiningufsd.org/news/2013/11/21/demo-article/',
		'https://ossiningufsd.org/contact/thank-you.html',
		'https://ossiningufsd.org/sitemap.xml',
		'https://ossiningufsd.org/news/2015/03/04/title/',
		'https://ossiningufsd.org/style.css',
		'https://ossiningufsd.org/schools/ohs/',
		'https://ossiningufsd.org/search-results.html',
		'https://ossiningufsd.org/schools/ohs/calendar/',
		'https://ossiningufsd.org/schools/ohs/staff/',
		'https://ossiningufsd.org/schools/ohs/athletics/schedules.html',
		'https://ossiningufsd.org/schools/ohs/clubs-and-organizations/yearbook.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/basketball/',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/cross-country.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/golf.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/football.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/soccer.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/softball.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/swimming.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/tennis.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/volleyball.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/wrestling.html',
		'https://ossiningufsd.org/schools/ohs/pta-septo/',
		'https://ossiningufsd.org/programs/equity/',
		'https://ossiningufsd.org/schools/ohs/library/',
		'https://ossiningufsd.org/schools/ohs/overview.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/college-and-career-planning/',
		'https://ossiningufsd.org/departments/technology/data-privacy.html',
		'https://ossiningufsd.org/schools/roosevelt/principal/',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/forms-and-downloads.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/registration.html',
		'https://ossiningufsd.org/schools/amd/',
		'https://ossiningufsd.org/schools/amd/principal/',
		'https://ossiningufsd.org/schools/amd/calendar/',
		'https://ossiningufsd.org/schools/amd/staff/',
		'https://ossiningufsd.org/schools/amd/overview.html',
		'https://ossiningufsd.org/schools/roosevelt/',
		'https://ossiningufsd.org/schools/roosevelt/about-us/',
		'https://ossiningufsd.org/schools/roosevelt/o-blast/',
		'https://ossiningufsd.org/schools/roosevelt/calendar/',
		'https://ossiningufsd.org/schools/roosevelt/resources.html',
		'https://ossiningufsd.org/schools/roosevelt/staff/',
		'https://ossiningufsd.org/schools/roosevelt/library-media-center/',
		'https://ossiningufsd.org/schools/claremont/',
		'https://ossiningufsd.org/schools/claremont/principal/',
		'https://ossiningufsd.org/schools/ohs/clubs-and-organizations/test.html',
		'https://ossiningufsd.org/schools/claremont/calendar/',
		'https://ossiningufsd.org/schools/claremont/resources/',
		'https://ossiningufsd.org/schools/claremont/staff/',
		'https://ossiningufsd.org/schools/claremont/library-media-center/',
		'https://ossiningufsd.org/schools/brookside/',
		'https://ossiningufsd.org/schools/brookside/principal/',
		'https://ossiningufsd.org/schools/park/about-us.html',
		'https://ossiningufsd.org/schools/brookside/calendar/',
		'https://ossiningufsd.org/schools/brookside/staff/',
		'https://ossiningufsd.org/schools/brookside/media-center/',
		'https://ossiningufsd.org/schools/park/',
		'https://ossiningufsd.org/district/about/',
		'https://ossiningufsd.org/district/',
		'https://ossiningufsd.org/schools/park/calendar/',
		'https://ossiningufsd.org/schools/park/staff/',
		'https://ossiningufsd.org/schools/brookside/brookside-curriculum-newsletters.html',
		'https://ossiningufsd.org/district/leadership.html',
		'https://ossiningufsd.org/district/about/our-community.html',
		'https://ossiningufsd.org/district/about/strategic-plan.html',
		'https://ossiningufsd.org/district/boe/',
		'https://ossiningufsd.org/district/boe/members.html',
		'https://ossiningufsd.org/district/boe/meetings.html',
		'https://ossiningufsd.org/district/boe/agendas.html',
		'https://ossiningufsd.org/district/boe/minutes/',
		'https://ossiningufsd.org/district/boe/policies.html',
		'https://ossiningufsd.org/district/communications/',
		'https://ossiningufsd.org/district/communications/connect-with-us.html',
		'https://ossiningufsd.org/district/communications/o-blast-email.html',
		'https://ossiningufsd.org/district/communications/website-feedback.html',
		'https://ossiningufsd.org/district/fiscal-equity/',
		'https://ossiningufsd.org/district/fiscal-equity/overview.html',
		'https://ossiningufsd.org/district/fiscal-equity/resources.html',
		'https://ossiningufsd.org/district/fiscal-equity/take-action!.html',
		'https://ossiningufsd.org/district/alumni/',
		'https://ossiningufsd.org/district/boe/duplicate-of-board-member-biographies.html',
		'https://ossiningufsd.org/district/voter-registration/overview.html',
		'https://ossiningufsd.org/programs/',
		'https://ossiningufsd.org/programs/community-partnership/',
		'https://ossiningufsd.org/programs/dasa/',
		'https://ossiningufsd.org/programs/oprime.html',
		'https://ossiningufsd.org/programs/first-steps/',
		'https://ossiningufsd.org/departments/',
		'https://ossiningufsd.org/departments/business/',
		'https://ossiningufsd.org/departments/business/food-services/overview.html',
		'https://ossiningufsd.org/departments/business/food-services/menu.html',
		'https://ossiningufsd.org/departments/transportation.html',
		'https://ossiningufsd.org/departments/curriculum-and-assessment/',
		'https://ossiningufsd.org/departments/enl-program/',
		'https://ossiningufsd.org/departments/enl-program/overview-staff.html',
		'https://ossiningufsd.org/departments/enl-program/resources.html',
		'https://ossiningufsd.org/departments/health-services/',
		'https://ossiningufsd.org/departments/health-services/overview-staff.html',
		'https://ossiningufsd.org/departments/health-services/sick-day-guidelines.html',
		'https://ossiningufsd.org/departments/health-services/immunization-requirements.html',
		'https://ossiningufsd.org/departments/health-services/physical-form.html',
		'https://ossiningufsd.org/departments/health-services/medication-form.html',
		'https://ossiningufsd.org/departments/health-services/resources.html',
		'https://ossiningufsd.org/departments/human-resources/',
		'https://ossiningufsd.org/departments/human-resources/overview.html',
		'https://ossiningufsd.org/departments/human-resources/benefits.html',
		'https://ossiningufsd.org/departments/human-resources/eval-dev.html',
		'https://ossiningufsd.org/departments/human-resources/teachers-association.html',
		'https://ossiningufsd.org/departments/human-resources/forms.html',
		'https://ossiningufsd.org/schools/ohs/student-tech-support.html',
		'https://ossiningufsd.org/departments/human-resources/support-staff-information.html',
		'https://ossiningufsd.org/departments/technology/',
		'https://ossiningufsd.org/departments/technology/assessment-and-curriculum/',
		'https://ossiningufsd.org/schools/ohs/ossining-athletics-department/',
		'https://ossiningufsd.org/district/three-year-plan.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/ossining-profile.html',
		'https://ossiningufsd.org/district/boe/minutes/2017-2018.html',
		'https://ossiningufsd.org/departments/technology/parent-resources.html',
		'https://ossiningufsd.org/departments/technology/student-resources.html',
		'https://ossiningufsd.org/departments/technology/staff.html',
		'https://ossiningufsd.org/activities/',
		'https://ossiningufsd.org/activities/athletics/',
		'https://ossiningufsd.org/activities/cultural-arts.html',
		'https://ossiningufsd.org/students/',
		'https://ossiningufsd.org/students/google.html',
		'https://ossiningufsd.org/students/infinite-campus.html',
		'https://ossiningufsd.org/staff/',
		'https://ossiningufsd.org/staff/infinite-campus.html',
		'https://ossiningufsd.org/staff/hr-forms/',
		'https://ossiningufsd.org/calendar',
		'https://ossiningufsd.org/parents/',
		'https://ossiningufsd.org/schools/ohs/resources/portal-assistance.html',
		'https://ossiningufsd.org/parents/lunch-menus.html',
		'https://ossiningufsd.org/parents/staff-directory.html',
		'https://ossiningufsd.org/parents/board-of-education/',
		'https://ossiningufsd.org/staff/appr.html',
		'https://ossiningufsd.org/calendars.html',
		'https://ossiningufsd.org/schools.html',
		'https://ossiningufsd.org/schools/ohs/departments/',
		'https://ossiningufsd.org/staff-directory/',
		'https://ossiningufsd.org/departments/human-resources/compliance-and-policies.html',
		'https://ossiningufsd.org/page-not-found.html',
		'https://ossiningufsd.org/oblast/',
		'https://ossiningufsd.org/appfeed.rss',
		'https://ossiningufsd.org/schools/amd/signup-for-o-blast.html',
		'https://ossiningufsd.org/schools/claremont/signup-for-o-blast.html',
		'https://ossiningufsd.org/schools/roosevelt/signup-for-o-blast.html',
		'https://ossiningufsd.org/schools/park/signup-for-o-blast.html',
		'https://ossiningufsd.org/schools/brookside/signup-for-o-blast.html',
		'https://ossiningufsd.org/schools/park/resources.html',
		'https://ossiningufsd.org/schools/brookside/resources/',
		'https://ossiningufsd.org/parents/registration.html',
		'https://ossiningufsd.org/schools/claremont/photos-and-videos.html',
		'https://ossiningufsd.org/schools/ohs/staff-tester.html',
		'https://ossiningufsd.org/schools/amd/resources/',
		'https://ossiningufsd.org/district/2021-2022-budget/',
		'https://ossiningufsd.org/district/boe/nominating-petitions-for-board-of-education-candidates.html',
		'https://ossiningufsd.org/schools/brookside/principal/blog.html',
		'https://ossiningufsd.org/schools/ohs/resources/',
		'https://ossiningufsd.org/district/voter-registration/absentee-ballot.html',
		'https://ossiningufsd.org/programs/first-steps/resources.html',
		'https://ossiningufsd.org/programs/first-steps/sevices.html',
		'https://ossiningufsd.org/programs/dasa/overview.html',
		'https://ossiningufsd.org/departments/business/budget/2014-2015.html',
		'https://ossiningufsd.org/departments/business/budget/2012-2013.html',
		'https://ossiningufsd.org/departments/business/budget/2013-2014.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/staff.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/special-education.html',
		'https://ossiningufsd.org/site-map.html',
		'https://ossiningufsd.org/schools/ohs/departments/athletic-department.html',
		'https://ossiningufsd.org/departments/special-education/',
		'https://ossiningufsd.org/departments/human-resources/aesop.html',
		'https://ossiningufsd.org/departments/special-education/related-services.html',
		'https://ossiningufsd.org/departments/special-education/overview.html',
		'https://ossiningufsd.org/departments/special-education/eligibility-classifications.html',
		'https://ossiningufsd.org/departments/special-education/special-education-process.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/academic-success.html',
		'https://ossiningufsd.org/schools/ohs/athletics/contact.html',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/family-vacation-policy.html',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/how-to-get-involved.html',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/program-philosophy.html',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/playing-time-policy.html',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/sportsmanship-guidelines.html',
		'https://ossiningufsd.org/staff-search-test.html',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/uniform/equipment-policy.html',
		'https://ossiningufsd.org/schools/ohs/athletics/policies-forms/concussion.html',
		'https://ossiningufsd.org/schools/ohs/athletics/coaches/',
		'https://ossiningufsd.org/schools/ohs/athletics/boosters.html',
		'https://ossiningufsd.org/schools/ohs/athletics/photos-and-videos/2012-sports-photos.html',
		'https://ossiningufsd.org/schools/ohs/athletics/photos-and-videos/2013-sports-photos.html',
		'https://ossiningufsd.org/schools/ohs/athletics/photos-and-videos/2014-sports-photos.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/baseball.html',
		'https://ossiningufsd.org/district/2016-2017-budget.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/boys-lacrosse.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/boys-soccer.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/cheerleading.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/field-hockey.html',
		'https://ossiningufsd.org/district/boe/minutes/2019-2020.html',
		'https://ossiningufsd.org/schools/ohs/prestigious-science-research-program!.html',
		'https://ossiningufsd.org/schools/ohs/ap-exams/',
		'https://ossiningufsd.org/schools/ohs/ap-exams/ap-exams-new.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/girls-lacrosse.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/girls-soccer.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/gymnastics.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/hockey.html',
		'https://ossiningufsd.org/schools/ohs/athletics/sports/track-and-field.html',
		'https://ossiningufsd.org/schools/ohs/departments/attendance.html',
		'https://ossiningufsd.org/schools/ohs/departments/business/',
		'https://ossiningufsd.org/schools/ohs/departments/cultural-arts.html',
		'https://ossiningufsd.org/schools/ohs/departments/english.html',
		'https://ossiningufsd.org/schools/ohs/departments/esl.html',
		'https://ossiningufsd.org/schools/ohs/departments/health.html',
		'https://ossiningufsd.org/schools/ohs/departments/math.html',
		'https://ossiningufsd.org/schools/ohs/departments/nurses-office.html',
		'https://ossiningufsd.org/schools/ohs/departments/technology.html',
		'https://ossiningufsd.org/schools/ohs/departments/physical-education.html',
		'https://ossiningufsd.org/schools/ohs/departments/science.html',
		'https://ossiningufsd.org/schools/ohs/departments/science-researc.html',
		'https://ossiningufsd.org/schools/ohs/departments/social-studies.html',
		'https://ossiningufsd.org/schools/ohs/departments/world-languages.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/naviance/',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/incoming-freshmen.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/program-of-studies.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/campus-portal-instructions.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/college-and-career-planning/colleges-of-ohs-graduates.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/community-service-requirement.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/guidance-plan.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/prom-and-graduation-saftey.html',
		'https://ossiningufsd.org/district/2020-2021-budget/',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/homework-and-study-guide-resources.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/parent/guardian-presentations.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/class-profile.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/esl-resources.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/college-and-career-planning/college-application-process.html',
		'https://ossiningufsd.org/district/2021-2022-budget/duplicate-of-2019-2020-budget/',
		'https://ossiningufsd.org/schools/ohs/clubs-and-organizations/national-honor-society.html',
		'https://ossiningufsd.org/schools/park/parents.html',
		'https://ossiningufsd.org/district/about/school-of-distinction.html',
		'https://ossiningufsd.org/schools/ohs/resources/ptsa.html',
		'https://ossiningufsd.org/staff-directory/ohs-staff.html',
		'https://ossiningufsd.org/schools/ohs/resources/diginity-for-all-students.html',
		'https://ossiningufsd.org/schools/ohs/resources/ipad-app-request-form.html',
		'https://ossiningufsd.org/schools/ohs/resources/teacher-mentor-program.html',
		'https://ossiningufsd.org/schools/park/first-steps.html',
		'https://ossiningufsd.org/schools/amd/amd-announcements.html',
		'https://ossiningufsd.org/schools/ohs/athletics/coaches/athletic-trainer.html',
		'https://ossiningufsd.org/schools/amd/open-door.html',
		'https://ossiningufsd.org/schools/claremont/archived-o-blasts.html',
		'https://ossiningufsd.org/staff-directory/amd-staff.html',
		'https://ossiningufsd.org/staff-directory/roosevelt-staff.html',
		'https://ossiningufsd.org/staff-directory/claremont-staff.html',
		'https://ossiningufsd.org/staff-directory/brookside-staff.html',
		'https://ossiningufsd.org/staff-directory/park-staff.html',
		'https://ossiningufsd.org/schools/ohs/ohs-announcements.html',
		'https://ossiningufsd.org/combined-calendar-test.html',
		'https://ossiningufsd.org/students/registration.html',
		'https://ossiningufsd.org/combined-calendar-test-2.html',
		'https://ossiningufsd.org/privacy-policy.html',
		'https://ossiningufsd.org/schools/ohs/guidance.html',
		'https://ossiningufsd.org/district/emergency-procedures/',
		'https://ossiningufsd.org/district/boe/board-presentations.html',
		'https://ossiningufsd.org/test-contact/test-school-home.html',
		'https://ossiningufsd.org/district/advocacy/',
		'https://ossiningufsd.org/schools/ohs/departments/capstone.html',
		'https://ossiningufsd.org/schools/park/library-media-center.html',
		'https://ossiningufsd.org/programs/wellness.html',
		'https://ossiningufsd.org/basics',
		'https://ossiningufsd.org/programs/parent-leadership-institute.html',
		'https://ossiningufsd.org/district/boe/minutes/2016-2017.html',
		'https://ossiningufsd.org/district/2017-2018-budget.html',
		'https://ossiningufsd.org/district/boe/minutes/2018-2019.html',
		'https://ossiningufsd.org/schools/ohs/**new-bell-schedule**.html',
		'https://ossiningufsd.org/schools/amd/amd-bell-schedule.html',
		'https://ossiningufsd.org/schools/ohs/program-of-studies.html',
		'https://ossiningufsd.org/departments/technology/web-site-accessibility-guidelines.html',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/infinite-campus-portal.html',
		'https://ossiningufsd.org/schools/ohs/student-equity.html',
		'https://ossiningufsd.org/programs/saturday-explore-and-learn-(sel).html',
		'https://ossiningufsd.org/district/2020-2021-budget/2019-2020-budget/',
		'https://ossiningufsd.org/schools/ohs/departments/counseling/resources/substance-prevention.html',
		'https://ossiningufsd.org/programs/my-brothers-keeper-program.html',
		'https://ossiningufsd.org/district/health-and-wellness-coronavirus/',
		'https://ossiningufsd.org/district/boe/minutes/2020-2021-press-releases-and-minutes.html',
		'https://ossiningufsd.org/parents/online-registration.html',
		'https://ossiningufsd.org/schools/ohs/empowering-us!.html',
		'https://ossiningufsd.org/district/summer-programs-2020/duplicate-of-2019-2020-budget/',
		'https://ossiningufsd.org/staff/professional-development.html',
		'https://ossiningufsd.org/district/district-fields-usage-calendar/',
		'https://ossiningufsd.org/schools/amd/amd-morning-announcements.html',
		'https://ossiningufsd.org/schools/amd/amd-library-media-center.html',
		'https://ossiningufsd.org/schools/park/park-social-emotional-learning.html',
		'https://ossiningufsd.org/programs/virtual-family-resource-center.html',
		'https://ossiningufsd.org/departments/technology/online-registration.html',
		'https://ossiningufsd.org/parents/prek-online-registration.html',
		'https://ossiningufsd.org/schools/park/registration.html',
		'https://ossiningufsd.org/district/boe/about-the-board-of-education-and-mission-statement.html',
		'https://ossiningufsd.org/schools/ohs/clubs-and-organizations.html',
		'https://ossiningufsd.org/schools/ohs/cultural-arts/',
	]
	# mainfolder = all_sites[0].split('.')[1]
	mainfolder = 'ossiningufsd'
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
		school_name = 'ossiningufsd'

		csv_report.writerow(['School name', school_name])

		with open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
			csv_writer = csv.writer(csv_main)
			csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

			for link in all_sites:
				tiers = link.split('/')
				t1, t2, t3, t4, t5 = '', '', '', '', ''
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
				else:
					print(len(tiers))

				page_link = link

				page_counter += 1
				col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
				issue_pages_counter += content_ipc

				csv_writer.writerow([str(page_link), t1, t2, t3, t4, t5, col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

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
