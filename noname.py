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

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='region-content') != None and web_soup.find(class_='region-content') != '':
			col1 = web_soup.find(class_='region-content')
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
		'https://www.vcsedu.org/about',
'https://www.vcsedu.org/about/contact-us',
'https://www.vcsedu.org/about/disclaimer-volusia-county-schools-social-media-sites',
'https://www.vcsedu.org/about/privacy-statement',
'https://www.vcsedu.org/about/volusia-county-schools-the-best-place-learn',
'https://www.vcsedu.org/about/website-accessibility-statement',
'https://www.vcsedu.org/advanced-programs/advanced-placement',
'https://www.vcsedu.org/advanced-programs/advancement-individual-determination-avid',
'https://www.vcsedu.org/advanced-programs/cambridge-advanced-international-certificate-education-aice',
'https://www.vcsedu.org/advanced-programs/dual-enrollment-information',
'https://www.vcsedu.org/advanced-programs/international-baccalaureate',
'https://www.vcsedu.org/alt-education',
'https://www.vcsedu.org/alt-education/2019-2020-school-financial-report',
'https://www.vcsedu.org/alt-education/daytona-juvenile-residential-facility',
'https://www.vcsedu.org/alt-education/alternative-education-department-resources',
'https://www.vcsedu.org/alt-education/highbanks-learning-center',
'https://www.vcsedu.org/alt-education/riverview-learning-center',
'https://www.vcsedu.org/alt-education/school-improvement-plans',
'https://www.vcsedu.org/alt-education/stewart-marchman-residential-adolescent-program',
'https://www.vcsedu.org/alt-education/volusia-branch-jail',
'https://www.vcsedu.org/alt-education/volusia-regional-juvenile-detention-center',
'https://www.vcsedu.org/behavior-initiatives',
'https://www.vcsedu.org/behavior-initiatives/behavior-initiatives-department-resources',
'https://www.vcsedu.org/budget',
'https://www.vcsedu.org/budget/budget-department-resources',
'https://www.vcsedu.org/building-inspection',
'https://www.vcsedu.org/building-inspection/building-and-code-information',
'https://www.vcsedu.org/building-inspection/forms-and-inspection-requests',
'https://www.vcsedu.org/building-inspection/frequently-asked-questions-about-building-permits',
'https://www.vcsedu.org/certification',
'https://www.vcsedu.org/certification/announcements',
'https://www.vcsedu.org/certification/certification-requirements',
'https://www.vcsedu.org/certification/certification-department-resources',
'https://www.vcsedu.org/certification/out-field',
'https://www.vcsedu.org/certification/test-registration',
'https://www.vcsedu.org/chart-schools',
'https://www.vcsedu.org/chart-schools/charter-school-applications',
'https://www.vcsedu.org/chart-schools/current-charter-school-information',
'https://www.vcsedu.org/chart-schools/potential-charter-school-applicants',
'https://www.vcsedu.org/choice-programs',
'https://www.vcsedu.org/choice-programs/family-empowerment-scholarship-fes',
'https://www.vcsedu.org/choice-programs/hope-scholarship',
'https://www.vcsedu.org/choice-programs/school-choice-application',
'https://www.vcsedu.org/choice-programs/school-choice-fair',
'https://www.vcsedu.org/choice-programs/school-choice-frequently-asked-questions',
'https://www.vcsedu.org/choice-programs/school-choice-process',
'https://www.vcsedu.org/choice-programs/teen-parent-program',
'https://www.vcsedu.org/choice-programs/teen-parent-resources',
'https://www.vcsedu.org/community-information-services',
'https://www.vcsedu.org/community-information-services/archived-agenda-and-minutes',
'https://www.vcsedu.org/community-information-services/calendars',
'https://www.vcsedu.org/community-information-services/demographics-and-statistics',
'https://www.vcsedu.org/community-information-services/community-information-department-resources',
'https://www.vcsedu.org/community-information-services/district-advisory-committee',
'https://www.vcsedu.org/community-information-services/family-network-night',
'https://www.vcsedu.org/community-information-services/graduation-information',
'https://www.vcsedu.org/community-information-services/parent-organizations',
'https://www.vcsedu.org/community-information-services/publications',
'https://www.vcsedu.org/community-information-services/public-records',
'https://www.vcsedu.org/community-information-services/required-paperwork-adventhealth-free-physicals',
'https://www.vcsedu.org/community-information-services/teacher-the-year-info',
'https://www.vcsedu.org/community-information-services/vcs-advertisements',
'https://www.vcsedu.org/community-information-services/volusia-county-council-ptas-vccpta',
'https://www.vcsedu.org/cte',
'https://www.vcsedu.org/cte/career-pathways-articulation-agreements',
'https://www.vcsedu.org/cte/cte-action',
'https://www.vcsedu.org/cte/cte-department-resources',
'https://www.vcsedu.org/cte/high-school-showcase',
'https://www.vcsedu.org/cte/industry-certifications',
'https://www.vcsedu.org/cte/internships-and-ojt',
'https://www.vcsedu.org/EDEP',
'https://www.vcsedu.org/EDEP/2022-summer-camp-site-information',
'https://www.vcsedu.org/EDEP/2223-sy-fall-registration-resources',
'https://www.vcsedu.org/employment',
'https://www.vcsedu.org/employment/application-employment',
'https://www.vcsedu.org/employment/application-forms-and-information',
'https://www.vcsedu.org/employment/employment-screenings',
'https://www.vcsedu.org/employment/testing-information',
'https://www.vcsedu.org/employment/types-positions',
'https://www.vcsedu.org/environmental-compliance',
'https://www.vcsedu.org/environmental-compliance/asbestos',
'https://www.vcsedu.org/environmental-compliance/indoor-air-quality',
'https://www.vcsedu.org/environmental-compliance/radon',
'https://www.vcsedu.org/environmental-compliance/regulated-waste',
'https://www.vcsedu.org/environmental-compliance/regulated-petroleum-storage-tanks',
'https://www.vcsedu.org/environmental-compliance/safe-drinking-water',
'https://www.vcsedu.org/environmental-compliance/wastewater-and-water-plants',
'https://www.vcsedu.org/equity',
'https://www.vcsedu.org/equity/americans-disabilities-act-ada',
'https://www.vcsedu.org/equity/equity-department-resources',
'https://www.vcsedu.org/equity/equity-plan',
'https://www.vcsedu.org/equity/laws-and-policies',
'https://www.vcsedu.org/equity/title-ix',
'https://www.vcsedu.org/ese-programs-services',
'https://www.vcsedu.org/ese-programs-services/ese-parentguardian-qand',
'https://www.vcsedu.org/ese-programs-services/ese-upcoming-events',
'https://www.vcsedu.org/ese-programs-services/hearing-and-visual-impairments',
'https://www.vcsedu.org/ese-programs-services/speech-language-impairments',
'https://www.vcsedu.org/ESOL-Title-III',
'https://www.vcsedu.org/ESOL-Title-III/assessments',
'https://www.vcsedu.org/ESOL-Title-III/english-language-learners-ell-plan',
'https://www.vcsedu.org/ESOL-Title-III/parentspadres',
'https://www.vcsedu.org/exceptional-student-education',
'https://www.vcsedu.org/exceptional-student-education/covid-19-activities-and-resources-students-disabilities',
'https://www.vcsedu.org/exceptional-student-education/ese-advisory-committee',
'https://www.vcsedu.org/exceptional-student-education/ese-parent-resources',
'https://www.vcsedu.org/exceptional-student-education/family-support',
'https://www.vcsedu.org/exceptional-student-education/individual-education-plan-iep-compliance',
'https://www.vcsedu.org/exceptional-student-education/mckay-scholarship-important-information',
'https://www.vcsedu.org/exceptional-student-education/parentally-placed-private-school-students-pppss',
'https://www.vcsedu.org/exceptional-student-education/section-504',
'https://www.vcsedu.org/exceptional-student-education/visual-supports-home-and-school-environments',
'https://www.vcsedu.org/exceptional-student-education/volusia-adaptive-assistive-technology-team-vaatt',
'https://www.vcsedu.org/facilities-design',
'https://www.vcsedu.org/facilities-design/bid-documents',
'https://www.vcsedu.org/facilities-design/construction-management-services',
'https://www.vcsedu.org/facilities-design/construction-project-tracking-reports',
'https://www.vcsedu.org/facilities-design/consultant-services',
'https://www.vcsedu.org/facilities-design/plans-and-project-manual-forms-and-documents',
'https://www.vcsedu.org/facilities-services',
'https://www.vcsedu.org/fdlrs',
'https://www.vcsedu.org/fdlrs/child-find',
'https://www.vcsedu.org/fdlrs/fdlrs-resourcestraining',
'https://www.vcsedu.org/federal-programs-and-grants',
'https://www.vcsedu.org/federal-programs-and-grants/2021-2022-title-i-schools',
'https://www.vcsedu.org/federal-programs-and-grants/academic-intervention-and-tutoring',
'https://www.vcsedu.org/federal-programs-and-grants/homeless-non-title-i-schools-title-i-part',
'https://www.vcsedu.org/federal-programs-and-grants/migrant-education-title-i-part-c',
'https://www.vcsedu.org/federal-programs-and-grants/neglecteddelinquent-title-i-part-and-d',
'https://www.vcsedu.org/federal-programs-and-grants/private-non-public-schools',
'https://www.vcsedu.org/federal-programs-and-grants/summer-programs',
'https://www.vcsedu.org/federal-programs-and-grants/title-ii-building-systems-support-excellent-teaching-and-leading',
'https://www.vcsedu.org/federal-programs-and-grants/title-i-programs',
'https://www.vcsedu.org/finance',
'https://www.vcsedu.org/finance/finance-department-resources',
'https://www.vcsedu.org/financial-services',
'https://www.vcsedu.org/financial-services/audit-committee',
'https://www.vcsedu.org/financial-services/charter-schools-audits',
'https://www.vcsedu.org/financial-services/financial-services-department-resources',
'https://www.vcsedu.org/financial-services/financial-transparency',
'https://www.vcsedu.org/financial-services/presentationsworkshops',
'https://www.vcsedu.org/financial-services/presentationsworkshops-archives',
'https://www.vcsedu.org/general-counsel',
'https://www.vcsedu.org/general-counsel/documents',
'https://www.vcsedu.org/general-counsel/union-contracts',
'https://www.vcsedu.org/gifted-program',
'https://www.vcsedu.org/gifted-program/curriculum',
'https://www.vcsedu.org/gifted-program/parents',
'https://www.vcsedu.org/grants-development',
'https://www.vcsedu.org/grants-development/grant-funding-information',
'https://www.vcsedu.org/grants-development/grants-action',
'https://www.vcsedu.org/halifax-behavioral-services',
'https://www.vcsedu.org/halifax-behavioral-services/current-students-and-parents',
'https://www.vcsedu.org/halifax-behavioral-services/day-treatment-program',
'https://www.vcsedu.org/halifax-behavioral-services/inpatient-unit',
'https://www.vcsedu.org/halifax-behavioral-services/re-enrolling-after-discharge-hbs',
'https://www.vcsedu.org/halifax-behavioral-services/title-1-services',
'https://www.vcsedu.org/health-pe',
'https://www.vcsedu.org/health-pe/health-and-physical-education-department-resources',
'https://www.vcsedu.org/health-pe/health-our-schools',
'https://www.vcsedu.org/health-pe/physical-education-programs',
'https://www.vcsedu.org/health-pe/physical-education-waivers',
'https://www.vcsedu.org/home-education',
'https://www.vcsedu.org/home-education/annual-evaluation',
'https://www.vcsedu.org/home-education/enrollment-and-additional-resources',
'https://www.vcsedu.org/home-education/homeschooling-information',
'https://www.vcsedu.org/hospital-homebound',
'https://www.vcsedu.org/hospital-homebound/1-eligibility-information',
'https://www.vcsedu.org/hospital-homebound/2-referral-process',
'https://www.vcsedu.org/hospital-homebound/3-dismissal-process',
'https://www.vcsedu.org/human-resources',
'https://www.vcsedu.org/human-resources/compensation',
'https://www.vcsedu.org/human-resources/employment-records',
'https://www.vcsedu.org/human-resources/new-hires',
'https://www.vcsedu.org/human-resources/pathways-the-principalship',
'https://www.vcsedu.org/human-resources/substitutes',
'https://www.vcsedu.org/imlms',
'https://www.vcsedu.org/imlms/adoption-process',
'https://www.vcsedu.org/imlms/instructional-materials',
'https://www.vcsedu.org/imlms/library-media-information',
'https://www.vcsedu.org/imlms/summer-reading',
'https://www.vcsedu.org/information-technology-security',
'https://www.vcsedu.org/information-technology-security/cybersecure-home',
'https://www.vcsedu.org/information-technology-security/cybersecurity-101',
'https://www.vcsedu.org/information-technology-security/smartphone-security',
'https://www.vcsedu.org/information-technology-security/social-engineering',
'https://www.vcsedu.org/insurance',
'https://www.vcsedu.org/insurance/annual-enrollment',
'https://www.vcsedu.org/insurance/benefit-announcements',
'https://www.vcsedu.org/insurance/benefits-information',
'https://www.vcsedu.org/insurance/cobra',
'https://www.vcsedu.org/insurance/dental-insurance',
'https://www.vcsedu.org/insurance/disability-and-life-insurance',
'https://www.vcsedu.org/insurance/employee-assistance-program-eap',
'https://www.vcsedu.org/insurance/family-status-changes-and-section-125',
'https://www.vcsedu.org/insurance/flexible-spending-account',
'https://www.vcsedu.org/insurance/health-care-reform',
'https://www.vcsedu.org/insurance/health-insurance',
'https://www.vcsedu.org/insurance/new-employee-benefits',
'https://www.vcsedu.org/insurance/overage-dependent-rules',
'https://www.vcsedu.org/insurance/retirement-and-drop',
'https://www.vcsedu.org/insurance/tax-sheltered-annuities-403b-and-roth-plans',
'https://www.vcsedu.org/insurance/vision-insurance',
'https://www.vcsedu.org/insurance/wellness-information',
'https://www.vcsedu.org/insurance/workers-compensation',
'https://www.vcsedu.org/learning-technologies',
'https://www.vcsedu.org/learning-technologies/apple-project',
'https://www.vcsedu.org/learning-technologies/waterford',
'https://www.vcsedu.org/maintenance-operations',
'https://www.vcsedu.org/maintenance-operations/energy-management',
'https://www.vcsedu.org/maintenance-operations/safety-department',
'https://www.vcsedu.org/maintenance-operations/facility-use-and-rentals',
'https://www.vcsedu.org/mathematics',
'https://www.vcsedu.org/mathematics/6-8-mathematics',
'https://www.vcsedu.org/mathematics/9-12-mathematics',
'https://www.vcsedu.org/mathematics/k-5-mathematics',
'https://www.vcsedu.org/mental-wellness',
'https://www.vcsedu.org/mental-wellness/bully-prevention',
'https://www.vcsedu.org/mental-wellness/community-resources',
'https://www.vcsedu.org/mental-wellness/crisis-response-information',
'https://www.vcsedu.org/mental-wellness/lesbian-gay-bisexual-transgender-and-questioning-lgbtq',
'https://www.vcsedu.org/mental-wellness/mental-and-emotional-health-education-videos',
'https://www.vcsedu.org/mental-wellness/mental-wellness-teams',
'https://www.vcsedu.org/mental-wellness/re-entry-meeting',
'https://www.vcsedu.org/mental-wellness/substance-abuse',
'https://www.vcsedu.org/mental-wellness/threat-assessment',
'https://www.vcsedu.org/mental-wellness/youth-mental-health-first-aid',
'https://www.vcsedu.org/operations-services',
'https://www.vcsedu.org/parent-family-engagement',
'https://www.vcsedu.org/parent-family-engagement/parent-and-family-engagement-plans',
'https://www.vcsedu.org/parent-family-engagement/parent-information',
'https://www.vcsedu.org/payroll',
'https://www.vcsedu.org/payroll/payroll-department-resources',
'https://www.vcsedu.org/performing-visual-arts',
'https://www.vcsedu.org/performing-visual-arts/dance',
'https://www.vcsedu.org/performing-visual-arts/music',
'https://www.vcsedu.org/performing-visual-arts/performing-arts',
'https://www.vcsedu.org/performing-visual-arts/theatre',
'https://www.vcsedu.org/performing-visual-arts/visual-arts',
'https://www.vcsedu.org/planning-business-services',
'https://www.vcsedu.org/planning-business-services/growth-management',
'https://www.vcsedu.org/planning-business-services/half-cent-sales-tax',
'https://www.vcsedu.org/planning-business-services/interactive-maps',
'https://www.vcsedu.org/planning-business-services/real-estate',
'https://www.vcsedu.org/problem-solving-rti',
'https://www.vcsedu.org/problem-solving-rti/problem-solving-department-resources',
'https://www.vcsedu.org/professional-learning',
'https://www.vcsedu.org/professional-learning/announcements',
'https://www.vcsedu.org/professional-learning/college-universityinformation',
'https://www.vcsedu.org/professional-learning/endorsements',
'https://www.vcsedu.org/professional-learning/ese-credit-requirement',
'https://www.vcsedu.org/professional-learning/impact-instructional-coaching-program',
'https://www.vcsedu.org/professional-learning/mypgs',
'https://www.vcsedu.org/professional-learning/professional-growth-and-leadership-opportunities',
'https://www.vcsedu.org/professional-learning/professional-learning-commitments',
'https://www.vcsedu.org/professional-learning/professional-learning-standards-and-statutes',
'https://www.vcsedu.org/professional-learning/reading-endorsement',
'https://www.vcsedu.org/professional-learning/service-credit',
'https://www.vcsedu.org/professional-learning/service-non-employees',
'https://www.vcsedu.org/professional-learning/teacher-tuition-reimbursement',
'https://www.vcsedu.org/professional-learning/transfer-credit',
'https://www.vcsedu.org/professional-learning/volusia-chats',
'https://www.vcsedu.org/professional-learning/volusia-reads',
'https://www.vcsedu.org/professional-standards',
'https://www.vcsedu.org/professional-standards/professional-standards-department-resources',
'https://www.vcsedu.org/professional-standards/jessica-lunsford-act-jla',
'https://www.vcsedu.org/purchasing',
'https://www.vcsedu.org/purchasing/charter-buses',
'https://www.vcsedu.org/purchasing/customer-satisfaction-survey',
'https://www.vcsedu.org/purchasing/purchasing-department-resources',
'https://www.vcsedu.org/purchasing/notice-vendors',
'https://www.vcsedu.org/purchasing/policies-and-procedures',
'https://www.vcsedu.org/purchasing/project-portfolio',
'https://www.vcsedu.org/purchasing/search-contracts',
'https://www.vcsedu.org/purchasing/search-solicitations',
'https://www.vcsedu.org/purchasing/special-events',
'https://www.vcsedu.org/purchasing/travel-services',
'https://www.vcsedu.org/REA',
'https://www.vcsedu.org/REA/accountability',
'https://www.vcsedu.org/REA/assessment',
'https://www.vcsedu.org/REA/research',
'https://www.vcsedu.org/reading-ela',
'https://www.vcsedu.org/records-management',
'https://www.vcsedu.org/records-management/current-student-records',
'https://www.vcsedu.org/records-management/directions-site',
'https://www.vcsedu.org/records-management/education-verifications',
'https://www.vcsedu.org/records-management/subpoenas-student-records',
'https://www.vcsedu.org/records-management/transcripts',
'https://www.vcsedu.org/recruitment-and-retention',
'https://www.vcsedu.org/recruitment-and-retention/florida-future-educators-america-ffea',
'https://www.vcsedu.org/recruitment-and-retention/minority-recruitment',
'https://www.vcsedu.org/recruitment-and-retention/pathways-school-counseling',
'https://www.vcsedu.org/recruitment-and-retention/relocation-information',
'https://www.vcsedu.org/recruitment-and-retention/speech-language-pathologist-recruitment',
'https://www.vcsedu.org/recruitment-and-retention/student-internships',
'https://www.vcsedu.org/recruitment-and-retention/upcoming-hiring-events',
'https://www.vcsedu.org/recruitment-and-retention/vcs-new-teachers',
'https://www.vcsedu.org/recruitment-and-retention/why-volusia',
'https://www.vcsedu.org/sac',
'https://www.vcsedu.org/sac/sac-department-resources',
'https://www.vcsedu.org/sac/sac-information',
'https://www.vcsedu.org/sac/sip-information',
'https://www.vcsedu.org/school-board',
'https://www.vcsedu.org/school-board/agendas-and-minutes',
'https://www.vcsedu.org/school-board/legislative-information',
'https://www.vcsedu.org/school-board/meeting-information',
'https://www.vcsedu.org/school-board/resolutions',
'https://www.vcsedu.org/school-board/school-board-members',
'https://www.vcsedu.org/school-board/school-board-members/anita-burnette',
'https://www.vcsedu.org/school-board/school-board-members/carl-persis',
'https://www.vcsedu.org/school-board/school-board-members/jamie-haynes',
'https://www.vcsedu.org/school-board/school-board-members/linda-cuthbert',
'https://www.vcsedu.org/school-board/school-board-members/ruben-colon',
'https://www.vcsedu.org/school-board/school-board-policies',
'https://www.vcsedu.org/school-board/upcoming-school-board-meeting',
'https://www.vcsedu.org/school-counseling',
'https://www.vcsedu.org/school-counseling/elementary-school-counseling',
'https://www.vcsedu.org/school-counseling/graduation-requirements',
'https://www.vcsedu.org/school-counseling/high-school-counseling',
'https://www.vcsedu.org/school-counseling/middle-school-counseling',
'https://www.vcsedu.org/school-counseling/student-progression-plan',
'https://www.vcsedu.org/school-maps',
'https://www.vcsedu.org/schools/school-hours',
'https://www.vcsedu.org/schools/maps-and-directions',
'https://www.vcsedu.org/school-psychological-services',
'https://www.vcsedu.org/school-psychological-services/early-warning-signs-risk-students',
'https://www.vcsedu.org/school-psychological-services/intern-application-process',
'https://www.vcsedu.org/school-psychological-services/private-practitioners',
'https://www.vcsedu.org/school-psychological-services/private-schools',
'https://www.vcsedu.org/school-psychological-services/problem-solving-team',
'https://www.vcsedu.org/school-social-services',
'https://www.vcsedu.org/school-social-services/attendance',
'https://www.vcsedu.org/school-social-services/bullying-what-parents-can-do',
'https://www.vcsedu.org/school-social-services/crisis-response',
'https://www.vcsedu.org/school-social-services/school-social-services-department-resources',
'https://www.vcsedu.org/school-social-services/drug-and-alcohol-education',
'https://www.vcsedu.org/school-social-services/florida-labor-law',
'https://www.vcsedu.org/school-social-services/foster-care',
'https://www.vcsedu.org/school-social-services/helping-our-children-transition',
'https://www.vcsedu.org/school-social-services/homeless-children-and-youth',
'https://www.vcsedu.org/school-social-services/if-someone-overdosing-call-911-and-save-life',
'https://www.vcsedu.org/school-social-services/improving-your-childs-attendance',
'https://www.vcsedu.org/school-social-services/making-parent-teacher-conferences-work-your-child',
'https://www.vcsedu.org/school-social-services/safe-and-drug-free-schools',
'https://www.vcsedu.org/school-social-services/school-based-mental-health-resources',
'https://www.vcsedu.org/school-social-services/school-social-services-procedural-manual',
'https://www.vcsedu.org/school-social-services/school-social-work',
'https://www.vcsedu.org/school-social-services/signs-and-symptoms-teen-drinking-or-drug-use',
'https://www.vcsedu.org/school-social-services/supporting-military-youth-and-families',
'https://www.vcsedu.org/school-social-services/talking-your-children-about-alcohol-and-drugs',
'https://www.vcsedu.org/schoolwaycafe',
'https://www.vcsedu.org/schoolwaycafe/free-and-reduced-meal-applications',
'https://www.vcsedu.org/schoolwaycafe/fun-facts-and-faqs',
'https://www.vcsedu.org/schoolwaycafe/menus-and-prices',
'https://www.vcsedu.org/schoolwaycafe/policies',
'https://www.vcsedu.org/schoolwaycafe/special-diet-request',
'https://www.vcsedu.org/science',
'https://www.vcsedu.org/science/6-8-science',
'https://www.vcsedu.org/science/9-12-science',
'https://www.vcsedu.org/science/k-5-science',
'https://www.vcsedu.org/science/science-competitions',
'https://www.vcsedu.org/secondary-curriculum',
'https://www.vcsedu.org/secondary-curriculum/program-studies',
'https://www.vcsedu.org/security',
'https://www.vcsedu.org/security/district-safety-and-security-update',
'https://www.vcsedu.org/security/school-guardians',
'https://www.vcsedu.org/security/security-plan',
'https://www.vcsedu.org/security/student-hero-award-program',
'https://www.vcsedu.org/security/visiting-our-schools',
'https://www.vcsedu.org/SEL',
'https://www.vcsedu.org/SEL/sel-volusia-county-schools',
'https://www.vcsedu.org/social-studies',
'https://www.vcsedu.org/social-studies/social-studies-department-resources',
'https://www.vcsedu.org/social-studies/heritage-and-history-months',
'https://www.vcsedu.org/social-studies/social-studies-fair',
'https://www.vcsedu.org/special-programs',
'https://www.vcsedu.org/special-programs/athletics',
'https://www.vcsedu.org/special-programs/drivers-education',
'https://www.vcsedu.org/strategic-partnerships',
'https://www.vcsedu.org/strategic-partnerships/adventhealth',
'https://www.vcsedu.org/strategic-partnerships/daytona-tortugas',
'https://www.vcsedu.org/student-accounting-services',
'https://www.vcsedu.org/student-accounting-services/gender-and-ethnicity-reports',
'https://www.vcsedu.org/student-accounting-services/gender-and-ethnicity-reports-archives',
'https://www.vcsedu.org/student-accounting-services/membership-reports',
'https://www.vcsedu.org/student-accounting-services/membership-reports-archives',
'https://www.vcsedu.org/student-health-services',
'https://www.vcsedu.org/student-health-services/administration-medication',
'https://www.vcsedu.org/student-health-services/clinic-information',
'https://www.vcsedu.org/student-health-services/common-childhood-diseases',
'https://www.vcsedu.org/student-health-services/student-health-services-department-resources',
'https://www.vcsedu.org/student-health-services/florida-kidcare-health-insurance',
'https://www.vcsedu.org/student-health-services/school-entry-information',
'https://www.vcsedu.org/student-health-services/student-health-records',
'https://www.vcsedu.org/student-services',
'https://www.vcsedu.org/student-services/government-relations',
'https://www.vcsedu.org/student-services/implementation-plans',
'https://www.vcsedu.org/student-services/student-registration',
'https://www.vcsedu.org/student-transportation',
'https://www.vcsedu.org/student-transportation/bus-route-information',
'https://www.vcsedu.org/student-transportation/meet-the-transportation-team',
'https://www.vcsedu.org/student-transportation/parent-resources',
'https://www.vcsedu.org/student-transportation/school-bus-safety-measures',
'https://www.vcsedu.org/student-transportation/transportation-business-partners',
'https://www.vcsedu.org/superintendent',
'https://www.vcsedu.org/superintendent/organizational-chart',
'https://www.vcsedu.org/superintendent/superintendents-cabinet',
'https://www.vcsedu.org/teaching-leading-learning',
'https://www.vcsedu.org/teaching-leading-learning/teaching-leading-and-learning-department-resources',
'https://www.vcsedu.org/technology-services',
'https://www.vcsedu.org/technology-services/copy-center',
'https://www.vcsedu.org/technology-services/parent-and-student-technical-guide',
'https://www.vcsedu.org/technology-services/vportal',
'https://www.vcsedu.org/technology-services/vportal-down-information',
'https://www.vcsedu.org/transition',
'https://www.vcsedu.org/transition/deferment',
'https://www.vcsedu.org/transition/transition-department-resources',
'https://www.vcsedu.org/transition/project-search',
'https://www.vcsedu.org/transition/transition-agencies',
'https://www.vcsedu.org/volunteer-partnership',
'https://www.vcsedu.org/volunteer-partnership/awards',
'https://www.vcsedu.org/volunteer-partnership/business-partners',
'https://www.vcsedu.org/volunteer-partnership/college-students',
'https://www.vcsedu.org/volunteer-partnership/volunteerpartnership-department-resources',
'https://www.vcsedu.org/volunteer-partnership/high-school-youth-partnership-program',
'https://www.vcsedu.org/volunteer-partnership/mentors',
'https://www.vcsedu.org/volunteer-partnership/speakers-bureau',
'https://www.vcsedu.org/volunteer-partnership/volunteers-vips',
'https://www.vcsedu.org/volusia-leads',
'https://www.vcsedu.org/volusia-leads/professional-learning-members',
'https://www.vcsedu.org/volusia-leads/social-media',
'https://www.vcsedu.org/VPK',
'https://www.vcsedu.org/VPK/family-resources',
'https://www.vcsedu.org/VPK/kindergarten-roundup',
'https://www.vcsedu.org/VPK/voluntary-prekindergarten-school-year-blended-programs',
'https://www.vcsedu.org/VPK/voluntary-prekindergarten-school-year-program',
'https://www.vcsedu.org/VPK/voluntary-prekindergarten-summer-program',
'https://www.vcsedu.org/VPK/vpk-registration',
'https://www.vcsedu.org/world-languages',
'https://www.vcsedu.org/world-languages/american-sign-language-asl',
'https://www.vcsedu.org/world-languages/chinese',
'https://www.vcsedu.org/world-languages/florida-seal-biliteracy',
'https://www.vcsedu.org/world-languages/french',
'https://www.vcsedu.org/world-languages/german',
'https://www.vcsedu.org/world-languages/hispanic-heritage-month',
'https://www.vcsedu.org/world-languages/international-student-exchange',
'https://www.vcsedu.org/world-languages/japanese',
'https://www.vcsedu.org/world-languages/russian',
'https://www.vcsedu.org/world-languages/spanish',
'https://www.vcsedu.org/world-languages/world-languages-festival',
'https://www.vcsedu.org/world-languages/world-languages-taught',
'https://www.vcsedu.org/students/dress-code',
'https://www.vcsedu.org/parents/beginning-school-year-forms',
'https://www.vcsedu.org/parents/parent-portal',
'https://www.vcsedu.org/community/job-fair-teens-online-portal',
	]
	mainfolder = 'vcsedu'
	school_name = 'vcsedu'
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
