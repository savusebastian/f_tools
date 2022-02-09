from pathlib import Path
from time import time
import csv

from bs4 import BeautifulSoup
import requests

from util import get_column


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

		if web_soup.find(class_='content').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='content').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='content').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='content').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='content').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='content').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='content') != None and web_soup.find(class_='content') != '':
			col1 = web_soup.find(class_='content')
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
		'https://www.pvschools.net/about/about-us',
		'https://www.pvschools.net/about/about-us/pvschools-district-administration',
		'https://www.pvschools.net/about/governing-board',
		'https://www.pvschools.net/election',
		'https://www.pvschools.net/about/nutrition-and-wellness',
		'https://www.pvschools.net/about/transportation/bus-stop-locations-times',
		'https://www.pvschools.net/about/transportation/bus-drivers-aides',
		'https://www.pvschools.net/academics/academic-programs/dual-enrollment',
		'https://www.pvschools.net/academics/academic-programs/fine-arts-education/north-valley-arts-academies',
		'https://www.pvschools.net/academics/college-career',
		'https://www.pvschools.net/about/budget-and-finance/title-1-schools',
		'https://www.pvschools.net/about/budget-and-finance/title-1-schools/education-services-homeless-mckinney-vento-act',
		'https://www.pvschools.net/academics/academic-programs/ap-programs',
		'https://www.pvschools.net/academics/academic-programs/career-and-technical-education',
		'https://www.pvschools.net/academics/academic-programs/career-and-technical-education/cte-program-offerings',
		'https://www.pvschools.net/academics/academic-programs/career-and-technical-education/cte-alumni-where-are-they-now',
		'https://www.pvschools.net/academics/academic-programs/international-baccalaureate',
		'https://www.pvschools.net/academics/academic-programs/language-immersion',
		'https://www.pvschools.net/academics/academic-programs/special-education/vision-department',
		'https://www.pvschools.net/about/budget-and-finance/title-1-schools',
		'https://www.pvschools.net/academics/curriculum/k-8-social-studies-adoption',
		'https://www.pvschools.net/academics/curriculum/9-12-math-adoption',
		'https://www.pvschools.net/academics/academic-programs/language-immersion',
		'https://www.pvschools.net/academics/athletics-and-physical-education/middle-school-athletics',
		'https://www.pvschools.net/academics/athletics-and-physical-education/middle-school-athletics/athletes-and-parents',
		'https://www.pvschools.net/academics/academic-services/online-gradebook',
		'https://www.pvschools.net/enrollment/enrollment-packet',
		'https://www.pvschools.net/enrollment/enrollment-packet/in-person-online-options',
		'https://www.pvschools.net/enrollment/open-enrollment',
		'https://www.pvschools.net/enrollment/enrollment-packet/locate-school',
		'https://www.pvschools.net/community-education/summer-programs',
		'https://www.pvschools.net/community-education/summer-programs/high-school-summer-school',
		'https://www.pvschools.net/join-pv/pvschools-hiring',
		'https://www.pvschools.net/join-pv/donate-pvschools',
		'https://www.pvschools.net/join-pv/volunteer-pvschools',
		'https://www.pvschools.net/join-pv/volunteer-paradise',
		'https://www.pvschools.net/join-pv/pvschools-flyer-partnership-program',
		'https://www.pvschools.net/join-pv/pvschools-flyer-partnership-program/flyer-partner-resources',
		'https://www.pvschools.net/community-education/facility-and-field-use',
		'https://www.pvschools.net/about/contact-pvschools',
		'https://www.pvschools.net/about/budget-and-finance/website-accessibility-notice',
		'https://www.pvschools.net/about/success-stories/shadow-mountain-graduates-return-open-restaurant',
		'https://www.pvschools.net/academics/curriculum/pvschools-preschool-kindergarten/kindergarten-open-houses',
		'https://www.pvschools.net/newscenter/daily-point-light-awarded-vip-cathy-mckeever',
		'https://www.pvschools.net/newscenter/horizon-high-girls-volleyball-takes-2021-aia-5a-championship-title',
		'https://www.pvschools.net/newscenter/message-office-superintendent',
		'https://www.pvschools.net/newscenter/update-pvschools-prepared-plan',
		'https://www.pvschools.net/newscenter/student-spotlight-claire-severs',
		'https://www.pvschools.net/newscenter/so-whats-problem',
		'https://www.pvschools.net/newscenter/tax-credit-contributions-its-win-win-you-and-students',
		'https://www.pvschools.net/newscenter/helping-our-neighbors-paradise-valley-emergency-food-bank',
		'https://www.pvschools.net/newscenter/student-mission-creating-future-success',
		'https://www.pvschools.net/newscenter/depth-quail-run-elementarys-international-baccalaureate',
		'https://www.pvschools.net/newscenter/paradise-valley-high-crest-teacher-named-2021-asta-high-school-teacher-year',
		'https://www.pvschools.net/newscenter/curriculum-section-process-top-10-steps',
		'https://www.pvschools.net/newscenter/paradise-valley-high-school-students-honored-college-board-national-recognition-programs',
		'https://www.pvschools.net/newscenter/pvwit-conversation-isabella-swanson',
		'https://www.pvschools.net/newscenter/20-pvschools-seniors-named-2022-national-merit-commended-students',
		'https://www.pvschools.net/newscenter/6-pvschools-seniors-named-2022-national-merit-semifinalists',
		'https://www.pvschools.net/newscenter/fafsa-process-what-parents-and-seniors-need-know',
		'https://www.pvschools.net/newscenter/join-band-marching-success',
		'https://www.pvschools.net/newscenter/artist-spotlight-laura-syjud-suzuki-strings-teacher',
		'https://www.pvschools.net/newscenter/space-exploration-pv-crest-senior-creates-mural-space-center',
		'https://www.pvschools.net/newscenter/school-art-murals-phoenix-scottsdale',
		'https://www.pvschools.net/newscenter/showcasing-arts-pvschools-conversation-maureen-minnick',
		'https://www.pvschools.net/newscenter/open-enrollment-2022-23-how-it-works',
		'https://www.pvschools.net/newscenter/desk-conversation-superintendent-dr-bales',
		'https://www.pvschools.net/newscenter/going-behind-scenes-teachers-head-back-classroom',
		'https://www.pvschools.net/newscenter/school-lunch-conversation-director-nutrition-and-wellness-camille-unruh',
		'https://www.pvschools.net/newscenter/your-journey-excellence-continues-welcome-2021-22-students-and-families',
		'https://www.pvschools.net/newscenter/experience-everyonechoose-your-journey-pvschools',
		'https://www.pvschools.net/newscenter/welcome-paradise-pvschools-announces-new-administrators-2021-22-school-year',
		'https://www.pvschools.net/newscenter/benefits-dual-language-immersion-program',
		'https://www.pvschools.net/newscenter/why-being-time-school-matters-tips-get-your-child-school-time',
		'https://www.pvschools.net/newscenter/advantages-learning-second-language-early-age',
		'https://www.pvschools.net/newscenter/why-learn-mandarin-top-5-reasons',
		'https://www.pvschools.net/newscenter/take-mystery-out-middle-school-debunking-middle-school-myths',
		'https://www.pvschools.net/newscenter/paradise-valley-high-crest-student-first-robotics-competition-deans-list-finalist',
		'https://www.pvschools.net/newscenter/how-nail-nightly-homework',
		'https://www.pvschools.net/newscenter/mastering-art-organization',
		'https://www.pvschools.net/newscenter/bullying-and-suicide-awareness-guidance-and-resources',
		'https://www.pvschools.net/newscenter/bus-rider-safety-tips-0',
		'https://www.pvschools.net/newscenter/how-keep-learning-and-thriving-during-summer-vacation',
		'https://www.pvschools.net/newscenter/horizon-high-and-north-canyon-high-are-aia-division-ii-track-field-state-champions',
		'https://www.pvschools.net/newscenter/2-pv-students-named-co-champions-maricopa-county-regional-ii-spelling-bee',
		'https://www.pvschools.net/newscenter/copper-canyon-elementary-student-takes-home-maricopa-county-regional-ii-spelling-bee',
		'https://www.pvschools.net/newscenter/science-behind-leap-year',
		'https://www.pvschools.net/newscenter/role-curriculum-specialists-education',
		'https://www.pvschools.net/newscenter/shadow-mountain-high-school-afjrotc-program-designated-us-space-force',
		'https://www.pvschools.net/newscenter/shadow-mountain-principal-receives-amea-outstanding-administrator-award',
		'https://www.pvschools.net/newscenter/how-school-communities-are-helping-students-during-pandemic',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-education-philosophy',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/curriculum-goals-objectives',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-testing-information ',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-testing-information/gifted-programs-testing',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-testing-information/should-my-child-be-tested',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/application-forms',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-and-talented-preschool-program',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/elementary-school-programs-0',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/elementary-school-programs-0/schoolwide-cluster',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/elementary-school-programs-0/content-replacement-honors',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/self-contained-gifted-programs',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/kindergarten-self-contained-gifted-and-talented',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/self-contained-grades-1-6',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/middle-school-programs',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/middle-school-programs/digital-learning-center',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/middle-school-programs/journey-middle-school-program',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/high-school-student-programs',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-education-parent-resources',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-education-parent-resources/characteristics-and',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/teacher-resources',
		'https://www.pvschools.net/academics/academic-programs/gifted-programs/gifted-tours',
		'https://www.pvschools.net/schools/boulder-creek-elementary/our-school/about-our-school',
		'https://www.pvschools.net/schools/boulder-creek-elementary/our-school/school-council',
		'https://www.pvschools.net/schools/boulder-creek-elementary/our-school/parent-student-resources',
		'https://www.pvschools.net/schools/boulder-creek-elementary/services/health-and-nutrition',
		'https://www.pvschools.net/schools/boulder-creek-elementary/academics/instruction',
		'https://www.pvschools.net/schools/boulder-creek-elementary/academics/instruction/kindergarten',
		'https://www.pvschools.net/schools/boulder-creek-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/cactus-view-elementary/our-school/overview',
		'https://www.pvschools.net/schools/cactus-view-elementary/our-school/about-our-principal/cactus-view-school-council',
		'https://www.pvschools.net/schools/cactus-view-elementary/services/publications',
		'https://www.pvschools.net/schools/cactus-view-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/cactus-view-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/cactus-view-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/campo-bello-elementary/our-school/overview',
		'https://www.pvschools.net/schools/campo-bello-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/campo-bello-elementary/services/emergency-preparedness',
		'https://www.pvschools.net/schools/campo-bello-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/campo-bello-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/campo-bello-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/copper-canyon-elementary/our-school/copper-canyons-vision-mission-and-values',
		'https://www.pvschools.net/schools/copper-canyon-elementary/our-school/principals-welcome/school-council',
		'https://www.pvschools.net/schools/copper-canyon-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/copper-canyon-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/copper-canyon-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/copper-canyon-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/desert-cove-elementary/our-school/overview',
		'https://www.pvschools.net/schools/desert-cove-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/desert-cove-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/desert-cove-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/desert-cove-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/desert-cove-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/desert-shadows-elementary/our-school/overview',
		'https://www.pvschools.net/schools/desert-shadows-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/desert-shadows-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/desert-shadows-elementary/services/transportation',
		'https://www.pvschools.net/schools/desert-shadows-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/desert-shadows-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/desert-shadows-elementary/academics/enrichment',
		'https://www.pvschools.net/schools/desert-shadows-middle/our-school/overview',
		'https://www.pvschools.net/schools/desert-shadows-middle/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/desert-shadows-middle/our-school/principals-page/school-counselors',
		'https://www.pvschools.net/schools/desert-shadows-middle/our-school/dsms-highlights',
		'https://www.pvschools.net/schools/desert-shadows-middle/academics/electives/7th-grade-electives',
		'https://www.pvschools.net/schools/desert-shadows-middle/academics/electives/8th-grade-electives',
		'https://www.pvschools.net/schools/desert-shadows-middle/academics/dsms-academies',
		'https://www.pvschools.net/schools/desert-shadows-middle/extracurricular/dsms-athletics',
		'https://www.pvschools.net/schools/desert-springs-preparatory/our-school/overview',
		'https://www.pvschools.net/schools/desert-springs-preparatory/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/desert-springs-preparatory/our-school/parents-page',
		'https://www.pvschools.net/schools/desert-springs-preparatory/services/nurses-office',
		'https://www.pvschools.net/schools/desert-springs-preparatory/academics/curriculum',
		'https://www.pvschools.net/schools/desert-springs-preparatory/academics/physical-education-desert-springs',
		'https://www.pvschools.net/schools/desert-springs-preparatory/our-school/overview/and-after-school-classes',
		'https://www.pvschools.net/schools/desert-springs-preparatory/academics/and-after-school-classes',
		'https://www.pvschools.net/schools/desert-trails-elementary/our-school/overview',
		'https://www.pvschools.net/schools/desert-trails-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/desert-trails-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/desert-trails-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/desert-trails-elementary/services/safety',
		'https://www.pvschools.net/schools/desert-trails-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/desert-trails-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/eagle-ridge-elementary/our-school/overview',
		'https://www.pvschools.net/schools/eagle-ridge-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/eagle-ridge-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/eagle-ridge-elementary/services/nurses-notes',
		'https://www.pvschools.net/schools/eagle-ridge-elementary/academics/enrichment',
		'https://www.pvschools.net/schools/eagle-ridge-elementary/our-school/overview/attendance',
		'https://www.pvschools.net/schools/echo-mountain-intermediate/our-school/overview',
		'https://www.pvschools.net/schools/echo-mountain-intermediate/our-school/overview/behavior-program',
		'https://www.pvschools.net/schools/echo-mountain-intermediate/our-school/principals-bio/school-council',
		'https://www.pvschools.net/schools/echo-mountain-intermediate/our-school/kids-corner',
		'https://www.pvschools.net/schools/echo-mountain-intermediate/services/nurses-office',
		'https://www.pvschools.net/schools/echo-mountain-intermediate/academics/curriculum',
		'https://www.pvschools.net/schools/echo-mountain-intermediate/academics/signature-programs',
		'https://www.pvschools.net/schools/echo-mountain-primary/our-school/overview',
		'https://www.pvschools.net/schools/echo-mountain-primary/our-school/overview/make-your-day',
		'https://www.pvschools.net/schools/echo-mountain-primary/our-school/principals-page',
		'https://www.pvschools.net/schools/echo-mountain-primary/our-school/kids-corner',
		'https://www.pvschools.net/schools/echo-mountain-primary/academics/curriculum/supply-lists',
		'https://www.pvschools.net/schools/echo-mountain-primary/services/nurses-office',
		'https://www.pvschools.net/schools/echo-mountain-primary/academics/signature-programs',
		'https://www.pvschools.net/schools/echo-mountain-primary/academics/media-center-and-technology',
		'https://www.pvschools.net/schools/explorer-middle/our-school/overview',
		'https://www.pvschools.net/schools/explorer-middle/our-school/overview/attendance',
		'https://www.pvschools.net/schools/explorer-middle/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/explorer-middle/our-school/parent-resources',
		'https://www.pvschools.net/schools/explorer-middle/services/academic-services',
		'https://www.pvschools.net/schools/explorer-middle/services/nurses-office',
		'https://www.pvschools.net/schools/explorer-middle/academics/signature-programs/career-and-technology-education',
		'https://www.pvschools.net/schools/explorer-middle/academics/signature-programs/visual-and-performing-arts',
		'https://www.pvschools.net/schools/fireside-elementary/our-school/attendance-and-registration',
		'https://www.pvschools.net/schools/fireside-elementary/join-us/support-our-school/fireside-elementary-school-council',
		'https://www.pvschools.net/schools/fireside-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/fireside-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/fireside-elementary/services/emergency-preparedness',
		'https://www.pvschools.net/schools/fireside-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/fireside-elementary/academics/gifted-programs',
		'https://www.pvschools.net/schools/grayhawk-elementary/our-school/overview',
		'https://www.pvschools.net/schools/grayhawk-elementary/our-school/overview/attendance-and-registration',
		'https://www.pvschools.net/schools/grayhawk-elementary/our-school/leadership',
		'https://www.pvschools.net/schools/grayhawk-elementary/our-school/parents/supply-lists',
		'https://www.pvschools.net/schools/grayhawk-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/grayhawk-elementary/academics/core-knowledge',
		'https://www.pvschools.net/schools/greenway-middle/our-school/overview',
		'https://www.pvschools.net/schools/greenway-middle/our-school/attendance-information',
		'https://www.pvschools.net/schools/greenway-middle/our-school/leadership/site-council',
		'https://www.pvschools.net/schools/greenway-middle/services/health-and-nutrition',
		'https://www.pvschools.net/schools/greenway-middle/services/emergency-response-planning',
		'https://www.pvschools.net/schools/greenway-middle/academics/academic-services',
		'https://www.pvschools.net/schools/greenway-middle/academics/instruction-curriculum',
		'https://www.pvschools.net/schools/greenway-middle/academics/avid',
		'https://www.pvschools.net/schools/hidden-hills-elementary/our-school/overview',
		'https://www.pvschools.net/schools/hidden-hills-elementary/our-school/principals-page/schoolsite-council',
		'https://www.pvschools.net/schools/hidden-hills-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/hidden-hills-elementary/services/health-and-wellness',
		'https://www.pvschools.net/schools/hidden-hills-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/hidden-hills-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/horizon-high/our-school/horizon-school-profile',
		'https://www.pvschools.net/schools/horizon-high/our-school/administrative-profiles/horizon-school-council',
		'https://www.pvschools.net/schools/horizon-high/our-school/attendance',
		'https://www.pvschools.net/schools/horizon-high/our-school/student-life-and-registration',
		'https://www.pvschools.net/schools/horizon-high/services/emergency-preparedness',
		'https://www.pvschools.net/schools/horizon-high/services/emergency-preparedness/behavior',
		'https://www.pvschools.net/schools/horizon-high/services/academic-services',
		'https://www.pvschools.net/schools/horizon-high/academics/signature-program',
		'https://www.pvschools.net/schools/horizon-high/extracurricular/huskies-home',
		'https://www.pvschools.net/schools/horizon-high/extracurricular/clubs-and-organizations',
		'https://www.pvschools.net/schools/horizon-high/newscenter/charles-everroad-named-2022-national-merit-commended-student',
		'https://www.pvschools.net/schools/horizon-high/newscenter/girls-volleyball-state-champions',
		'https://www.pvschools.net/schools/indian-bend-elementary/our-school/overview',
		'https://www.pvschools.net/schools/indian-bend-elementary/our-school/overview/attendance',
		'https://www.pvschools.net/schools/indian-bend-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/indian-bend-elementary/our-school/parents',
		'https://www.pvschools.net/schools/indian-bend-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/indian-bend-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/indian-bend-elementary/academics/instruction',
		'https://www.pvschools.net/schools/indian-bend-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/larkspur-elementary/our-school/attendance',
		'https://www.pvschools.net/schools/larkspur-elementary/join-us/support-our-school/school-council',
		'https://www.pvschools.net/schools/larkspur-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/larkspur-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/larkspur-elementary/services/emergency-preparedness',
		'https://www.pvschools.net/schools/larkspur-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/liberty-elementary/our-school/overview',
		'https://www.pvschools.net/schools/liberty-elementary/our-school/principals-welcome/school-council',
		'https://www.pvschools.net/schools/liberty-elementary/our-school/attendance-and-bell-schedule',
		'https://www.pvschools.net/schools/liberty-elementary/our-school/student-resources',
		'https://www.pvschools.net/schools/liberty-elementary/services/health-and-nutrition',
		'https://www.pvschools.net/schools/liberty-elementary/services/transportation',
		'https://www.pvschools.net/schools/liberty-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/liberty-elementary/academics/gifted-programs',
		'https://www.pvschools.net/schools/liberty-elementary/academics/gifted-programs',
		'https://www.pvschools.net/schools/mercury-mine-elementary/our-school/overview',
		'https://www.pvschools.net/schools/mercury-mine-elementary/our-school/overview/attendance-and-registration',
		'https://www.pvschools.net/schools/mercury-mine-elementary/our-school/principals-page/mmes-school-council',
		'https://www.pvschools.net/schools/mercury-mine-elementary/services/nurses-office',
		'https://www.pvschools.net/schools/mercury-mine-elementary/academics/core-knowledge-curriculum',
		'https://www.pvschools.net/schools/mercury-mine-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/mountain-trail-middle/our-school/about-mtms',
		'https://www.pvschools.net/schools/mountain-trail-middle/services/academic-services/media-center',
		'https://www.pvschools.net/schools/mountain-trail-middle/our-school/principals-welcome/school-council',
		'https://www.pvschools.net/schools/mountain-trail-middle/our-school/pv-learners',
		'https://www.pvschools.net/schools/mountain-trail-middle/services/nurses-office',
		'https://www.pvschools.net/schools/mountain-trail-middle/services/safety',
		'https://www.pvschools.net/schools/mountain-trail-middle/services/academic-services/9th-hour-homework-help',
		'https://www.pvschools.net/schools/mountain-trail-middle/services/student-resource-center',
		'https://www.pvschools.net/schools/mountain-trail-middle/extracurricular/mtms-athletics',
		'https://www.pvschools.net/schools/mountain-trail-middle/extracurricular/clubs-and-activities/njhs',
		'https://www.pvschools.net/schools/mountain-trail-middle/academics/curriculum/7th-grade-courses',
		'https://www.pvschools.net/schools/mountain-trail-middle/academics/curriculum/8th-grade-courses',
		'https://www.pvschools.net/schools/mountain-trail-middle/join-us/mtms-ptso',
		'https://www.pvschools.net/schools/north-canyon-high/our-school/overview',
		'https://www.pvschools.net/schools/north-canyon-high/our-school/overview/attendance',
		'https://www.pvschools.net/schools/north-canyon-high/services/academic-services',
		'https://www.pvschools.net/schools/north-canyon-high/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/north-canyon-high/our-school/student-life',
		'https://www.pvschools.net/schools/north-canyon-high/our-school/student-life/rattler-rise',
		'https://www.pvschools.net/schools/north-canyon-high/services/academic-services/bookstore',
		'https://www.pvschools.net/schools/north-canyon-high/services/nurses-office',
		'https://www.pvschools.net/schools/north-canyon-high/services/safety',
		'https://www.pvschools.net/schools/north-canyon-high/extracurricular/rattlers-home',
		'https://www.pvschools.net/schools/north-canyon-high/extracurricular/clubs-and-Activities',
		'https://www.pvschools.net/schools/north-canyon-high/our-school/student-life/senior-info',
		'https://www.pvschools.net/schools/north-canyon-high/academics/signature-programs',
		'https://www.pvschools.net/schools/north-canyon-high/academics/signature-programs/international-baccalaureate-ib',
		'https://www.pvschools.net/schools/north-canyon-high/academics/signature-programs/rio-salado-dual-enrollment',
		'https://www.pvschools.net/schools/north-ranch-elementary/our-school/overview',
		'https://www.pvschools.net/schools/north-ranch-elementary/our-school/school-council',
		'https://www.pvschools.net/schools/north-ranch-elementary/our-school/attendance',
		'https://www.pvschools.net/schools/north-ranch-elementary/our-school/supply-lists',
		'https://www.pvschools.net/schools/north-ranch-elementary/academics/gifted',
		'https://www.pvschools.net/schools/north-ranch-elementary/academics/maker-center',
		'https://www.pvschools.net/schools/palomino-intermediate/our-school/about-our-school',
		'https://www.pvschools.net/schools/palomino-intermediate/our-school/principals-page/school-council-mission-statement',
		'https://www.pvschools.net/schools/palomino-intermediate/our-school/kids-corner',
		'https://www.pvschools.net/schools/palomino-intermediate/services/nurses-office',
		'https://www.pvschools.net/schools/palomino-intermediate/academics/signature-programs',
		'https://www.pvschools.net/schools/palomino-primary/our-school/about-palomino-primary',
		'https://www.pvschools.net/schools/palomino-primary/our-school/principals-page/palomino-primary-school-council',
		'https://www.pvschools.net/schools/palomino-primary/services/resources',
		'https://www.pvschools.net/schools/palomino-primary/services/nurses-office',
		'https://www.pvschools.net/schools/palomino-primary/our-school/principals-page/leadership-teams',
		'https://www.pvschools.net/schools/palomino-primary/academics/instruction',
		'https://www.pvschools.net/schools/palomino-primary/academics/signature-programs',
		'https://www.pvschools.net/schools/paradise-valley-high/our-school/overview',
		'https://www.pvschools.net/schools/paradise-valley-high/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/paradise-valley-high/our-school/paradise-valley-high-school-attendance',
		'https://www.pvschools.net/schools/paradise-valley-high/our-school/student-life-paradise-valley-high-school',
		'https://www.pvschools.net/schools/paradise-valley-high/our-school/student-life-paradise-valley-high-school/information-seniors',
		'https://www.pvschools.net/schools/paradise-valley-high/services/behavior',
		'https://www.pvschools.net/schools/paradise-valley-high/services/nurses-office',
		'https://www.pvschools.net/schools/paradise-valley-high/services/registration',
		'https://www.pvschools.net/schools/paradise-valley-high/services/registration/student-opportunities',
		'https://www.pvschools.net/schools/paradise-valley-high/services/bookstore',
		'https://www.pvschools.net/schools/paradise-valley-high/extracurricular/trojans-home',
		'https://www.pvschools.net/schools/paradise-valley-high/extracurricular/clubs-and-activities',
		'https://www.pvschools.net/schools/paradise-valley-high/academics/about-our-programs',
		'https://www.pvschools.net/schools/paradise-valley-high/academics/crest-stem-program',
		'https://www.pvschools.net/schools/paradise-valley-high/academics/about-crest-program-pv-high-school/programs-study',
		'https://www.pvschools.net/schools/paradise-valley-high/academics/about-crest-program-pv-high-school/apply-crest',
		'https://www.pvschools.net/schools/pinnacle-high/our-school/overview',
		'https://www.pvschools.net/schools/pinnacle-high/our-school/overview/attendance',
		'https://www.pvschools.net/schools/pinnacle-high/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/pinnacle-high/services/health-and-nutrition',
		'https://www.pvschools.net/schools/pinnacle-high/services/pinnacle-publications',
		'https://www.pvschools.net/schools/pinnacle-high/services/behavior',
		'https://www.pvschools.net/schools/pinnacle-high/services/behavior/student-resource-officer-sro',
		'https://www.pvschools.net/schools/pinnacle-high/services/transportation',
		'https://www.pvschools.net/schools/pinnacle-high/extracurricular/pioneers-home',
		'https://www.pvschools.net/schools/pinnacle-high/academics/curriculum',
		'https://www.pvschools.net/schools/pinnacle-high/academics/tutoring',
		'https://www.pvschools.net/schools/pinnacle-high/academics/graduation-information',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/our-school/overview',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/our-school/overview/attendance-and-tardies',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/services/nurses-office/health-office',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/services/social-emotional-learning-supports/library-services',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/services/campus-visit-procedures',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/extracurricular/clubs-and-activities/community-education-programs',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/academics/curriculum',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/academics/signature-programs',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/academics/special-education',
		'https://www.pvschools.net/schools/pinnacle-peak-preparatory-k-8/academics/annual-field-trips',
		'https://www.pvschools.net/schools/pvonline/our-school/overview',
		'https://www.pvschools.net/schools/pvonline/services/counseling-center',
		'https://www.pvschools.net/schools/pvonline/services/behavior',
		'https://www.pvschools.net/schools/pvonline/our-school/pvonline-programs',
		'https://www.pvschools.net/schools/pvonline/academics/instruction',
		'https://www.pvschools.net/schools/pvonline/academics/pvonline-summer-school',
		'https://www.pvschools.net/schools/pvonline/academics/academic-services',
		'https://www.pvschools.net/schools/pvonline/our-staff/instructors-profiles',
		'https://www.pvschools.net/schools/pvonline/newscenter/pvonline-provides-alternative-learning-options-students',
		'https://www.pvschools.net/schools/quail-run-elementary/our-school/overview',
		'https://www.pvschools.net/schools/quail-run-elementary/our-school/overview/attendance',
		'https://www.pvschools.net/schools/quail-run-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/quail-run-elementary/services/resources',
		'https://www.pvschools.net/schools/quail-run-elementary/academics/curriculum/media-center',
		'https://www.pvschools.net/schools/quail-run-elementary/services/health-nutrition',
		'https://www.pvschools.net/schools/quail-run-elementary/academics/international-baccalaureate-quail-run',
		'https://www.pvschools.net/schools/quail-run-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/roadrunner-school/our-school/overview',
		'https://www.pvschools.net/schools/roadrunner-school/our-school/overview/attendance',
		'https://www.pvschools.net/schools/roadrunner-school/services/emergency-preparedness/student-conduct',
		'https://www.pvschools.net/schools/roadrunner-school/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/roadrunner-school/services/nurses-office',
		'https://www.pvschools.net/schools/roadrunner-school/services/transportation',
		'https://www.pvschools.net/schools/roadrunner-school/services/emergency-preparedness',
		'https://www.pvschools.net/schools/roadrunner-school/services/emergency-preparedness/student-discipline',
		'https://www.pvschools.net/schools/roadrunner-school/academics/curriculum',
		'https://www.pvschools.net/schools/roadrunner-school/academics/signature-programs/teaching-interactions',
		'https://www.pvschools.net/schools/roadrunner-school/academics/signature-programs',
		'https://www.pvschools.net/schools/roadrunner-school/academics/enrichment',
		'https://www.pvschools.net/schools/sandpiper-elementary/our-school/overview',
		'https://www.pvschools.net/schools/sandpiper-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/sandpiper-elementary/services/health-and-nutrition',
		'https://www.pvschools.net/schools/sandpiper-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/sandpiper-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/sandpiper-elementary/academics/enrichment',
		'https://www.pvschools.net/schools/sandpiper-elementary/academics/fine-arts',
		'https://www.pvschools.net/schools/sandpiper-elementary/academics/classroom-supply-lists',
		'https://www.pvschools.net/schools/shadow-mountain-high/our-school/attendance',
		'https://www.pvschools.net/schools/shadow-mountain-high/our-school/leadership/school-council',
		'https://www.pvschools.net/schools/shadow-mountain-high/our-school/parents/smhs-parent-teacher-committee',
		'https://www.pvschools.net/schools/shadow-mountain-high/our-school/parents/senior-graduation-information',
		'https://www.pvschools.net/schools/shadow-mountain-high/services/shadow-mountain-nurses-office',
		'https://www.pvschools.net/schools/shadow-mountain-high/services/guidance',
		'https://www.pvschools.net/schools/shadow-mountain-high/services/college-career-center',
		'https://www.pvschools.net/schools/shadow-mountain-high/services/bookstore',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/shadow-mountain-media-center',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/shadow-mountain-high-school-smhs-arts-program/north-valley-arts',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/shadow-mountain-high-school-smhs-arts-program/smhs-choral-music',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/shadow-mountain-high-school-smhs-arts-program/shadow-mountain-bands',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/signature-programs-shadow-mountain/afjrotc-air-force-junior-reserve',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/signature-programs-shadow-mountain/advancement-individual',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/signature-programs-shadow-mountain/career-and-technical-education-2',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/signature-programs-shadow-mountain/career-and-technical-education-3',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/signature-programs-shadow-mountain/career-and-technical-education-1',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/signature-programs-shadow-mountain/career-and-technical-education-0',
		'https://www.pvschools.net/schools/shadow-mountain-high/academics/signature-programs-shadow-mountain/daaps-digital-academy-advanced',
		'https://www.pvschools.net/schools/shadow-mountain-high/extracurricular/matadors-home',
		'https://www.pvschools.net/schools/shadow-mountain-high/extracurricular/clubs-and-activities',
		'https://www.pvschools.net/schools/shea-middle/our-school/overview',
		'https://www.pvschools.net/schools/shea-middle/services/health-and-nutrition',
		'https://www.pvschools.net/schools/shea-middle/services/campus-safety',
		'https://www.pvschools.net/schools/shea-middle/our-school/student-life',
		'https://www.pvschools.net/schools/shea-middle/services/transportation',
		'https://www.pvschools.net/schools/shea-middle/academics/signature-programs/avid',
		'https://www.pvschools.net/schools/shea-middle/academics/signature-programs/north-valley-arts-academies',
		'https://www.pvschools.net/schools/shea-middle/our-school/student-life/summer-enrichment',
		'https://www.pvschools.net/schools/shea-middle/extracurricular/middle-school-athletics',
		'https://www.pvschools.net/schools/sky-crossing-elementary/home/overview',
		'https://www.pvschools.net/schools/sky-crossing-elementary/home/principals-page/school-council-news',
		'https://www.pvschools.net/schools/sky-crossing-elementary/home/overview/parent-resources',
		'https://www.pvschools.net/schools/sky-crossing-elementary/home/overview/nursing-nutrition',
		'https://www.pvschools.net/schools/sky-crossing-elementary/home/overview/support-sky-crossing',
		'https://www.pvschools.net/schools/sky-crossing-elementary/home/instruction',
		'https://www.pvschools.net/schools/sky-crossing-elementary/home/instruction/signature-programs',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/our-school/overview',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/our-school/school-hours',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/our-school/supply-list',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/our-school/school-hours/arrivaldismissal-procedures',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/join-us/support-our-school',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/academics/curriculum-highlights',
		'https://www.pvschools.net/schools/sonoran-sky-elementary/academics/signature-programs',
		'https://www.pvschools.net/schools/sunrise-middle/our-school/overview',
		'https://www.pvschools.net/schools/sunrise-middle/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/sunrise-middle/services/nurses-office',
		'https://www.pvschools.net/schools/sunrise-middle/services/safety',
		'https://www.pvschools.net/schools/sunrise-middle/services/transportation',
		'https://www.pvschools.net/schools/sunrise-middle/services/academic-services',
		'https://www.pvschools.net/schools/sunrise-middle/our-school/student-life',
		'https://www.pvschools.net/schools/sunrise-middle/academics/signature-programs',
		'https://www.pvschools.net/schools/sunrise-middle/academics/curriculum',
		'https://www.pvschools.net/schools/sunrise-middle/extracurricular/clubs-and-activities',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/our-school/overview',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/our-school/overview/attendance',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/services/health-and-nutrition',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/services/emergency-preparedness',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/academics/curriculum',
		'https://www.pvschools.net/schools/sunset-canyon-elementary/join-us/support-our-school',
		'https://www.pvschools.net/schools/sweetwater-community/our-school/overview',
		'https://www.pvschools.net/schools/sweetwater-community/services/nurses-office',
		'https://www.pvschools.net/schools/sweetwater-community/services/behavior',
		'https://www.pvschools.net/schools/sweetwater-community/services/academic-and-counseling-services',
		'https://www.pvschools.net/schools/sweetwater-community/academics/instruction-and-curriculum-sweetwater',
		'https://www.pvschools.net/schools/sweetwater-community/academics/signature-programs',
		'https://www.pvschools.net/schools/sweetwater-community/extracurricular/clubs-and-activities',
		'https://www.pvschools.net/schools/sweetwater-community/our-staff/teaching-staff',
		'https://www.pvschools.net/schools/vista-verde-middle/our-school/overview',
		'https://www.pvschools.net/schools/vista-verde-middle/our-school/overview/attendance',
		'https://www.pvschools.net/schools/vista-verde-middle/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/vista-verde-middle/our-school/information/student-handbook#dresscode',
		'https://www.pvschools.net/schools/vista-verde-middle/services/nurses-office',
		'https://www.pvschools.net/schools/vista-verde-middle/services/safety',
		'https://www.pvschools.net/schools/vista-verde-middle/services/transportation',
		'https://www.pvschools.net/schools/vista-verde-middle/join-us/support-our-school',
		'https://www.pvschools.net/schools/vista-verde-middle/extracurricular/athletics',
		'https://www.pvschools.net/schools/vista-verde-middle/extracurricular/clubs-and-activities',
		'https://www.pvschools.net/schools/vista-verde-middle/academics/electives/fine-arts',
		'https://www.pvschools.net/schools/vista-verde-middle/academics/electives/performing-arts',
		'https://www.pvschools.net/schools/whispering-wind-academy/our-school/overview',
		'https://www.pvschools.net/schools/whispering-wind-academy/join-us/support-our-school/school-council',
		'https://www.pvschools.net/schools/whispering-wind-academy/our-school/kids-corner',
		'https://www.pvschools.net/schools/whispering-wind-academy/services/nurses-office',
		'https://www.pvschools.net/schools/whispering-wind-academy/services/drop-and-pick',
		'https://www.pvschools.net/schools/whispering-wind-academy/join-us/support-our-school/ptso',
		'https://www.pvschools.net/schools/whispering-wind-academy/academics/our-commitment',
		'https://www.pvschools.net/schools/whispering-wind-academy/academics/signature-programs',
		'https://www.pvschools.net/schools/whispering-wind-academy/academics/pbis',
		'https://www.pvschools.net/schools/whispering-wind-academy/academics/signature-programs/chinese-mandarin-immersion',
		'https://www.pvschools.net/schools/whispering-wind-academy/academics/signature-programs/stem-g2',
		'https://www.pvschools.net/schools/wildfire-elementary/our-school/overview',
		'https://www.pvschools.net/schools/wildfire-elementary/our-school/overview/attendance-and-tardies',
		'https://www.pvschools.net/schools/wildfire-elementary/our-school/overview/make-your-day-citizenship-program',
		'https://www.pvschools.net/schools/wildfire-elementary/our-school/principals-page/school-council',
		'https://www.pvschools.net/schools/wildfire-elementary/services/health-and-nutrition/nurses-office',
		'https://www.pvschools.net/schools/wildfire-elementary/services/safety',
		'https://www.pvschools.net/schools/wildfire-elementary/our-school/kids-corner',
		'https://www.pvschools.net/schools/wildfire-elementary/services/transportation',
		'https://www.pvschools.net/schools/wildfire-elementary/academics/core-knowledge',
		'https://www.pvschools.net/schools/wildfire-elementary/academics/gifted-education-wfes',
		'https://www.pvschools.net/schools/wildfire-elementary/academics/gifted-education-wfes/gifted-testing-information',
		'https://www.pvschools.net/schools/wildfire-elementary/academics/meet-our-special-education-team',
		'https://www.pvschools.net/schools/wildfire-elementary/services/publications',
	]
	mainfolder = 'pvschools'
	school_name = 'pvschools'
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open(f'../f_web_interface/static/files/{mainfolder}/report.csv', 'w', encoding='utf-8') as csv_report, open(f'../f_web_interface/static/files/{mainfolder}/{school_name}.csv', 'w', encoding='utf-8') as csv_main:
		csv_report = csv.writer(csv_report)
		csv_report.writerow(['School name', school_name])

		csv_writer = csv.writer(csv_main)
		csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Tier 5', 'Tier 6', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

		page_counter = 0
		issue_pages_counter = 0

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

			if tiers[2].find(mainfolder) == -1:
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
