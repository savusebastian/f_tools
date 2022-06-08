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
		if web_soup.find(class_='ptl_page') != None and web_soup.find(class_='ptl_page') != '':
			col1 = web_soup.find(class_='ptl_page')
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
		'https://www.edmonds.wednet.edu/about',
'https://www.edmonds.wednet.edu/about/a_look_at_our_district',
'https://www.edmonds.wednet.edu/about/a_look_at_our_district/enrollment_reports',
'https://www.edmonds.wednet.edu/about/a_look_at_our_district/budget_information',
'https://www.edmonds.wednet.edu/about/district__school_learning_improvement',
'https://www.edmonds.wednet.edu/about/frequently_requested_forms',
'https://www.edmonds.wednet.edu/about/frequently_requested_forms/harassment__intimidation__and_bullying_reporting',
'https://www.edmonds.wednet.edu/about/language_access',
'https://www.edmonds.wednet.edu/about/language_access/servicios_de_idiomas_-_espa_ol___spanish_',
'https://www.edmonds.wednet.edu/about/language_access/d_ch_v__ng_n_ng__-_ti_ng_vi_t___vietnamese_',
'https://www.edmonds.wednet.edu/about/language_access/_arabic_',
'https://www.edmonds.wednet.edu/about/language_access/__korean_',
'https://www.edmonds.wednet.edu/about/language_access/__russian_',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452233',
'https://www.edmonds.wednet.edu/about/news___publications',
'https://www.edmonds.wednet.edu/news/what_s_new',
'https://www.edmonds.wednet.edu/news/archived_news',
'https://www.edmonds.wednet.edu/about/news___publications/archived_news_2016-17',
'https://www.edmonds.wednet.edu/about/news___publications/district_e_news',
'https://www.edmonds.wednet.edu/about/news___publications/district_newsletter',
'https://www.edmonds.wednet.edu/cms/one.aspx?portalid=306754&pageid=1721873',
'https://www.edmonds.wednet.edu/about/news___publications/school_videos_to_students',
'https://www.edmonds.wednet.edu/about/news___publications/2020_calendar_art',
'https://www.edmonds.wednet.edu/about/news___publications/closures___delays',
'https://www.edmonds.wednet.edu/about/organizational_chart',
'https://www.edmonds.wednet.edu/about/public_notices_and_records',
'https://www.edmonds.wednet.edu/about/school_board',
'https://www.edmonds.wednet.edu/about/school_board/school_board_redistricting',
'https://www.edmonds.wednet.edu/about/school_board/directors',
'https://www.edmonds.wednet.edu/about/school_board/map_of_board_member_districts',
'https://www.edmonds.wednet.edu/about/school_board/schedule_of_board_meetings',
'https://www.edmonds.wednet.edu/about/school_board/board_meeting_calendar',
'https://go.boarddocs.com/wa/edmonds/Board.nsf/Public',
'https://www.edmonds.wednet.edu/about/school_board/nominate_an_individual_for_school_board_celebrates',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451712',
'https://www.edmonds.wednet.edu/about/school_board/process_to_address_your_concerns',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2022',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2021',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2020',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2019',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2018',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2017',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2016',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2015',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2014',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2013',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2012',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2011',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2010',
'https://www.edmonds.wednet.edu/about/school_board/approved_interlocal_agreements/approved_interlocal_agreements_2009',
'https://www.edmonds.wednet.edu/about/school_board/resolution_18-22__sensible_gun_safety',
'https://www.edmonds.wednet.edu/about/school_board/application_for_student_advisor_to_the_board',
'https://www.youtube.com/user/EdmondsSD',
'https://go.boarddocs.com/wa/edmonds/Board.nsf/Public?open&id=policies',
'https://www.edmonds.wednet.edu/about/strategic_plan',
'https://www.edmonds.wednet.edu/about/superintendent',
'https://www.edmonds.wednet.edu/about/superintendent/superintendent_s_biography',
'https://www.edmonds.wednet.edu/about/superintendent/safe_schools_alert',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451712',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=3366892',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1169328',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=6773610',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=7224662',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1028964',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=2217806',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=6765576',
'https://www.edmonds.wednet.edu/schools',
'https://www.edmonds.wednet.edu/schools/elementary_schools',
'https://www.edmonds.wednet.edu/schools/middle_schools',
'https://www.edmonds.wednet.edu/schools/high_schools',
'https://www.edmonds.wednet.edu/schools/online_learning_2021-22',
'https://www.edmonds.wednet.edu/schools/preschool',
'https://www.edmonds.wednet.edu/schools/boundary_maps__feeder_patterns',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/Image/About%20Us/News%20&%20Publications/2019-20/2019-2020%20Boundary%20Map%20Elementary%2011.19.2019.pdf',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/Image/About%20Us/News%20&%20Publications/2019-20/2019-2020%20Boundary%20Map%20Secondary%2011.19.2019.pdf',
'https://www.edmonds.wednet.edu/schools/boundary_maps__feeder_patterns/feeder_patterns',
'https://esdfinder.site/',
'https://www.edmonds.wednet.edu/schools/start___dismissal_times',
'https://www.edmonds.wednet.edu/departments',
'https://www.edmonds.wednet.edu/departments/athletics',
'https://www.edmonds.wednet.edu/departments/athletics/athletic_schedules',
'https://www.edmonds.wednet.edu/departments/athletics/athletic_contacts',
'https://www.edmonds.wednet.edu/departments/athletics/forms',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/Image/Departments/Athletics/Handbook/Student%20Athletic%20Handbook%208.22.17.pdf',
'https://www.edmonds.wednet.edu/departments/athletics/summer_activities',
'https://www.edmonds.wednet.edu/departments/business_and_finance',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/citizen_s_guide_to_the_budget',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/state_auditor_reports',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/fundraising',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/accounting_and_accounts_payable',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/budget_and_finance',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/risk_management__audit_and_internal_controls',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/purchasing',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/purchasing/bid_opportunities',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/purchasing/terms',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/purchasing/small_works_roster',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/purchasing/public_works_process',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/purchasing/public_works_award_postings',
'https://www.edmonds.wednet.edu/departments/business_and_finance/business_services/a_s_b_fund_balances',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=525918',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=525918',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=525621',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=525939',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526077',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526088',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526096',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526124',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526273',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526287',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526297',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526312',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=489271',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526347',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=525714',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526504',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526401',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=526514',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=528331',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=529298',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=530743',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=530795',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=530820',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=530926',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=531013',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=531032',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=531143',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=531484',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=531179',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=531498',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=451606',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451810',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452233',
'https://www.edmonds.wednet.edu/departments/capital_projects',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452952',
'https://www.edmonds.wednet.edu/departments/capital_projects/consultant_roster',
'https://www.edmonds.wednet.edu/departments/capital_projects/capitol_projects_staff',
'https://www.edmonds.wednet.edu/departments/capital_projects/awarded_public_works_contracts__300_k',
'https://www.edmonds.wednet.edu/departments/capital_projects/c_p_o_presentations_to_the_school_board',
'https://www.edmonds.wednet.edu/departments/capital_projects/links_of_interest',
'https://www.edmonds.wednet.edu/departments/facilities_operations',
'https://www.edmonds.wednet.edu/departments/facilities_operations',
'http://p13cdn4static.sharpschool.com/UserFiles/Servers/Server_306670/File/Departments/Facilities%20and%20Operations/01_EDSC%202020%20CFP%20Final.pdf',
'https://www.edmonds.wednet.edu/departments/facilities_operations/capital_partnership_program',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452921',
'https://www.edmonds.wednet.edu/departments/facilities_operations/custodial_services',
'https://www.edmonds.wednet.edu/departments/facilities_operations/maintenance_overview',
'https://www.edmonds.wednet.edu/departments/facilities_operations/maintenance_overview/volunteer_beautification_of_school_grounds',
'https://www.edmonds.wednet.edu/departments/facilities_operations/maintenance_overview/grounds_maintenance',
'https://www.edmonds.wednet.edu/departments/facilities_operations/safety___security',
'https://www.edmonds.wednet.edu/departments/facilities_operations/safety___security/safety',
'https://www.edmonds.wednet.edu/departments/facilities_operations/volunteer_use',
'https://www.edmonds.wednet.edu/departments/communications',
'https://www.edmonds.wednet.edu/departments/communications/closures_and_delays',
'https://edmonds.sjc1.qualtrics.com/jfe/form/SV_bdr2FMk8ev92liB',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451656',
'https://www.edmonds.wednet.edu/departments/communications/text_messaging',
'https://www.edmonds.wednet.edu/departments/communications/students_of_the_month_form',
'https://www.edmonds.wednet.edu/departments/communications/remind',
'https://www.edmonds.wednet.edu/departments/communications/mobile_app',
'https://www.edmonds.wednet.edu/departments/communications/skylert',
'https://www.edmonds.wednet.edu/departments/communications/website_feedback',
'https://www.edmonds.wednet.edu/departments/communications/2021_featured_graduates',
'https://www.edmonds.wednet.edu/departments/communications/feedback_-_questions',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/meet_the_staff',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_teams',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_teams/librarians_for_equity_and_diversity___l_e_a_d_',
'https://www.edmonds.wednet.edu/programs/multilingual_education__ml_',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/family_and_community_engagement',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/family_and_community_engagement/natural_leaders',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/family_and_community_engagement/family_survey',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/families_in_transition__mckinney_vento_foster_care',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/families_in_transition__mckinney_vento_foster_care/homeless__mc_kinney_vento_information',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/families_in_transition__mckinney_vento_foster_care/foster_care_information',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/families_in_transition__mckinney_vento_foster_care/edmonds_hub',
'https://www.edmonds.wednet.edu/community/equity_alliance_for_achievement__eaach_',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/college_and_career_readiness',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/resources_for_families',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/community_partnerships',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/community_partnerships/equity_alliance_for_achievement___e_a_a_c_h_',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/community_partnerships/equity_alliance_for_achievement___e_a_a_c_h_/community_resources__recursos_de_la_comunidad',
'https://www.edmonds.wednet.edu/community/equity_alliance_for_achievement__eaach_',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/juneteenth',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/black_lives_matter___district_equity',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/black_lives_matter___district_equity/b_l_m_month_of_action',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/black_lives_matter___district_equity/b_l_m_resources_for_families',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/superintendent_student_advisory_committee',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=452486',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_monthly_themes_committees',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_monthly_themes_committees/may_theme',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_monthly_themes_committees/june_theme',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_monthly_themes_committees/september_theme',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_monthly_themes_committees/october_theme',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/equity_monthly_themes_committees/march_theme',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/2_s_l_g_b_t_q_i_a__inclusivity',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/m_t_s_s___multi-_tiered_system_of_supports_',
'https://www.edmonds.wednet.edu/departments/food___nutrition_services',
'https://wa-edmonds-lite.intouchreceipting.com/',
'https://www.myschoolmenus.com/instance/189/district/213',
'https://wa-edmonds.intouchreceipting.com/',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=451845',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=593874',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=451840',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=37311454',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=37668689',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=38252069',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employment_home',
'https://www.applitrack.com/edmonds/onlineapp/',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employment_home/application_information',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employment_home/recruitment_events',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451851',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/benefits',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/payroll',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/administrative_assistants',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/bus_drivers',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/cabinet__formerly_superintendent_s_staff_',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/classified_support_staff_of_edmonds___paraeducator',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/coaches',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/custodians__food_service_drivers__and_warehouse_em',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/edmonds_education_association',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/edmonds_managers_association',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/edmonds_principals_association',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/e_s_d_association_of_office_personnel',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/food_service',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/maintenance',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employee_agreements/professional-_technical',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/evaluation_forms',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/evaluation_forms/e_e_a_evaluation_forms___professional_teaching_sta',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/evaluation_forms/administrator_evaluation_forms',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/salary_schedules',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/nondiscrimination_policy',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/title_i_notification',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/TEA_program',
'https://www.applitrack.com/Edmonds/onlineapp/',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/substitutes',
'https://www.edmonds.wednet.edu/departments/transportation_services_public_home',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=33441152',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=33443502',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=33443962',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=33454671',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=33455433',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=33499673',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=32808564',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=37459011',
'https://www.edmonds.wednet.edu/departments/special_education',
'https://www.edmonds.wednet.edu/departments/special_education/behavioral_intervention',
'https://www.edmonds.wednet.edu/departments/special_education/child_find',
'https://www.edmonds.wednet.edu/departments/special_education/dispute_resolution',
'https://www.edmonds.wednet.edu/departments/special_education/early_learning_programs',
'https://aecc.edmonds.wednet.edu/',
'https://www.edmonds.wednet.edu/departments/special_education/early_learning_programs/developmental_milestones',
'https://www.edmonds.wednet.edu/departments/special_education/elementary_programs',
'https://www.edmonds.wednet.edu/departments/special_education/elementary_programs/developmental_kindergarten',
'https://www.edmonds.wednet.edu/departments/special_education/elementary_programs/intensive_academic_support',
'https://www.edmonds.wednet.edu/departments/special_education/elementary_programs/intensive_social_emotional_support',
'https://www.edmonds.wednet.edu/departments/special_education/elementary_programs/learning_support',
'https://www.edmonds.wednet.edu/departments/special_education/evaluation_process',
'https://www.edmonds.wednet.edu/departments/special_education/i_e_p_online_connect_for_parents',
'https://www.edmonds.wednet.edu/departments/special_education/procedural_safeguards__parent_and_student_rights',
'https://www.edmonds.wednet.edu/departments/special_education/programs_and_services',
'https://sites.google.com/edmonds.wednet.edu/edmonds-school-district/home',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452248',
'https://www.edmonds.wednet.edu/departments/special_education/programs_and_services/health_services',
'https://www.edmonds.wednet.edu/departments/special_education/programs_and_services/occupational_therapy__physical_therapy',
'https://www.edmonds.wednet.edu/departments/special_education/programs_and_services/school_psychology',
'https://www.edmonds.wednet.edu/departments/special_education/programs_and_services/speech__language__and_hearing',
'https://www.edmonds.wednet.edu/departments/special_education/programs_and_services/visually_impaired',
'https://www.edmonds.wednet.edu/departments/special_education/records',
'https://www.edmonds.wednet.edu/departments/special_education/resources',
'https://www.edmonds.wednet.edu/departments/special_education/resources/federal_agencies_and_national_resources',
'https://www.edmonds.wednet.edu/departments/special_education/resources/local_and_state_agencies_and_resources',
'https://www.edmonds.wednet.edu/departments/special_education/resources/online_support_groups',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452124',
'https://www.edmonds.wednet.edu/departments/special_education/secondary_programs',
'https://www.edmonds.wednet.edu/departments/special_education/secondary_programs/intensive_social_emotional_support',
'https://www.edmonds.wednet.edu/departments/special_education/secondary_programs/learning_support',
'https://www.edmonds.wednet.edu/departments/special_education/secondary_programs/lifeskills___intensive_academic_support_',
'https://www.edmonds.wednet.edu/departments/special_education/special_education_p_t_s_a',
'https://www.edmonds.wednet.edu/departments/special_education/special_education_terms',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451954',
'https://www.edmonds.wednet.edu/departments/special_education/transportation',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/school_or_district_assessments',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/school_or_district_assessments/i-_ready',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/school_or_district_assessments/i-_ready',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/district_data',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/test_schedules',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/student_resources_to_prepare_for_online_testing',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/student_resources_to_prepare_for_online_testing/online_test_preparation_-_web_version',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/test_results',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/test_results/test_scores_in_family_access',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/test_results/sample_s_b_a_e_l_a_score_report',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/test_results/sample_s_b_a_math_score_report',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/test_results/sample_w_c_a_s_science_score_report',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/assessment/state_testing/additional_parent__guardian_resources',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=452293',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/english_language_arts',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/health_and_fitness',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/health_and_fitness/sexual_health_and_disease_prevention',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/health_and_fitness/sexual_health_and_disease_prevention/sexual_health___disease_prevention_curriculum',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/mathematics',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/science___s_t_e_m',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/social_studies',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/understanding_your_child_s_progress',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452446',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/science___s_t_e_m',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/english_language_arts',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/health_and_fitness',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/health_and_fitness/sexual_health_and_disease_prevention',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/health_and_fitness/s_o_s_signs_of_suicide_prevention',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/mathematics',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/social_studies',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/social_studies/district_approved_social_studies_resources',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=1190387',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452446',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/instructional_materials',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/instructional_materials/instructional_materials_committee',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/english_language_arts',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=542208',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/health_and_fitness',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/health_and_fitness/sexual_health_and_disease_prevention',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/middle_school_7-8/health_and_fitness/s_o_s_signs_of_suicide_prevention',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/mathematics',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/mathematics/edmonds_school_district_math_flow_chart',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/science___s_t_e_m',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/social_studies',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/world_languages',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/high_school_9-12/world_languages/world_language_proficiency_credits',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452446',
'https://www.edmonds.wednet.edu/departments/student_services',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451882',
'https://www.edmonds.wednet.edu/departments/student_services/title_i__l_a_p',
'https://www.edmonds.wednet.edu/departments/student_services/title_i__l_a_p/title_1_compacts_-_grades_k-4',
'https://www.edmonds.wednet.edu/departments/student_services/section_504',
'https://www.edmonds.wednet.edu/departments/student_services/elementary_counseling',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Departments/Student%20Services/Secondary%20Counseling%20&%20Student%20Support/SecondarySupportStaffFlowChart.pdf',
'https://www.edmonds.wednet.edu/departments/student_services/staff',
'https://www.edmonds.wednet.edu/departments/student_services/citizen_complaint_process',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=1338636',
'https://www.edmonds.wednet.edu/departments/technology',
'https://www.edmonds.wednet.edu/departments/technology/instructional_technology',
'https://www.edmonds.wednet.edu/departments/technology/digital_citizenship',
'https://www.edmonds.wednet.edu/departments/technology/library_resources',
'https://www.edmonds.wednet.edu/departments/technology/status_of_key_products',
'https://www.edmonds.wednet.edu/programs',
'https://cte.edmonds.wednet.edu/',
'https://www.edmonds.wednet.edu/programs/high_school__college__career',
'https://www.edmonds.wednet.edu/programs/high_school__college__career/contracted_learning_for_individual_pacing___c_l_i_',
'https://www.edmonds.wednet.edu/programs/high_school__college__career/vocational_programs',
'https://sites.google.com/edmonds.wednet.edu/workadjustment/home',
'https://sites.google.com/edmonds.wednet.edu/seps',
'https://www.edmonds.wednet.edu/programs/high_school__college__career/high_school_completion',
'https://www.edmonds.wednet.edu/programs/high_school__college__career/international_exchange_students',
'https://www.edmonds.wednet.edu/programs/high_school__college__career/running_start',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/d_h_h_staff_contact_information',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/program_services',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/requesting_interpreter_services',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/preschool__kindergarten_classroom',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/primary_classroom',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/intermediate_classroom',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/middle_school_classroom',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/high_school',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/newsletters',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/deaf_events__activites__trainings',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/extra_curricular_activities',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/schools_and_driving_directions',
'https://www.edmonds.wednet.edu/programs/deaf_and_hard_of_hearing___d_h_h_/calendar',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_',
'https://aecc.edmonds.wednet.edu/',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/early_childhood_education_and_assistance_program',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/early_childhood_education_and_assistance_program/Eligibility',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/early_childhood_education_and_assistance_program/application',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/early_childhood_education_and_assistance_program/e_c_e_a_p_sites',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/early_childhood_education_and_assistance_program/frequently_asked_questions',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/early_childhood_education_and_assistance_program/contact_us',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/family_pre-_k',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/family_pre-_k/family_pre-_k_locations_and_schedule',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/family_pre-_k/meet_our_pre-_k_facilitators',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/family_pre-_k/how_to_apply',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/family_pre-_k/frequently_asked_questions',
'https://www.edmonds.wednet.edu/programs/preschool__pre-k_/community_resources',
'https://www.edmonds.wednet.edu/programs/multilingual_education__ml_',
'https://www.edmonds.wednet.edu/programs/multilingual_education__ml_/multilingual_learners',
'https://www.edmonds.wednet.edu/programs/multilingual_education__ml_/dual-_language',
'https://www.edmonds.wednet.edu/programs/multilingual_education__ml_/indian_education',
'https://www.edmonds.wednet.edu/programs/multilingual_education__ml_/educational_resources',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/referral_forms_k_-_7th_grade',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/testing_dates__assessment__and_identification',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/testing_dates__assessment__and_identification/cognitive_abilities_test',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/testing_dates__assessment__and_identification/identification_and_notification',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/testing_dates__assessment__and_identification/appeals_process',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/information_sessions__presentations___handouts',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/remote_learning',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/k-12_programs',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/frequently_asked_questions_-_hi-cap_program',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/frequently_asked_questions_-_challenge_grades_1-6',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/review__change_of_placement_and_exit',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/transportation',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/resources___links',
'https://www.edmonds.wednet.edu/programs/highly_capable___gifted/calendar',
'https://www.edmonds.wednet.edu/programs/homeschool',
'https://www.edmonds.wednet.edu/programs/move_60_',
'https://www.edmonds.wednet.edu/programs/move_60_/move_60_registration_packets',
'https://www.edmonds.wednet.edu/programs/move_60_/move_60__school_schedules',
'https://www.edmonds.wednet.edu/programs/move_60_/move_60_early_learning',
'https://www.edmonds.wednet.edu/programs/move_60_/move_60__nutrition',
'https://www.edmonds.wednet.edu/programs/move_60_/move_60__calendar',
'https://www.edmonds.wednet.edu/programs/science__technology__engineering___math___s_t_e_m_',
'https://stem.edmonds.wednet.edu/',
'https://www.edmonds.wednet.edu/programs/science__technology__engineering___math___s_t_e_m_/more_s_t_e_m_for_students_and_families',
'https://www.edmonds.wednet.edu/programs/science__technology__engineering___math___s_t_e_m_/more_s_t_e_m_for_students_only',
'https://www.edmonds.wednet.edu/programs/science__technology__engineering___math___s_t_e_m_/s_t_e_m_competitions',
'https://www.edmonds.wednet.edu/programs/science__technology__engineering___math___s_t_e_m_/s_t_e_m_expo_2020',
'https://www.edmonds.wednet.edu/programs/science__technology__engineering___math___s_t_e_m_/s_t_e_m_for_teachers',
'https://www.edmonds.wednet.edu/programs/summer_learning_opportunities',
'https://www.edmonds.wednet.edu/programs/summer_learning_opportunities/high_school_summer_school',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/summer_music_school',
'https://www.edmonds.wednet.edu/programs/summer_learning_opportunities/summer_online_new_credit',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451882',
'https://www.edmonds.wednet.edu/programs/third_grade_swim_lessons',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/elementary_honor_groups',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/elementary_instrumental_music_program',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/music_staff_directory_-_by_school',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/summer_music_school',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/elementary_instrument_rental',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/music_news',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_dept/summer_honor_jazz_band',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/theater_arts',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/theater_arts/theater_arts_staff',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/visual_arts',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/visual_arts/edmonds_arts_festival_foundation_grants',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/visual_arts/edmonds_arts_festival',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/visual_arts/edmonds_arts_festival/volunteer_information',
'https://www.edmonds.wednet.edu/programs/visual___performing_arts___music__drama__art_/music_and_arts_calender',
'https://www.edmonds.wednet.edu/programs/high_school__college__career/vocational_programs',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=306770',
'https://www.edmonds.wednet.edu/students',
'https://www.edmonds.wednet.edu/students/career___college_readiness',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/a_c_t_and_s_a_t_test_dates_and_registration',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/guide_to_college_admissions',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/scholarship_resources',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/undocumented_student_information',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/financial_aid',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/general_college_information_websites',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/college_athletics',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/special_interest_websites',
'https://www.edmonds.wednet.edu/students/career___college_readiness/college_planning/gap_year_program_websites',
'https://www.edmonds.wednet.edu/students/career___college_readiness/naviance_-_career___college_planning',
'https://www.edmonds.wednet.edu/students/career___college_readiness/transcripts__diplomas',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/1_1_f_a_qs',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/student_online_privacy',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/digital_citizenship',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/district_policies_and_procedures',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/district_chromebook_-_change_password',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/district_chromebook_-_offline_access',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/district_chromebook_-_at_home_use',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/class_communication',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/google_drive_export',
'https://www.edmonds.wednet.edu/students/chromebooks_1_1/High%20School%20Summer%20Take%20Home%20Program',
'https://www.edmonds.wednet.edu/students/diversity_resources',
'https://www.edmonds.wednet.edu/students/diversity_resources/african_and_african_american_outreach_resources',
'https://www.edmonds.wednet.edu/students/diversity_resources/latina_outreach__asuntos_y_servicios_para_latinos',
'https://www.edmonds.wednet.edu/students/diversity_resources/indian_education',
'https://www.edmonds.wednet.edu/students/diversity_resources/asian_pacific_american_outreach_resources',
'https://www.edmonds.wednet.edu/students/diversity_resources/international_exchange_students',
'https://www.edmonds.wednet.edu/students/diversity_resources/diversity__equity___outreach_staff/',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/families_in_transition__mckinney_vento_foster_care',
'https://www.edmonds.wednet.edu/students/graduation_requirements',
'https://www.edmonds.wednet.edu/students/graduation_requirements/graduation_pathways',
'https://www.edmonds.wednet.edu/students/graduation_requirements/earning_additional_credits',
'https://wa-edmonds.intouchreceipting.com/',
'https://www.edmonds.wednet.edu/students/online_resources',
'https://www.edmonds.wednet.edu/students/online_resources/elementary_resources',
'https://www.edmonds.wednet.edu/students/online_resources/middle_school_resources',
'https://www.edmonds.wednet.edu/students/online_resources/high_school_resources',
'https://infosysapps.edmonds.wednet.edu/change_password/',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=541513',
'https://www.edmonds.wednet.edu/families',
'https://www.edmonds.wednet.edu/families/attendance',
'https://www.edmonds.wednet.edu/families/attendance/informaci_n_de_asistencia_del_estudiante',
'https://www.edmonds.wednet.edu/families/back-_to-_school_fair',
'https://www.edmonds.wednet.edu/families/back-_to-_school_fair/back-to-_school_fair_-_spanish',
'https://www.edmonds.wednet.edu/families/back-_to-_school_fair/back-to-_school_fair_-_korean',
'https://www.edmonds.wednet.edu/families/back-_to-_school_fair/back-to-_school_fair_vietnamese',
'https://www.edmonds.wednet.edu/families/back-_to-_school_fair/back-to-_school_fair_-_arabic',
'https://www.edmonds.wednet.edu/families/back-_to-_school_fair/back-to-_school_fair_-_amharic',
'https://www.edmonds.wednet.edu/families/calendars_and_family_handbook',
'https://www.edmonds.wednet.edu/families/calendars_and_family_handbook/key_dates_2020-21__2021-22__2022-23',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=306770',
'https://www.edmonds.wednet.edu/families/calendars_and_family_handbook/past_calendars',
'https://www.edmonds.wednet.edu/families/calendars_and_family_handbook/past_calendars/calendars_and_family_handbook_2020-21',
'https://www.edmonds.wednet.edu/families/calendars_and_family_handbook/past_calendars/calendars_and_parent_handbook_2019_2020',
'https://www.edmonds.wednet.edu/families/calendars_and_family_handbook/past_calendars/calendars_and_parent_handbook_2018-2019',
'https://www.edmonds.wednet.edu/families/community_health_programs',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2016_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2014_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2012_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2010_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2008_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2006_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2004_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2002_results',
'https://www.edmonds.wednet.edu/families/community_health_programs/health___fitness_e_x_p_o',
'https://www.edmonds.wednet.edu/programs/third_grade_swim_lessons',
'https://www.edmonds.wednet.edu/families/c_o_v_i_d_health__safety',
'https://datastudio.google.com/u/0/reporting/f282b9ac-54d6-460f-a961-fd8249978119/page/p_3q4xcpamrc',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451936',
'https://www.edmonds.wednet.edu/families/enrollment',
'https://www.edmonds.wednet.edu/families/enrollment/step_1__enrollment_eligibility',
'https://www.edmonds.wednet.edu/families/enrollment/step_2___3__documentation_and_forms',
'https://www.edmonds.wednet.edu/families/enrollment/step_4__online_enrollment',
'https://www.edmonds.wednet.edu/families/enrollment/step_5__finalize',
'https://www.edmonds.wednet.edu/families/enrollment/paper_enrollment',
'https://www.edmonds.wednet.edu/families/enrollment/school_change__transfer',
'https://www.edmonds.wednet.edu/families/enrollment/school_change__transfer/elementary_school_change_information',
'https://www.edmonds.wednet.edu/families/enrollment/school_change__transfer/middle_and_high_school_change_information',
'https://www.edmonds.wednet.edu/families/enrollment/school_change__transfer/transferring_to__from_another_district___choice_tr',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success/families_in_transition__mckinney_vento_foster_care',
'https://www.edmonds.wednet.edu/families/family_support',
'https://www.edmonds.wednet.edu/departments/food___nutrition_services',
'https://www.edmonds.wednet.edu/families/family_support/internet',
'https://sites.google.com/edmonds.wednet.edu/esdresources/home',
'https://www.edmonds.wednet.edu/families/family_support/tech_support___chromebooks',
'https://www.edmonds.wednet.edu/families/family_support/mental_health_resources',
'https://www.edmonds.wednet.edu/families/family_support/mental_health_resources/mental_health_videos',
'https://www.edmonds.wednet.edu/families/family_support/mental_health_resources/mental_health_partners',
'https://www.edmonds.wednet.edu/families/family_support/mental_health_resources/mental_health_community_forum',
'https://www.edmonds.wednet.edu/families/family_support/financial_support',
'https://www.edmonds.wednet.edu/community/before_and_after_school_care',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=451648',
'https://www.edmonds.wednet.edu/cms/one.aspx?portalId=306754&pageId=541513',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452727',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=489249',
'https://www.edmonds.wednet.edu/families/kindergarten',
'https://www.edmonds.wednet.edu/families/kindergarten/jump_start',
'https://www.edmonds.wednet.edu/families/kindergarten/early_entrance',
'https://www.edmonds.wednet.edu/families/kindergarten/early_entrance/early_entrance_details',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452233',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=452293',
'https://www.edmonds.wednet.edu/families/grades___report_cards',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Families/Report%20Cards/Access%20a%20Report%20Card%20Online/Report%20Cards%20are%20now%20being%20posted%20to%20Family%20Access.pdf',
'https://www.edmonds.wednet.edu/departments/student_learning_assessment_curriculum_instruction/elementary_school_k-6/understanding_your_child_s_progress',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=601389',
'https://www.edmonds.wednet.edu/families/skyward_family_access',
'https://www.edmonds.wednet.edu/families/skyward_family_access/skyward_account_access',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=20563686',
'https://www.edmonds.wednet.edu/families/skyward_family_access/reports_cards_in_skyward',
'https://www.edmonds.wednet.edu/families/skyward_family_access/annual_information_update_in_skyward',
'https://www.edmonds.wednet.edu/families/student_health_services_-_school_nurses',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1638595',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1638151',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1339961',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=38189179',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1340221',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1340285',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1340325',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=1340421',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=27138489',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=10325637',
'https://www.edmonds.wednet.edu/families/student_discipline',
'https://www.edmonds.wednet.edu/families/wellness',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=452969',
'https://www.edmonds.wednet.edu/community',
'https://www.edmonds.wednet.edu/community/2022_educational_programs_and_operations_levy',
'https://www.edmonds.wednet.edu/community/2022_educational_programs_and_operations_levy/pro__con_committee',
'https://www.edmonds.wednet.edu/community/2022_educational_programs_and_operations_levy/frequently_asked_questions',
'https://www.edmonds.wednet.edu/community/2022_educational_programs_and_operations_levy/financial_information',
'https://www.edmonds.wednet.edu/community/bonds___levies',
'https://www.edmonds.wednet.edu/community/bonds___levies/2021_capital_levy',
'https://www.edmonds.wednet.edu/community/bonds___levies/2021_capital_levy/frequently_asked_questions_-_levies',
'https://www.edmonds.wednet.edu/community/bonds___levies/2021_capital_levy/financial_information_-_2021_levy',
'https://www.edmonds.wednet.edu/community/bonds___levies/2021_capital_levy/fiscal_responsibility',
'https://www.edmonds.wednet.edu/community/bonds___levies/2021_capital_levy/levy_materials',
'https://www.edmonds.wednet.edu/community/bonds___levies/2020_capital__technology_levy___construction_bond',
'https://www.edmonds.wednet.edu/community/bonds___levies/2020_capital__technology_levy___construction_bond/2020_capital_construction_bond',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Departments/Capital%20Projects/2018%20Enrollment%20Committee%20Report.pdf',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Departments/Capital%20Projects/Final%202020%20Bond%20Committee%20Report%20with%20link%20to%20Enrollment%20Report.pdf',
'https://www.edmonds.wednet.edu/community/bonds___levies/2020_capital__technology_levy___construction_bond/2020_technology__capital_levy',
'https://www.edmonds.wednet.edu/community/bonds___levies/2020_capital__technology_levy___construction_bond/frequently_asked_questions_-_bonds_and_levies',
'https://www.edmonds.wednet.edu/community/bonds___levies/2020_capital__technology_levy___construction_bond/financial_information',
'https://www.edmonds.wednet.edu/community/bonds___levies/2020_capital__technology_levy___construction_bond/2014_capital_construction_bond_status',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/Image/Community/2020%20Levy%20and%20Bond/2020%20Bond%20and%20Levy%20Capital%20Facilities%20Projects%20by%20School%20v22.pdf',
'https://www.edmonds.wednet.edu/cms/One.aspx?portalId=306754&pageId=26646870',
'https://www.edmonds.wednet.edu/community/bonds___levies/2018_replacement_school_programs_and_operations_le',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/About%20Us/News%20&%20Publications/Publications/ESD%20Election%20Newsletter%202015%20for%20online.pdf',
'https://www.edmonds.wednet.edu/community/bonds___levies/2014_school_programs_and_operation_levy_and_capito',
'https://www.edmonds.wednet.edu/community/bonds___levies/2014_school_programs_and_operation_levy_and_capito/capitol_improvements_in_2014_bond',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Community/Your%20Tax%20Dollars/2012%20Replacement%20Technology/12TechCapLevyInfo-sm%20.pdf',
'https://www.edmonds.wednet.edu/community/bonds___levies/2010_school_programs_and_operation_levy',
'https://www.edmonds.wednet.edu/community/bonds___levies/2010_supplemental_school_programs_and_operation_le',
'https://www.edmonds.wednet.edu/community/bonds___levies/2008_technology__capitol_levy',
'https://www.edmonds.wednet.edu/community/bonds___levies/2006_capitol_construction_bond',
'https://www.edmonds.wednet.edu/community/bonds___levies/2006_capitol_construction_bond/list_of_projects_for_elementary_and_k-8_schools',
'https://www.edmonds.wednet.edu/community/bonds___levies/2006_capitol_construction_bond/list_of_projects_for_secondary_schools_and_other_p',
'https://www.edmonds.wednet.edu/community/before_and_after_school_care',
'https://www.edmonds.wednet.edu/community/before_and_after_school_care/right_at_school',
'https://rightatschool.com/pdfs/Edmonds%20Info%20Page.pdf',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/Image/Community/Right%20At%20School/Day_in_the_Life_at_RAS.pdf',
'https://www.edmonds.wednet.edu/community/before_and_after_school_care/right_at_school/frequently_asked_questions',
'https://www.edmonds.wednet.edu/community/community_e_fliers',
'https://www.edmonds.wednet.edu/community/community_health_programs',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_surveys_2018_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2016_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2014_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2012_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2010_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2008_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2006_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2004_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/healthy_youth_surveys/healthy_youth_survey_2002_results',
'https://www.edmonds.wednet.edu/community/community_health_programs/health___fitness_expo',
'https://www.edmonds.wednet.edu/cms/one.aspx?portalid=306754&pageid=452361',
'https://www.edmonds.wednet.edu/programs/third_grade_swim_lessons',
'https://www.edmonds.wednet.edu/community/community_use_of_district_facilities',
'https://www.edmonds.wednet.edu/community/community_use_of_district_facilities',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/About%20Us/School%20Board%20Policies%20&%20Procedures/Section%204000/4260%20Use%20of%20School%20Facilities%20FINAL.pdf',
'https://drive.google.com/file/d/1UZZGkrNHvf_kZGzdm6_X4s1EbRzmn9YR/view?%20Procedures/Section%204000/4260P%20Procedures%20-%20Community%20Use%20of%20School%20Facilities%20FINAL%203-23-18.pdf',
'https://www.edmonds.wednet.edu/community/community_use_of_district_facilities/fee_tables',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Community/Community%20Use%20of%20District%20Facilities/Fee%20Tables/FEE%20TABLE_INDOOR%20FOR%202021-22.pdf',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Community/Community%20Use%20of%20District%20Facilities/Fee%20Tables/Outdoor%20Fee%20Table%20for%202020-21.pdf',
'https://cdn5-ss13.sharpschool.com/UserFiles/Servers/Server_306670/File/Community/Community%20Use%20of%20District%20Facilities/Fee%20Tables/Theater%20Fee%20Table%20for%202020-21.pdf',
'https://www.edmonds.wednet.edu/community/community_use_of_district_facilities/insurance_requirements',
'https://www.edmonds.wednet.edu/community/construction_projects',
'https://www.edmonds.wednet.edu/community/construction_projects/alderwood_middle_school',
'https://www.edmonds.wednet.edu/community/construction_projects/cedar_valley_community_school',
'https://www.edmonds.wednet.edu/community/construction_projects/chase_lake_community_school',
'https://www.edmonds.wednet.edu/community/construction_projects/edmonds_woodway_high_school',
'https://www.edmonds.wednet.edu/community/construction_projects/lynndale_elementary_school',
'https://www.edmonds.wednet.edu/community/construction_projects/lynnwood_elementary_school',
'https://www.edmonds.wednet.edu/community/construction_projects/lynnwood_high_school',
'https://www.edmonds.wednet.edu/community/construction_projects/madrona_k-8_school',
'https://www.edmonds.wednet.edu/community/construction_projects/maintenance_and_transportation_facility',
'https://www.edmonds.wednet.edu/community/construction_projects/maplewood_and_maplewood_center',
'https://www.edmonds.wednet.edu/community/construction_projects/meadowdale_elementary_school',
'https://www.edmonds.wednet.edu/community/construction_projects/meadowdale_high_school',
'https://www.edmonds.wednet.edu/community/construction_projects/meadowdale_middle_school',
'https://www.edmonds.wednet.edu/community/construction_projects/mountlake_terrace_elementary_school',
'https://www.edmonds.wednet.edu/community/construction_projects/oak_heights_elementary_school',
'https://www.edmonds.wednet.edu/community/construction_projects/seaview_elementary_school',
'https://www.edmonds.wednet.edu/community/construction_projects/spruce_elementary_school',
'https://www.edmonds.wednet.edu/community/construction_projects/terrace_park_elementary_school',
'https://www.edmonds.wednet.edu/departments/equity_and_student_success',
'https://www.edmonds.wednet.edu/community/donations_to_schools_and_student_activities',
'https://www.edmonds.wednet.edu/community/equity_alliance_for_achievement__eaach_',
'https://foundationesd.org/',
'https://www.edmonds.wednet.edu/community/hazel_miller_foundation_partnership',
'https://www.edmonds.wednet.edu/community/student_voter_registration_information',
'https://teachersofcolorfoundation.org/',
'https://www.edmonds.wednet.edu/community/transcript___diploma_requests',
'https://www.edmonds.wednet.edu/community/volunteer',
'https://www.edmonds.wednet.edu/staff',
'https://staff.edmonds.wednet.edu/gateway/Login.aspx?ReturnUrl=%2f',
'https://login.frontlineeducation.com/login?signin=b629e461e0cf458d3dcddad61c62f133&productId=ABSMGMT&clientId=ABSMGMT#/login',
'https://www.edmonds.wednet.edu/departments/human_resources__payroll___benefits/employment_home',
'https://mail.google.com/',
'https://edmondsprodev.myschooldata.net/',
'https://helpdesk.edmonds.wednet.edu/helpdesk/WebObjects',
'https://xeponline.wa-k12.net/Account/LogOn',
'https://edmonds-wa.safeschools.com/login',
'https://www2.nwrdc.wa-k12.net/scripts/cgiip.exe/WService=wedmonds71/seplog01.w',
'https://www.edmonds.wednet.edu/cms/one.aspx?pageId=2463740',
	]
	mainfolder = 'edmonds'
	school_name = 'edmonds'
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
