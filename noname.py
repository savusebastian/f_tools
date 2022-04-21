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

		if web_soup.find(id='main').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='main').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='main').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='main').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='main').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='main').find_all(class_='news') != []:
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
		'https://www.stamfordpublicschools.org/choose-stamford/about-sps',
		'https://www.stamfordpublicschools.org/district/superintendents-office',
		'https://www.stamfordpublicschools.org/node/56/faq',
		'https://www.stamfordpublicschools.org/district/superintendents-office/faq/can-insice-employee-come-school',
		'https://www.stamfordpublicschools.org/district/superintendents-office/faq/what-if-insice-employee-arrives-school-without-following',
		'https://www.stamfordpublicschools.org/district/superintendents-office/faq/what-happens-if-ins-or-ice-employee-refuses-go-superintendent-or',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/one_sheeter_updated_5.pdf',
		'https://www.youtube.com/watch?v=LxKWQNLCrM8&feature=youtu.be',
		'https://www.stamfordpublicschools.org/choose-stamford/student-life',
		'https://user-xhtcbfi.cld.bz/2019-2020-Annual-Report-to-the-Community',
		'https://www.stamfordpublicschools.org/choose-stamford/student-life/links/college-list-class-2021',
		'https://www.stamfordpublicschools.org/district/stamford-public-schools-strategic-plan',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/learn-about-our-district-and-our-schools',
		'https://spsapples.org',
		'https://davenportridge.org ',
		'https://hartschool.org ',
		'https://starkschool.org',
		'https://ktmurphy.org ',
		'https://newfieldschool.org ',
		'https://northeastelementary.org',
		'https://rogersinternationalschool.org',
		'https://roxburyschool.org ',
		'https://springdaleschool.net',
		'https://stillmeadowct.org',
		'https://strawberryhillschool.org',
		'https://toquamschool.org',
		'https://westovermagnet.org',
		'https://cloonanms.org',
		'http://dolanmiddle.org',
		'https://rippowammiddle.org',
		'https://magnetmiddle.org',
		'https://toronline.org ',
		'https://aitestamford.org ',
		'https://stamfordhigh.org ',
		'https://westhillweb.com ',
		'https://www.stamfordadulted.org/Default.asp',
		'https://www.stamfordpublicschools.org/anchor',
		'https://www.stamfordpublicschools.org/district/summer-school-programs',
		'https://www.stamfordpublicschools.org/magnet-schools',
		'https://www.stamfordpublicschools.org/magnet-schools/pages/22-23-magnet-school-lottery-application-important-dates',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/21-22_magnet_schools_in_stamford_-_final_english.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/21-22_magnet_schools_in_stamford_final_-_spanish.pdf',
		'https://www.stamfordpublicschools.org/node/165803/faq',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/rogers_preferred_areas_1_2_0.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/preferred_area_1_to_admission_to_new_school.pdf',
		'https://www.stamfordpublicschools.org/magnet-schools/pages/sps-board-education-policy-and-regulation-magnet-schools',
		'https://www.stamfordpublicschools.org/rogers-international-school/information/pages/ib-program',
		'https://www.stamfordpublicschools.org/district/pages/interactive-map-stamford-public-schools',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/pages/required-registration-documents',
		'https://www.stamfordpublicschools.org/teaching-learning/college-and-career-readiness',
		'https://www.stamfordpublicschools.org/district/college-and-career-readiness/news/new-naviance-login-process-students-and-parents',
		'https://www.stamfordpublicschools.org/district/innovative-programs',
		'https://www.stamfordpublicschools.org/grants-funded-programs/pages/consolidated-grants-application',
		'https://drive.google.com/file/d/1TDPcg3zkvmEXfRf46pPRpEUzY2jYYOwK/view?usp=sharing',
		'https://drive.google.com/file/d/1MOYiAPq9QmMHgJDz4PZt-xAnDx_D-bik/view?usp=sharing',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/specific_grants_additional_information.pdf',
		'https://www.stamfordpublicschools.org/grants-funded-programs/pages/administration-neglected-delinquent-allocations',
		'https://www.stamfordpublicschools.org/grants-funded-programs/pages/administration-non-public-school-allocations',
		'https://www.stamfordpublicschools.org/district/grants-funded-programs/pages/downloadable-files',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/budget_allocation-april_15th.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/budget_breakdown.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/budget_revision.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/claim-invoice_form.pdf',
		'https://www.stamfordpublicschools.org/grants-funded-programs/pages/school-allocations',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/after-school-care',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/school-care',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/family-survey-summary-results',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/family-and-community-engagement-facilitators',
		'https://spslgbtqgallery.wixsite.com/spsgallery',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/long-term-facilities-plan-community-feedback-form',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/out-attendance-zone-placement-2021-2022',
		'https://www.stamfordpublicschools.org/office-family-community-engagement/pages/powerschool-parent-portal',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/resources-home-learning',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/sps-parent-university-resources',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/school-governance-councils',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/covid-19-vaccination-clinic-information',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/covid-19-voluntary-testing-unvaccinated-students',
		'https://www.covidtests.gov/',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/homeschooling',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/request-remote-learning-accommodation-due-living',
		'https://www.stamfordpublicschools.org/public-affairs/pages/parent-school-organizations',
		'https://www.stamfordpublicschools.org/district/teaching-learning',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/scientific-research-based-interventions-srbi',
		'https://www.stamfordpublicschools.org/curriculum-instruction/pages/avid',
		'https://www.stamfordpublicschools.org/district/curriculum-instruction/pages/common-core-state-standards',
		'https://www.stamfordpublicschools.org/teaching-learning/english-language-arts-ela',
		'https://www.stamfordpublicschools.org/district/english-language-arts-ela/pages/grades-k-5-ela',
		'https://www.stamfordpublicschools.org/english-language-arts-ela/pages/grades-6-8-ela',
		'https://www.stamfordpublicschools.org/english-language-arts-ela/pages/grades-9-12-ela',
		'https://www.stamfordpublicschools.org/teaching-learning/fine-arts',
		'https://www.stamfordpublicschools.org/district/performing-arts',
		'https://www.stamfordpublicschools.org/performing-arts/pages/music-stamford-public-schools',
		'https://www.stamfordpublicschools.org/district/performing-arts/pages/national-core-arts-standards',
		'https://www.stamfordpublicschools.org/teaching-learning/health-physical-education',
		'https://www.stamfordpublicschools.org/district/block-scheduling',
		'https://www.stamfordpublicschools.org/district/curriculum-instruction/pages/high-school-program-studies',
		'https://drive.google.com/file/d/1L-lWRvgSHAqCE6ZqkAMPk7pEEyvtTSmp/view?usp=sharing',
		'https://drive.google.com/file/d/19H3p-1isnK4S9Z-rPMpmDvcgBITIoAHh/view?usp=sharing',
		'https://www.stamfordpublicschools.org/teaching-learning/math',
		'https://www.stamfordpublicschools.org/district/grades-k-5-math',
		'https://www.stamfordpublicschools.org/district/grades-k-5-math/pages/common-core-state-standards-resources',
		'https://www.stamfordpublicschools.org/grades-k-5-math/links/everyday-math',
		'https://www.stamfordpublicschools.org/grades-k-5-math/links/everyday-math-log-page',
		'https://www.stamfordpublicschools.org/grades-k-5-math/pages/learn-zillion-lessons',
		'https://www.stamfordpublicschools.org/district/grades-k-5-math/pages/online-summer-math-and-literacy-resources',
		'https://www.stamfordpublicschools.org/district/grades-k-5-math/pages/teacher-parent-math-resources',
		'https://www.stamfordpublicschools.org/district/grades-6-8-math',
		'https://www.stamfordpublicschools.org/grades-6-8-math/links/dash-web-login',
		'https://www.stamfordpublicschools.org/grades-6-8-math/links/desmos-graphing-calculator',
		'https://www.stamfordpublicschools.org/grades-6-8-math/links/khan-academy-common-core-resources',
		'https://www.stamfordpublicschools.org/grades-6-8-math/links/mangahigh-math-games',
		'https://www.stamfordpublicschools.org/grades-6-8-math/links/mathematics-common-core-state-standards-ccss',
		'https://www.stamfordpublicschools.org/grades-6-8-math/pages/mymathuniverse-links',
		'https://www.stamfordpublicschools.org/district/grades-9-12-math',
		'https://www.stamfordpublicschools.org/grades-9-12-math/pages/classzone-links',
		'https://www.stamfordpublicschools.org/grades-9-12-math/links/desmos-graphing-calculator',
		'https://www.stamfordpublicschools.org/grades-9-12-math/links/khan-academy-algebra-i',
		'https://www.stamfordpublicschools.org/grades-9-12-math/links/mathematics-common-core-state-standards-ccss',
		'https://www.stamfordpublicschools.org/teaching-learning/science',
		'https://www.stamfordpublicschools.org/district/science/pages/grades-k-5-science',
		'https://www.stamfordpublicschools.org/district/science/pages/grades-6-8-science',
		'https://www.stamfordpublicschools.org/science/pages/grades-9-12-science',
		'https://www.stamfordpublicschools.org/teaching-learning/social-studies',
		'https://www.stamfordpublicschools.org/district/social-studies/pages/grades-k-5-social-studies',
		'https://www.stamfordpublicschools.org/social-studies/pages/grades-6-8-social-studies',
		'https://www.stamfordpublicschools.org/district/social-studies/pages/grades-9-12-social-studies',
		'https://www.stamfordpublicschools.org/social-studies/pages/social-studies-web-links',
		'https://www.stamfordpublicschools.org/teaching-learning/world-languages',
		'https://www.stamfordpublicschools.org/district/special-education-and-related-services',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/procedural_safeguards_2021.pdf',
		'https://www.stamfordpublicschools.org/district/special-education-and-related-services/pages/parents-guide-special-education-connecticut',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/special-education-and-related-services/pages/disabilities',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/special-education-and-related-services/pages/free-appropriate',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/iee_2.10.22_update.pdf',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/special-education-and-related-services/pages/key-terms',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/special-education-and-related-services/pages/specialized-programs',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/special-education-and-related-services/pages/preschool-special',
		'https://www.stamfordpublicschools.org/district/special-education-and-related-services/pages/individualized-education-plan-iep',
		'https://www.stamfordpublicschools.org/district/special-education-and-related-services/pages/section-504',
		'https://www.stamfordpublicschools.org/district/student-support-special-programs/pages/psychology-department',
		'https://www.stamfordpublicschools.org/student-support-special-programs/pages/social-work',
		'https://www.stamfordpublicschools.org/student-support-special-programs/pages/speech-language-department',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/english-learners',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/english-learners/pages/bilingual-education',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/english-learners/pages/el-program-locations',
		'https://www.stamfordpublicschools.org/english-learners/pages/el-program-overview',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/english-learners/pages/el-web-links',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services/pages/breakfast-lunch-menus',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services/pages/food-allergies',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services/pages/free-or-reduced-breakfast-lunch-application-information',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services/pages/new-mood-boost',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services/pages/pay-school-meals',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services/slideshows/student-engagement-event-photos',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services/pages/pay-school-meals',
		'https://www.stamfordpublicschools.org/district/chartwells-dining-services',
		'https://www.stamfordpublicschools.org/district/transportation',
		'https://www.stamfordct.gov/government/boards-commissions/stamford-asset-management-group',
		'https://www.stamfordpublicschools.org/district/finance-purchasing',
		'https://www.stamfordpublicschools.org/district/finance-purchasing/pages/rfps-and-bids',
		'https://www.stamfordpublicschools.org/district/finance-purchasing/pages/2021-2022-budget-documents',
		'https://www.stamfordpublicschools.org/district/finance-purchasing/pages/2022-2023-budget-documents',
		'https://www.stamfordpublicschools.org/district/finance-purchasing/pages/account-payables',
		'https://www.stamfordpublicschools.org/district/finance-purchasing/pages/budget-archives',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/sample_agreement_for_boe_rfp_packages_1.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/the_rfp_process_explained.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/bid_waiver_form_interactive.pdf',
		'https://www.stamfordpublicschools.org/district/finance-purchasing/pages/rfpbid-award-notification',
		'https://www.stamfordpublicschools.org/district/finance-purchasing/pages/contracts-ct-public-act18-125',
		'https://www.stamfordpublicschools.org/district/public-affairs',
		'https://www.stamfordpublicschools.org/district/public-affairs/webforms/2021-2022-communication-tools-flyer',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/communication_tools_flyer.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/communication_tools_flyer-spanish.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/communication_tools_flyer-hc.pdf',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/powerschool-parent-portal',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/closings-delays',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/8.5_x_11_congrats_2021_ad.jpg',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/one_sheeter_updated_5.pdf',
		'https://www.youtube.com/watch?v=LxKWQNLCrM8&feature=youtu.be',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/flyer-distribution',
		'https://www.stamfordpublicschools.org/public-affairs/pages/public-safety',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/school-bell-times-regular-day-delayed-opening-and-early-release',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/student-staff-achievements',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/school-district-calendars',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/school_calendar_2021-2022_adopted_05-07-19rev07-27-2021_0.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/school_calendar_2022-2023_v4.pdf',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/annual-report-community-historical',
		'https://user-xhtcbfi.cld.bz/2019-2020-Annual-Report-to-the-Community',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/stamford_public_schools_annual_report_single_pagesjunefinal.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/sps_annual_17-18_main_051519-web.pdf',
		'https://user-xhtcbfi.cld.bz/2016-2017-Annual-Report-to-the-Community',
		'https://www.stamfordpublicschools.org/district/human-resources',
		'https://www.stamfordpublicschools.org/human-resources/current-employees',
		'https://www.stamfordpublicschools.org/district/current-employees/pages/certification-resources',
		'https://www.stamfordpublicschools.org/human-resources/current-employees/pages/childcare-scholarships',
		'https://www.stamfordpublicschools.org/human-resources/current-employees/pages/employment-posters',
		'https://www.stamfordpublicschools.org/district/current-employees/pages/family-and-medical-leave-act-fmla',
		'https://www.stamfordpublicschools.org/current-employees/pages/federal-regulations',
		'https://www.stamfordpublicschools.org/human-resources/current-employees/pages/forms',
		'https://www.stamfordpublicschools.org/district/current-employees/pages/aesop-information',
		'http://www.generalasp.com/stamford/onlineapp/default.aspx?internal=internal&district=',
		'https://www.stamfordpublicschools.org/district/board-education/pages/policies-and-regulations',
		'https://www.stamfordpublicschools.org/human-resources/current-employees/pages/salary-reclassification',
		'https://www.stamfordpublicschools.org/district/human-resources/pages/staff-admin-logins',
		'https://www.stamfordpublicschools.org/human-resources/current-employees/pages/substitute-teacher-resources',
		'https://www.stamfordpublicschools.org/professional-learning/pages/team-program',
		'https://www.stamfordpublicschools.org/human-resources/current-employees/pages/tuition-reimbursement',
		'https://www.stamfordpublicschools.org/human-resources/current-employees/pages/union-contracts',
		'https://www.stamfordpublicschools.org/human-resources/pages/verification-employment',
		'https://www.stamfordpublicschools.org/district/benefits',
		'https://www.stamfordpublicschools.org/district/benefits/pages/benefit-plan-information',
		'https://www.stamfordpublicschools.org/district/benefits/pages/benefits-administrators-and-contact-information',
		'https://www.stamfordpublicschools.org/district/benefits/pages/benefits-checklist-qualified-life-events',
		'https://www.stamfordpublicschools.org/district/benefits/pages/benefits-forms-applications',
		'https://www.stamfordpublicschools.org/benefits/pages/employee-assistance-program',
		'https://www.stamfordpublicschools.org/district/benefits/pages/hep',
		'https://www.stamfordpublicschools.org/district/benefits/pages/health-and-wellness',
		'https://www.stamfordpublicschools.org/district/benefits/pages/retirement-plans',
		'https://www.stamfordpublicschools.org/district/human-resources/pages/employee-recognition',
		'https://www.stamfordpublicschools.org/district/human-resources/pages/former-employees',
		'https://www.stamfordpublicschools.org/district/human-resources/pages/volunteer-opportunities',
		'https://www.stamfordpublicschools.org/district/professional-learning',
		'https://www.calendarwiz.com/calendars/calendar.php?crd=sps_professionallearning&&jsenabled=1&winh=545&winw=1098&inifr=false',
		'https://www.stamfordpublicschools.org/district/professional-learning/pages/content-area-plans',
		'https://www.protraxx.com/login.aspx',
		'https://www.stamfordpublicschools.org/district/professional-learning/pages/web-resources',
		'https://www.stamfordpublicschools.org/human-resources/careers',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/paraeducator_wage_grids_2021-2022.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/sea_salary_schedule_2021-2022_0.pdf',
		'https://www.stamfordpublicschools.org/human-resources/careers/pages/areas-recruitment',
		'https://www.stamfordpublicschools.org/human-resources/careers/pages/substituting-stamford-public-schools',
		'https://www.youtube.com/watch?v=zaVgSMMJrzM',
		'https://www.youtube.com/watch?v=LxKWQNLCrM8',
		'https://www.stamfordpublicschools.org/district/careers/pages/why-work-stamford',
		'https://www.stamfordpublicschools.org/district/human-resources/pages/community-concerns-reporting',
		'https://www.stamfordpublicschools.org/node/1642/faq',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/cooperative-work-education',
		'https://www.stamfordpublicschools.org/stamford-high-school/school-counseling',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/internship-opportunities',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/limited-enrollment-programs-jrotc',
		'https://www.stamfordmyep.com/',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/part-time-job-opportunities',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/pathways',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/pre-apprenticeships',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/senior-internship',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/summer-career-pathway-programs',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/summer-job-opportunities',
		'https://www.stamfordpublicschools.org/district/career-pathways-workplace-learning-apprenticeships/pages/%E2%80%9Clooking-be-partner%E2%80%9D',
		'https://www.stamfordct.gov/government/view-all-city-departments/youth-services/mayor-s-youth-leadership-council',
		'https://www.stamfordpublicschools.org/district/pages/central-office',
		'https://www.stamfordpublicschools.org/district/pages/departments-programs-services',
		'https://www.stamfordpublicschools.org/district/office-family-community-engagement/pages/family-and-community-engagement-facilitators',
		'https://www.stamfordpublicschools.org/district/public-affairs/pages/flyer-distribution',
		'https://www.stamfordpublicschools.org/district/human-resources/pages/volunteer-opportunities',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/volunteer_application_-_english.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/volunteer_application_-_spanish.pdf',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/pages/required-registration-documents',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/list_of_documents_-_proof_of_address.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/notarized_residency_affidavit_-_form_a_-_english_-_pink_form.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/notarized_residency_affidavit_-_form_a_-_spanish_-_pink_form.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/health_assessment_form_-_har3_2018.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/medicationform.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/sps_-_sr7_in_english.doc.pdf',
		'https://www.stamfordpublicschools.org/sites/g/files/vyhlif3841/f/uploads/sps_-_sr7_in_spanish.doc.pdf',
		'https://www.stamfordpublicschools.org/district/research-office/pages/school-look',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/pages/school-contact-information',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/pages/2021-2022-grade-placement-guide',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/pages/kindergarten-information',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/pages/out-attendance-zone-placement-2021-2022',
		'https://script.google.com/macros/s/AKfycbyGqCqaBP8DkQk901bSVgISQ0dcmszKNRij4sFu6ZCtoA5ybEwlJGPEPorYMySGByhF/exec',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/links/ooaz-21-22-spanish',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/links/professional-courtesy-21-22-update',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/pages/request-student-records-0',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/links/records-request-form',
		'https://www.stamfordpublicschools.org/intervention-and-student-support/school-registration/links/record-request-form-spanish',
	]
	mainfolder = 'stamfordpublicschools'
	school_name = 'district'
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
			elif len(tiers) == 10:
				t1 = tiers[-7].capitalize()
				t2 = tiers[-6].capitalize()
				t3 = tiers[-5].capitalize()
				t4 = tiers[-4].capitalize()
				t5 = tiers[-3].capitalize()
				t6 = tiers[-2].capitalize()
			else:
				# t1 = tiers[-6].capitalize()
				# t2 = tiers[-5].capitalize()
				# t3 = tiers[-4].capitalize()
				# t4 = tiers[-3].capitalize()
				# t5 = tiers[-2].capitalize()
				# t6 = tiers[-1].capitalize()
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
