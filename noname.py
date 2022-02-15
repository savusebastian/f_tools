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

		if web_soup.find(id='page').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='page').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='page').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='page').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='page').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='page').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='page') != None and web_soup.find(id='page') != '':
			col1 = web_soup.find(id='page')
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
		'https://www.metrotech.edu/about',
		'https://www.metrotech.edu/about/mission',
		'https://www.metrotech.edu/about/board-education/access-open-records',
		'https://www.metrotech.edu/about/board-education/mtc-live',
		'https://www.metrotech.edu/about/board-education/legal-notice',
		'https://www.metrotech.edu/about/superintendent',
		'https://www.metrotech.edu/about/locations/downtown-business-campus/facilities',
		'https://www.metrotech.edu/business-training/event-centerr',
		'https://www.metrotech.edu/about/locations/springlake-campus/business-conference-center/event-center',
		'https://www.metrotech.edu/about/locations/springlake-campus/business-conference-center/event-center/catering',
		'https://www.metrotech.edu/about/locations/springlake-campus/business-conference-center/event-center/rooms',
		'https://www.metrotech.edu/about/locations/springlake-campus/child-care-center',
		'https://www.metrotech.edu/about/locations/springlake-campus/cosmetology',
		'https://www.metrotech.edu/about/locations/springlake-campus/economic-development-center',
		'https://www.metrotech.edu/about/locations/springlake-campus/health-careers-center',
		'https://www.metrotech.edu/about/locations/springlake-campus/information-technology-center',
		'https://www.metrotech.edu/about/locations/springlake-campus/metro-stem-academy',
		'https://www.metrotech.edu/about/locations/springlake-campus/service-center',
		'https://www.metrotech.edu/about/locations/springlake-campus/transportation-maintenance',
		'https://www.metrotech.edu/about/locations/springlake-campus/warehouse',
		'https://www.metrotech.edu/about/locations/springlake-campus/perry-klaassen-clinic',
		'https://www.metrotech.edu/about/employment-opportunities',
		'https://www.metrotech.edu/about/purchasing-opportunities',
		'https://www.metrotech.edu/about/public-surplus-auctions',
		'https://www.metrotech.edu/about/privacy-policy',
		'https://www.metrotech.edu/about/affirmation',
		'https://www.metrotech.edu/about/annual-security-report',
		'https://www.metrotech.edu/about/annual-security-report/campus-crime-statistics',
		'https://www.metrotech.edu/about/equal-opportunity-policy',
		'https://www.metrotech.edu/about/title-ix/consent',
		'https://www.metrotech.edu/about/title-ix/definitions',
		'https://www.metrotech.edu/about/title-ix/safety',
		'https://www.metrotech.edu/about/title-ix/reporting',
		'https://www.metrotech.edu/about/title-ix/resources',
		'https://www.metrotech.edu/about/title-ix/policies-procedures',
		'https://www.metrotech.edu/about/title-ix/training',
		'https://www.metrotech.edu/about/faq',
		'https://www.metrotech.edu/about/faq/kalms',
		'https://www.metrotech.edu/events/blog/financial-aid-frequently-asked-questions',
		'https://www.metrotech.edu/business-training',
		'https://www.metrotech.edu/business-training/small-business-management',
		'https://www.metrotech.edu/business-training/small-business-management/mission',
		'https://www.metrotech.edu/business-training/small-business-management/ready-start',
		'https://www.metrotech.edu/business-training/small-business-management/find-right-success',
		'https://www.metrotech.edu/business-training/small-business-management/steps-register-llc',
		'https://www.metrotech.edu/business-training/small-business-management/downloads',
		'https://www.metrotech.edu/business-training/small-business-management/workshops',
		'https://www.metrotech.edu/business-training/small-business-management/business-plan',
		'https://www.metrotech.edu/business-training/small-business-management/llc-better',
		'https://www.metrotech.edu/business-training/resources-start-up-businesses',
		'https://www.metrotech.edu/business-training/covid-online-learning',
		'https://www.metrotech.edu/business-training/courses-training',
		'https://www.metrotech.edu/business-training/courses-training/adobe/acrobat',
		'https://www.metrotech.edu/business-training/courses-training/adobe/after-effects',
		'https://www.metrotech.edu/business-training/courses-training/adobe/animate',
		'https://www.metrotech.edu/business-training/courses-training/adobe/captivate',
		'https://www.metrotech.edu/business-training/courses-training/adobe/contribute',
		'https://www.metrotech.edu/business-training/courses-training/adobe/dreamweaver',
		'https://www.metrotech.edu/business-training/courses-training/adobe/illustrator',
		'https://www.metrotech.edu/business-training/courses-training/adobe/indesign',
		'https://www.metrotech.edu/business-training/courses-training/adobe/photoshop',
		'https://www.metrotech.edu/business-training/courses-training/adobe/premiere',
		'https://www.metrotech.edu/business-training/courses-training/apple/certified-mac-technician-acmt-certification',
		'https://www.metrotech.edu/business-training/courses-training/apple/final-cut-pro-x',
		'https://www.metrotech.edu/business-training/courses-training/apple/final-cut-pro-x-10-3-professional-post-production',
		'https://www.metrotech.edu/business-training/courses-training/apple/iphone-application-development',
		'https://www.metrotech.edu/business-training/courses-training/apple/logic-pro-x',
		'https://www.metrotech.edu/business-training/courses-training/apple/mac-it-professional',
		'https://www.metrotech.edu/business-training/courses-training/apple/motion',
		'https://www.metrotech.edu/business-training/courses-training/apple/pages-numbers-keynote',
		'https://www.metrotech.edu/business-training/courses-training/apple/service-fundamentals',
		'https://www.metrotech.edu/business-training/courses-training/apple/garageband',
		'https://www.metrotech.edu/business-training/courses-training/apple/iwork',
		'https://www.metrotech.edu/business-training/courses-training/apple/os_x_certificationss',
		'https://www.metrotech.edu/business-training/courses-training/microsoft',
		'https://www.metrotech.edu/business-training/courses-training/microsoft/executives',
		'https://www.metrotech.edu/business-training/courses-training/microsoft/crash-courses',
		'https://www.metrotech.edu/business-training/courses-training/workplace-health-safety',
		'https://www.metrotech.edu/business-training/courses-training/video-professional',
		'https://www.metrotech.edu/business-training/courses-training/web-design',
		'https://www.metrotech.edu/business-training/courses-training/graphic-design',
		'https://www.metrotech.edu/business-training/courses-training/it-professional',
		'https://www.metrotech.edu/business-training/courses-training/associate-certification',
		'https://www.metrotech.edu/business-training/courses-training/phr-sphr-certification-prep',
		'https://www.metrotech.edu/business-training/courses-training/cpr-aed',
		'https://www.metrotech.edu/business-training/courses-training/project-management',
		'https://www.metrotech.edu/business-training/courses-training/lean',
		'https://www.metrotech.edu/business-training/courses-training/no-classes-currently-scheduled',
		'https://www.metrotech.edu/business-training/customized-solutions',
		'https://www.metrotech.edu/business-training/customized-solutions/leadership-development',
		'https://www.metrotech.edu/business-training/customized-solutions/employee-development',
		'https://www.metrotech.edu/business-training/customized-solutions/advanced-team-training',
		'https://www.metrotech.edu/business-training/customized-solutions/hr-management',
		'https://www.metrotech.edu/business-training/customized-solutions/coaching',
		'https://www.metrotech.edu/business-training/event-center',
		'https://www.metrotech.edu/business-training/testimonials',
		'https://www.metrotech.edu/business-training/authorized-training-center',
		'https://www.metrotech.edu/admission-cost/apply',
		'https://www.metrotech.edu/admission-cost/assessment-center',
		'https://www.metrotech.edu/admission-cost/college',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment/in-district',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment/home-private-school',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment/out-of-district',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment/tuition-cost',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment/senior-scholarships',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment/sending-schools',
		'https://www.metrotech.edu/admission-cost/high-school-enrollment/transportation',
		'https://www.metrotech.edu/admission-cost/adult-enrollment',
		'https://www.metrotech.edu/admission-cost/adult-enrollment/meet-with-career-advisor',
		'https://www.metrotech.edu/admission-cost/adult-enrollment/tuition-costs-refund-policy',
		'https://www.metrotech.edu/admission-cost/adult-enrollment/payment-financial-aid',
		'https://www.metrotech.edu/admission-cost/adult-enrollment/payment-financial-aid/tuition-waiver',
		'https://www.metrotech.edu/admission-cost/adult-enrollment/payment-financial-aid/scholarships',
		'https://www.metrotech.edu/admission-cost/best-program',
		'https://www.metrotech.edu/admission-cost/child-care-services',
		'https://www.metrotech.edu/admission-cost/student-services/counselors-corner',
		'https://www.metrotech.edu/admission-cost/student-services/special-services/overview',
		'https://www.metrotech.edu/admission-cost/student-services/special-services/faq',
		'https://www.metrotech.edu/admission-cost/student-services/special-services/dct-resources',
		'https://www.metrotech.edu/admission-cost/student-services/special-services/disclosures-procedural-safeguards',
		'https://www.metrotech.edu/admission-cost/student-services/career-advisors',
		'https://www.metrotech.edu/admission-cost/student-services/student-handbook',
		'https://www.metrotech.edu/admission-cost/student-services/transcript-request',
		'https://www.metrotech.edu/admission-cost/student-services/veteran-educational-benefits-resources',
		'https://www.metrotech.edu/admission-cost/student-services/information-technology-policy',
		'https://www.metrotech.edu/admission-cost/student-rights',
		'https://www.metrotech.edu/admission-cost/financial-aid/entrance-counseling',
		'https://www.metrotech.edu/admission-cost/financial-aid/exit-counseling',
		'https://www.metrotech.edu/admission-cost/catalog',
		'https://www.metrotech.edu/admission-cost/school-calendar',
		'https://www.metrotech.edu/programs-classes/career-trainingg',
		'https://www.metrotech.edu/programs-classes/aviation/aircraft-maintenance/info',
		'https://www.metrotech.edu/programs-classes/healthcare/medical-assisting/info',
		'https://www.metrotech.edu/programs-classes/healthcare/medical-assisting/info/course-descriptions',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/certifications',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/class-times-structure',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/curriculum-plan',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/student-learning-outcomes',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/course-descriptions',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/requirements-licensure',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/history',
		'https://www.metrotech.edu/programs-classes/healthcare/practical-nursing/info/advanced-standing',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/mission-goals-outcomes',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/course-descriptions',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/history',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/curriculum-plan',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/description',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/philosophy',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/admission',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/tuition-and-fees',
		'https://www.metrotech.edu/programs-classes/healthcare/radiologic-technology/info/hours',
		'https://www.metrotech.edu/programs-classes/healthcare/surgical-technology/info',
		'https://www.metrotech.edu/programs-classes/healthcare/surgical-technology/info/tuition',
		'https://www.metrotech.edu/programs-classes/healthcare/surgical-technology/info/advanced-standing',
		'https://www.metrotech.edu/programs-classes/healthcare/surgical-technology/info/history',
		'https://www.metrotech.edu/programs-classes/healthcare/surgical-technology/info/goals-student-learning-outcomes',
		'https://www.metrotech.edu/programs-classes/special-interest',
		'https://www.metrotech.edu/programs-classes/stem/biomedical-sciences-academy/overview',
		'https://www.metrotech.edu/programs-classes/stem/biomedical-sciences-academy/overview/faq',
		'https://www.metrotech.edu/programs-classes/stem/biomedical-sciences-academy/overview/course-descriptions',
		'https://www.metrotech.edu/programs-classes/career-training',
		'https://www.metrotech.edu/programs-classes/short-term',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/2020-nec-code-changes',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/boiler-operations-low-pressure',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/boiler-operations-high-pressure',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/drafting-technician-architectural-cad-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/drafting-technician-architectural-cad-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/drywall-paint-repair',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/electrical-troubleshooting-preventive-maintenance',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/electricity-non-electricians',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/hvac-basic-commercial',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/tile-i-walls-counter-tops',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/tile-ii-bathroom-remodel',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/upholstery-furniture',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/architecture-construction/window-installation-basic',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/business-management-administration',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/business-management-administration/grant-writing',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/chinese-mandarin-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/chinese-mandarin-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/esl-learn-english-better-way',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/golf-fundamentals-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/google-digital-skills',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/hiset-ged-prep-academy',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/spanish-conversational',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/spanish-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/spanish-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/education-training/spanish-iii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/aapc-membership-meeting-ceu',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/aapc-testing-class',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/alzheimers-advanced-dementia-certification-online',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/alzheimers-basic-dementia-certification-online',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/anatomy-physiology-providers-online',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cma-update-ceu',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cma-advanced-nasogastric-gastrostomy-respiratory',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cma-i-certified-medication-aide',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cma-i-certified-medication-aide-orientation',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cna-certified-nurse-aide-ltc-long-term-care',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cna-certified-nurse-aide-orientation',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cna-skills-test',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/coding-cpt-icd-10',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cpr-aha-basic-life-support-healthcare-providers',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/cpr-aha-heart-code-bls-skills-check',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/ekg-monitor-technician',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/emergency-medical-technician-emt',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/emergency-medical-technician-emt-orientation',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/heartsaver-first-aid-cpr-aed-aha',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/hha-home-health-aide-deeming',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/iv-therapy',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/mat-medication-administration-technician',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/mat-update',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/medical-terminology-online',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/nurse-refresher-orientation',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/nurse-refresher',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/pharmacy-technician',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/phlebotomy',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/phlebotomy-internship',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/phlebotomy-refresher',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/veterinary-assistant-certification',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/health-science/veterinary-assistant-certification-orientation',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/human-services',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/human-services/providing-childrens-safety',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/human-services/providing-childrens-health',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/human-services/providing-environment-learning',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/human-services/child-growth-development-concepts',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/human-services/ensuring-dev-appropriate-practices',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/human-services/putting-together',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/a-certification-level-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/access-2019-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/access-2019-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/access-2019-iii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/computer-literacy-all',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/computer-literacy-senior-citizens',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/excel-2019-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/excel-2019-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/excel-2019-iii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/fundamentals-technology',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/google-digital-skills',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/it-fundamentals-level-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/network-level-iii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/object-oriented-programming-oop-introduction',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/outlook-2019-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/power-point-2019-I',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/power-point-2019-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/publisher-2019-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/security-level-iv',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/word-2019-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/word-2019-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/information-technology/word-2019-iii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/law-public-safety-corrections-security',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/law-public-safety-corrections-security/active-shooter-simulation-milo',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/law-public-safety-corrections-security/phase-i-unarmed-security',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/law-public-safety-corrections-security/phase-ii-unarmed-security',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/law-public-safety-corrections-security/phase-iii-private-investigator',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/law-public-safety-corrections-security/phase-iv-firearms',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/manufacturing',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/manufacturing/aircraft-sheet-metal-structure-manufacturing',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/manufacturing/welding-basics',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/manufacturing/welding-job-readiness-i',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/manufacturing/welding-job-readiness-ii',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/transportation-distribution-logistics',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/transportation-distribution-logistics/drone-pilot-test-prep-uas',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/transportation-distribution-logistics/drone-safety-flight-practice-uas',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/transportation-distribution-logistics/forklift-certification',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/transportation-distribution-logistics/school-bus-inspector',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/transportation-distribution-logistics/small-engine-maintenance',
		'https://www.metrotech.edu/programs-classes/short-term/adult-continuing-education/enrollment',
		'https://www.metrotech.edu/programs-classes/short-term/online-classes',
		'https://www.metrotech.edu/metrofit',
		'https://www.metrotech.edu/student-resources',
		'https://www.metrotech.edu/community',
		'https://www.metrotech.edu/community/reel-jobs-ok-film-industry',
		'https://www.metrotech.edu/community/deadcenter-university',
		'https://www.metrotech.edu/metrofit',
		'https://www.metrotech.edu/events/graduation',
		'https://www.metrotech.edu/events/awards-recognitions',
		'https://www.metrotech.edu/events/awards-recognitions/employee-recognition',
		'https://www.metrotech.edu/events/upcoming',
		'https://www.metrotech.edu/about/board-education/mtc-live',
	]
	mainfolder = 'metrotech'
	school_name = 'metrotech_district'
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
