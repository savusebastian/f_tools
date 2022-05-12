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
		'https://www.bsd7.org/our_district/welcome_message',
'https://www.bsd7.org/our_district/2022_election',
'https://www.bsd7.org/our_district/2022_election/voter_information',
'https://www.bsd7.org/our_district/2022_election/contact_information',
'https://www.bsd7.org/our_district/2022_election/trustee_election',
'https://www.bsd7.org/our_district/2022_election/trustee_candidate_voter_information',
'https://www.bsd7.org/our_district/2022_election/levy_requests',
'https://www.bsd7.org/our_district/2022_election/endorsements',
'https://www.bsd7.org/our_district/2022_election/election_information_brochure',
'https://www.bsd7.org/our_district/2022_election/estimated_total_tax_impact',
'https://www.bsd7.org/our_district/2022_election/future_issues',
'https://www.bsd7.org/our_district/2022_election/presentation_schedule',
'https://www.bsd7.org/our_district/board_of_trustees',
'https://www.bsd7.org/our_district/board_of_trustees/board_of_trustees_members',
'https://www.bsd7.org/our_district/board_of_trustees/board_meeting_agendas',
'https://www.bsd7.org/our_district/board_of_trustees/standing_board_committees',
'https://www.bsd7.org/our_district/superintendent',
'https://www.bsd7.org/our_district/bozeman_public_schools_annual_report_2021-2022',
'https://www.bsd7.org/our_district/calendar',
'https://www.bsd7.org/our_district/e_s_s_a_report_card',
'https://www.bsd7.org/our_district/policies',
'https://www.bsd7.org/our_district/long_range_strategic_plan',
'https://www.bsd7.org/our_district/long_range_strategic_plan/long_range_strategic_plan_lrsp_',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2021-2022',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2020-2021',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2018-2019',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2017-2018',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2016-2017',
'https://www.bsd7.org/our_district/long_range_strategic_plan/lrsp_2015-2016',
'https://www.bsd7.org/our_district/long_range_strategic_plan/lrsp_2015-2016/lrsp_2015-16_action_matrix',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2014-2015',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2014-2015/lrsp_action_plan_matrix_2014-2015',
'https://www.bsd7.org/our_district/long_range_strategic_plan/LRSP%202013-2014',
'https://www.bsd7.org/our_district/long_range_strategic_plan/LRSP%202013-2014/l_r_s_p_action_plan_matrix_2013-2014',
'https://www.bsd7.org/our_district/long_range_strategic_plan/LRSP%202013-2014/l_r_s_p_balanced_score_card/',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_2012-2013_menu',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_action_plan_matrix_2012-2013',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_balanced_score_card/',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_implementation_framework_2012-2013',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_implementation_framework_2012-2013/long_range_strategic_plan__lrsp_',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_implementation_framework_2012-2013/consensus_process',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_implementation_framework_2012-2013/common_core_state_standards___c_c_s_s_',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_implementation_framework_2012-2013/montana_accreditation_standards',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_implementation_framework_2012-2013_update',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2012-2013/l_r_s_p_implementation_framework_2012-2013_update',
'https://www.bsd7.org/our_district/long_range_strategic_plan/l_r_s_p_2011-2012',
	]
	mainfolder = 'compton'
	school_name = 'compton'
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
