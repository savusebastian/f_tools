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

		if web_soup.find(class_='ptl_page').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='ptl_page').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='ptl_page').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='ptl_page').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='ptl_page').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='ptl_page').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='ptl_page') != None and web_soup.find(class_='ptl_page') != '':
			col1 = web_soup.find(class_='ptl_page')
			col1 = get_column(col1)
			print(1)
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
		'https://www.ceres.k12.ca.us/Information/superintendent',
		'https://www.ceres.k12.ca.us/Information/superintendent/Communications',
		'https://www.ceres.k12.ca.us/Information/superintendent/Communications/employee_spotlight',
		'https://www.ceres.k12.ca.us/Information/superintendent/Communications/employee_spotlight/c_u_s_d_employees_of_the_year',
		'https://www.ceres.k12.ca.us/Information/superintendent/Communications/employee_spotlight/letters_from_students',
		'https://www.ceres.k12.ca.us/Information',
		'https://www.ceres.k12.ca.us/Information/superintendent/Communications/employee_spotlight/c_u_s_d_spotlight',
		'https://www.ceres.k12.ca.us/Information/district_contacts',
		'https://www.ceres.k12.ca.us/Information/strategic_plan',
		'https://www.ceres.k12.ca.us/Information/technology_use_policy',
		'https://www.ceres.k12.ca.us/Information/local_education_agency_plan',
		'https://www.ceres.k12.ca.us/Information/staff_',
		'https://www.ceres.k12.ca.us/Information/staff_/teachers_resources',
		'https://www.ceres.k12.ca.us/Information/staff_/teachers_resources/a_e_s_o_p_resources',
		'https://www.ceres.k12.ca.us/Information/staff_/teachers_resources/substitute_teacher',
		'https://www.ceres.k12.ca.us/Information/staff_/teachers_resources/m_e_a_s_u_r_e_s',
		'https://www.ceres.k12.ca.us/Information/staff_/teachers_resources/pacing_guides',
		'https://www.ceres.k12.ca.us/Information/staff_/teachers_resources/standard_finder',
		'https://www.ceres.k12.ca.us/Information/staff_/staff_resources/staff_email',
		'https://www.ceres.k12.ca.us/Information/staff_/staff_directory',
		'https://www.ceres.k12.ca.us/Information/students',
		'https://www.ceres.k12.ca.us/Information/students/student_resources',
		'https://www.ceres.k12.ca.us/Information/parents',
		'https://www.ceres.k12.ca.us/Information/parents/school_choice_and_supplemental_educational_service',
		'https://www.ceres.k12.ca.us/Information/parents/dental_check-ups_required_for_your_child',
		'https://www.ceres.k12.ca.us/Information/parents/after_school_program_information_and_more___/educational_options',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/infinite_campus_portal',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/transportation',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/parent_rights',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/child_welfare___attendance',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/laws_regarding_school_attendance',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/elementary_schools_boundary_map',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/a_s_e_s_-_after_school_info',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/s_e_l_p_a_forms',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/district_contacts',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/educational_options',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/project_y_e_s',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/ceres_adult_school',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/504_information',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/ceres_healthy_start',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/student_support_services',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/gate',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/report_to_the_community',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/s_a_r_c_reports',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/c_a_healthy_kids_survey_results',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/photo_gallery',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/c_a_h_s_e_e_intensive_instruction_services_student_eligibility_form',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/williams_complaint_form',
		'https://www.ceres.k12.ca.us/Information/parents/c_u_s_d_photo_opt_out',
		'https://www.ceres.k12.ca.us/Information/community/all_employment_applications_now_paperless_',
		'https://www.ceres.k12.ca.us/Information/community/',
		'https://www.ceres.k12.ca.us/Information/school_accountability_report_card_reports',
		'https://www.ceres.k12.ca.us/Information/local_control_accountability_plan',
		'https://www.ceres.k12.ca.us/Information/ceres_days_gone_by',
		'https://www.ceres.k12.ca.us/Information/williams_complaint_form',
		'https://www.ceres.k12.ca.us/Information/reopening___safety_plan',
		'https://www.ceres.k12.ca.us/Information/reopening___safety_plan/distance_learning',
		'https://www.ceres.k12.ca.us/Information/reopening___safety_plan/prior_updates',
		'https://www.ceres.k12.ca.us/Information/reopening___safety_plan/c_o_v_i_d-19_dashboard',
		'https://www.ceres.k12.ca.us/Information/every_student_succeeds_act_comprehensive_support',
		'https://www.ceres.k12.ca.us/Information/StudentCalendar21-22',
		'https://www.ceres.k12.ca.us/Information/title_i_i_i_plan',
		'https://www.ceres.k12.ca.us/Information/title_i_i_i_plan/2021-22_title_i_i_i_plan',
		'https://www.ceres.k12.ca.us/Information/l_c_a_p_federal_addendum',
		'https://www.ceres.k12.ca.us/educational_services',
		'https://www.ceres.k12.ca.us/educational_services/professional_development',
		'https://www.ceres.k12.ca.us/educational_services/professional_development/contacts',
		'https://www.ceres.k12.ca.us/educational_services/projects___assessments',
		'https://www.ceres.k12.ca.us/educational_services/projects___assessments/c_u_s_d_state___benchmark_testing_dates',
		'https://www.ceres.k12.ca.us/educational_services/projects___assessments/elementary_music',
		'https://www.ceres.k12.ca.us/educational_services/projects___assessments/promotion___retention',
		'https://www.ceres.k12.ca.us/educational_services/projects___assessments/categorical',
		'https://www.ceres.k12.ca.us/educational_services/projects___assessments/elementary_p_e',
		'https://www.ceres.k12.ca.us/educational_services/curriculum___instruction/assembly_bill_104',
		'https://www.ceres.k12.ca.us/educational_services/curriculum___instruction/adopted_curriculum',
		'https://www.ceres.k12.ca.us/educational_services/curriculum___instruction',
		'https://www.ceres.k12.ca.us/educational_services/english_learner_resources',
		'https://www.ceres.k12.ca.us/educational_services/instructional_coaches',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness_night',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness/military',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness/applications',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness/letters_of_recommendation',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness/a-_g_requirements',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness/s_a_t_preparation_information',
		'https://www.ceres.k12.ca.us/educational_services/college_awareness/testing_fee_waivers',
		'https://www.ceres.k12.ca.us/educational_services/educational_technology',
		'https://www.ceres.k12.ca.us/educational_services/ceres_induction_program',
		'https://www.ceres.k12.ca.us/student_support',
		'https://www.ceres.k12.ca.us/student_support/educational_options',
		'https://www.ceres.k12.ca.us/student_support/educational_options/elementary_summer_school_information___k-6_',
		'https://www.ceres.k12.ca.us/student_support/educational_options/after_school_programs_summary_information',
		'https://www.ceres.k12.ca.us/student_support/educational_options/after_school_programs_summary_information/after_school_program_calendars',
		'https://www.ceres.k12.ca.us/student_support/educational_options/after_school_programs_summary_information/academic_intervention_program___a_i_p__-_elementar',
		'https://www.ceres.k12.ca.us/student_support/educational_options/after_school_programs_summary_information/academic_intervention_program___a_i_p__-_junior_hi',
		'https://www.ceres.k12.ca.us/student_support/educational_options/after_school_programs_summary_information/academic_extended_day___a_e_d__high_school',
		'https://www.ceres.k12.ca.us/student_support/educational_options/creative_learning_children_s_center',
		'https://www.ceres.k12.ca.us/student_support/state_preschool',
		'https://www.ceres.k12.ca.us/student_support/project_y_e_s',
		'https://www.ceres.k12.ca.us/student_support/career_technical_education___c_t_e_',
		'https://www.ceres.k12.ca.us/student_support/college___career_resources',
		'https://www.ceres.k12.ca.us/student_support/grants',
		'https://www.ceres.k12.ca.us/student_support/special_education',
		'https://www.ceres.k12.ca.us/student_support/special_education/about_us',
		'https://www.ceres.k12.ca.us/student_support/special_education/student_study_team___s_s_t_',
		'https://www.ceres.k12.ca.us/student_support/special_education/special_education_services',
		'https://www.ceres.k12.ca.us/student_support/special_education/s_e_l_p_a',
		'https://www.ceres.k12.ca.us/student_support/special_education/frequently_asked_questions_-_parent',
		'https://www.ceres.k12.ca.us/student_support/special_education/frequently_asked_questions_-_teacher',
		'https://www.ceres.k12.ca.us/student_support/special_education/parent_s_role',
		'https://www.ceres.k12.ca.us/student_support/special_education/resources',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/child_abuse',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/child_abuse/contacts',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/school_attendance_review_board',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/california_healthy_kids_survey',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/california_healthy_kids_survey/about_us',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/resources_for_tobacco_cessation__drug_and_alcohol_',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/c_w_a_referral_page',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/student_and_parent_information',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/transfer_options',
		'https://www.ceres.k12.ca.us/student_support/child_welfare___attendance/section_504',
		'https://www.ceres.k12.ca.us/student_support/specialized_programs',
		'https://www.ceres.k12.ca.us/student_support/student_services',
		'https://www.ceres.k12.ca.us/student_support/student_services/elementary_p_e',
		'https://www.ceres.k12.ca.us/student_support/student_services/ceres_healthy_start_program',
		'https://www.ceres.k12.ca.us/student_support/student_services/ceres_healthy_start_program/contacts',
		'https://www.ceres.k12.ca.us/student_support/student_services/ceres_healthy_start_program/foster_youth',
		'https://www.ceres.k12.ca.us/student_support/student_services/school_attendance_review_board',
		'https://www.ceres.k12.ca.us/student_support/student_services/important_information_from_your_school_nurses',
		'https://www.ceres.k12.ca.us/student_support/student_services/s_s_s_administrative_resources',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health/staff_resources',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health/parent_resources',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health/student_resources',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health/staff_resources/student_support_staff_resources',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health/staff_resources/teacher_resources',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health/newsletter',
		'https://www.ceres.k12.ca.us/student_support/student_services/mental_health/community_resources',
		'https://www.ceres.k12.ca.us/student_support/student_services/immunization_information',
		'https://www.ceres.k12.ca.us/business_services',
		'https://www.ceres.k12.ca.us/business_services/information_technology',
		'https://www.ceres.k12.ca.us/business_services/information_technology/contact_list',
		'https://www.ceres.k12.ca.us/business_services/information_technology/welcome_back_f_a_q',
		'https://www.ceres.k12.ca.us/business_services/information_technology/labels',
		'https://www.ceres.k12.ca.us/business_services/information_technology/data_resources_and_staff_documents',
		'https://www.ceres.k12.ca.us/business_services/information_technology/internet_access_support',
		'https://www.ceres.k12.ca.us/business_services/information_technology/internet_access_support/district_provided_hotspots',
		'https://www.ceres.k12.ca.us/business_services/information_technology/cybersecurity_resources',
		'https://www.ceres.k12.ca.us/business_services/information_technology/cybersecurity_resources/cybersecurity_awareness_month_-_week_1',
		'https://www.ceres.k12.ca.us/business_services/information_technology/cybersecurity_resources/cybersecurity_awareness_month_-_week_2',
		'https://www.ceres.k12.ca.us/business_services/information_technology/cybersecurity_resources/cybersecurity_awareness_month_-_week_3',
		'https://www.ceres.k12.ca.us/business_services/information_technology/cybersecurity_resources/cybersecurity_awareness_month_-_week_4',
		'https://www.ceres.k12.ca.us/business_services/information_technology/internet_access_support/emergency_broadband_benefit',
		'https://www.ceres.k12.ca.us/business_services/Transportation/field_trips_and_student_activities',
		'https://www.ceres.k12.ca.us/business_services/Transportation/publications',
		'https://www.ceres.k12.ca.us/business_services/Transportation/bus_routes',
		'https://www.ceres.k12.ca.us/business_services/Transportation/contacts',
		'https://www.ceres.k12.ca.us/business_services/maintenance',
		'https://www.ceres.k12.ca.us/business_services/fiscal_services',
		'https://www.ceres.k12.ca.us/business_services/fiscal_services/Accounting',
		'https://www.ceres.k12.ca.us/business_services/fiscal_services/Payroll_and_Benefits',
		'https://www.ceres.k12.ca.us/business_services/fiscal_services/Payroll_and_Benefits/contact_the_payroll_and_benefits_department',
		'https://www.ceres.k12.ca.us/business_services/fiscal_services/Warehouse',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/child_nutrition',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/enrollment__attendance__staffing_and_projections',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/facility_planning_and_facility_use',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/field_trips_and_student_activities',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/field_trips_and_student_activities/field_trips',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/field_trips_and_student_activities/a_s_b_information',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/field_trips_and_student_activities/student_activities',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/furniture_and_equipment',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/information_technology',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/maintenance__grounds_and_custodial_services',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/risk_management',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/transportation',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/williams_site_visits',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/energy_management',
		'https://www.ceres.k12.ca.us/business_services/business_administrator_resources/public_works_projects',
		'https://www.ceres.k12.ca.us/business_services/business_admin__resources',
		'https://www.ceres.k12.ca.us/business_services/print___copy_services',
		'https://www.ceres.k12.ca.us/business_services/print___copy_services/p_c_s_customer_feedback',
		'https://www.ceres.k12.ca.us/business_services/print___copy_services/basic_how_to_place_an_order',
		'https://www.ceres.k12.ca.us/business_services/print___copy_services/acrobat_dc_extract',
		'https://www.ceres.k12.ca.us/business_services/print___copy_services/split_pdf',
		'https://www.ceres.k12.ca.us/business_services/child_nutrition',
		'https://www.ceres.k12.ca.us/personnel',
		'https://www.ceres.k12.ca.us/personnel/salary_schedules',
		'https://www.ceres.k12.ca.us/personnel/volunteer_assistant_program',
		'https://www.ceres.k12.ca.us/personnel/personnel_administrative_resources',
		'https://www.ceres.k12.ca.us/personnel/e_d_j_o_i_n_applicant_tracking',
		'https://www.ceres.k12.ca.us/personnel/annual_employee_notification',
		'https://www.ceres.k12.ca.us/personnel/EmploymentOpportunities',
		'https://www.ceres.k12.ca.us/personnel/staff_telephone_directory',
		'https://www.ceres.k12.ca.us/schools',
		'https://www.ceres.k12.ca.us/schools/adkison_elementary',
		'https://www.ceres.k12.ca.us/schools/carroll_fowler_elementary',
		'https://www.ceres.k12.ca.us/schools/caswell_elementary',
		'https://www.ceres.k12.ca.us/schools/don_pedro_elementary',
		'https://www.ceres.k12.ca.us/schools/hidahl_elementary',
		'https://www.ceres.k12.ca.us/schools/la_rosa_elementary',
		'https://www.ceres.k12.ca.us/schools/lucas_elementary_dual_language_academy',
		'https://www.ceres.k12.ca.us/schools/sam_vaughn_elementary',
		'https://www.ceres.k12.ca.us/schools/sinclear_elementary',
		'https://www.ceres.k12.ca.us/schools/virginia_parks_elementary',
		'https://www.ceres.k12.ca.us/schools/walter_white_elementary',
		'https://www.ceres.k12.ca.us/schools/westport_elementary',
		'https://www.ceres.k12.ca.us/schools/whitmore_charter_school',
		'https://www.ceres.k12.ca.us/schools/blaker-_kinser_junior_high',
		'https://www.ceres.k12.ca.us/schools/cesar_chavez_junior_high',
		'https://www.ceres.k12.ca.us/schools/mae_hensley_junior_high',
		'https://www.ceres.k12.ca.us/schools/argus_high_school',
		'https://www.ceres.k12.ca.us/schools/central_valley_high_school',
		'https://www.ceres.k12.ca.us/schools/ceres_high_school',
		'https://www.ceres.k12.ca.us/schools/ceres_adult_school',
		'https://www.ceres.k12.ca.us/schools/patricia_kay_beaver_leadership_magnet',
		'https://www.ceres.k12.ca.us/schools/preschool',
		'https://www.ceres.k12.ca.us/schools/independent_study',
		'https://www.ceres.k12.ca.us/school_flag_program',
		'https://www.ceres.k12.ca.us/board_of_trustees',
		'https://www.ceres.k12.ca.us/air_quality__real-_time_air_advisory_network',
		'https://www.ceres.k12.ca.us/title_i_x',
		'https://www.ceres.k12.ca.us/ParentSquare',
		'https://www.ceres.k12.ca.us/ParentSquare/employee_spotlight',
		'https://www.ceres.k12.ca.us/Information/superintendent/Communications/employee_spotlight/c_u_s_d_employees_of_the_year',
		'https://www.ceres.k12.ca.us/ParentSquare/parent_square_f_a_q',
		'https://www.ceres.k12.ca.us/news',
		'https://www.ceres.k12.ca.us/Information/parents/parent_resources/curriculum___instruction',
		'https://www.ceres.k12.ca.us/Information/parents/school_enrollment',
		'https://www.ceres.k12.ca.us/business_services/Transportation',
		'https://www.ceres.k12.ca.us/Information/about_us',
	]
	mainfolder = 'ceresk12'
	school_name = 'ceresk12_district'
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
