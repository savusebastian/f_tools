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

				if src[0] != '/' and src[:4] != 'http':
					image['src'] = f'/{src}'
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
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/80.0'}
		web_link = requests.get(web_page, headers=headers, timeout=5).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(class_='pageContent').find_all('form') != []:
			form = 'form'

		if web_soup.find(class_='pageContent').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(class_='pageContent').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(class_='pageContent').find_all(id='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(class_='pageContent').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(class_='pageContent').find_all(id='news-list') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(class_='pageContent') != None and web_soup.find(class_='pageContent') != '':
			col1 = web_soup.find(class_='pageContent')
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
		'https://skhs.skschools.org/our_school',
		'https://skhs.skschools.org/our_school/tip_line',
		'https://skhs.skschools.org/our_school/administration',
		'https://skhs.skschools.org/our_school/depts',
		'https://skhs.skschools.org/our_school/depts/pe',
		'https://skhs.skschools.org/our_school/depts/pe/grading',
		'https://skhs.skschools.org/our_school/depts/pe/fitnessplan',
		'https://skhs.skschools.org/our_school/depts/pe/focused_fitness',
		'https://skhs.skschools.org/our_school/depts/pe/five_for_life',
		'https://skhs.skschools.org/our_school/depts/pe/cba_study_guide',
		'https://skhs.skschools.org/our_school/depts/pe/district_p_e_curriculum',
		'https://skhs.skschools.org/our_school/meet_the_office_staff',
		'https://skhs.skschools.org/our_school/bell_schedules',
		'https://skhs.skschools.org/our_school/staff_directory',
		'https://skhs.skschools.org/our_school/attendance',
		'https://skhs.skschools.org/our_school/inclement_weather',
		'https://skhs.skschools.org/our_school/library',
		'https://skhs.skschools.org/our_school/new_to_our_school',
		'https://skhs.skschools.org/our_school/school_report',
		'https://skhs.skschools.org/our_school/skhs_fight_song',
		'https://skhs.skschools.org/our_school/a_s_b_fund_balance_link',
		'https://skhs.skschools.org/our_school/sktv',
		'https://skhs.skschools.org/our_school/sktv/livestream',
		'https://skhs.skschools.org/our_school/sktv/schedule',
		'https://skhs.skschools.org/our_school/sktv/canned_film_festival',
		'https://skhs.skschools.org/our_school/sktv/awards',
		'https://skhs.skschools.org/our_school/sktv/a_day_in_video_production',
		'https://skhs.skschools.org/our_school/sktv/graduation_d_v_ds',
		'https://skhs.skschools.org/students',
		'https://skhs.skschools.org/students/Alumni',
		'https://skhs.skschools.org/students/summer_assignments',
		'https://skhs.skschools.org/students/asb_office',
		'https://skhs.skschools.org/students/asb_office/a_s_b_student_council',
		'https://skhs.skschools.org/students/BYUHighSchoolSuite',
		'https://skhs.skschools.org/students/career_center',
		'https://skhs.skschools.org/students/career_center/career_pathways',
		'https://skhs.skschools.org/students/career_center/career_pathways/arts___communication',
		'https://skhs.skschools.org/students/career_center/career_pathways/engineering_and_technology',
		'https://skhs.skschools.org/students/career_center/career_pathways/health___human_services',
		'https://skhs.skschools.org/students/career_center/career_pathways/business_and_marketing',
		'https://skhs.skschools.org/students/career_center/career_pathways/science_and_natural_resources',
		'https://skhs.skschools.org/students/career_center/scholarships',
		'https://skhs.skschools.org/students/career_center/college_admissions_info_',
		'https://skhs.skschools.org/students/career_center/paying_for_college',
		'https://skhs.skschools.org/students/career_center/writing_the_college_essay',
		'https://skhs.skschools.org/students/career_center/military__apprenticeships__trade_schools',
		'https://skhs.skschools.org/students/clubs',
		'https://skhs.skschools.org/students/on_track_course_catalog',
		'https://skhs.skschools.org/students/daily_bulletin',
		'https://skhs.skschools.org/students/d_e_c_a',
		'https://skhs.skschools.org/students/GoogleClassroom',
		'https://skhs.skschools.org/students/guidance_office',
		'https://skhs.skschools.org/students/guidance_office/schedule_change_request',
		'https://skhs.skschools.org/students/guidance_office/meet_the_guidance_office_staff',
		'https://skhs.skschools.org/students/guidance_office/meet_the_counselors',
		'https://skhs.skschools.org/students/guidance_office/enrollment',
		'https://skhs.skschools.org/students/guidance_office/change_student_information',
		'https://skhs.skschools.org/students/guidance_office/withdrawing_a_student',
		'https://skhs.skschools.org/students/guidance_office/scholarships',
		'https://skhs.skschools.org/students/guidance_office/class_of_2021',
		'https://skhs.skschools.org/students/guidance_office/class_of_2024',
		'https://skhs.skschools.org/students/guidance_office/class_of_2022',
		'https://skhs.skschools.org/students/guidance_office/class_of_2023',
		'https://skhs.skschools.org/students/high_school___beyond_plan___xello_',
		'https://skhs.skschools.org/students/honor_roll___principal_s_list___class_rank',
		'https://skhs.skschools.org/athletics',
		'https://skhs.skschools.org/athletics/spring',
		'https://skhs.skschools.org/athletics/spring/track___field',
		'https://skhs.skschools.org/athletics/spring/girls_water_polo_',
		'https://skhs.skschools.org/athletics/spring/boys_lacrosse',
		'https://skhs.skschools.org/athletics/spring/girls_lacrosse',
		'https://skhs.skschools.org/athletics/s_k_h_s_cheer_team',
		'https://skhs.skschools.org/athletics/s_k_h_s_cheer_team/s_k_h_s_cheer_photo_album',
		'https://skhs.skschools.org/athletics/s_k_h_s_cheer_team/SKHS_cheer_website',
		'https://skhs.skschools.org/athletics/s_k_h_s_cheer_team/skhs_cheer_facebook',
		'https://skhs.skschools.org/athletics/skhs_dance_team',
		'https://skhs.skschools.org/athletics/skhs_crew',
		'https://skhs.skschools.org/athletics/skhs_equestrian_team',
		'https://skhs.skschools.org/athletics/turn_out_info',
		'https://skhs.skschools.org/athletics/s_k_community_pool',
		'https://skhs.skschools.org/athletics/s_k_community_pool/general_swim_information',
		'https://skhs.skschools.org/athletics/s_k_community_pool/2017_fall_swimming_lessons',
		'https://skhs.skschools.org/athletics/s_k_community_pool/pool_rental_information',
		'https://skhs.skschools.org/athletics/directions_to_games',
		'https://skhs.skschools.org/athletics/athletic_medicine',
		'https://skhs.skschools.org/athletics/athletic_medicine/athletic_medicine_team',
		'https://skhs.skschools.org/athletics/athletic_medicine/athletic_medicine_team/team_physician',
		'https://skhs.skschools.org/athletics/athletic_medicine/athletic_medicine_team/certified__licensed_athletic_trainers',
		'https://skhs.skschools.org/athletics/athletic_medicine/injury_forms',
		'https://skhs.skschools.org/athletics/athletic_medicine/injury_forms/parent_and_athlete_letter',
		'https://skhs.skschools.org/athletics/athletic_medicine/injury_forms/physician_referral_form',
		'https://skhs.skschools.org/athletics/athletic_medicine/injury_forms/concussion_referral_form',
		'https://skhs.skschools.org/athletics/athletic_medicine/injury_forms/concussion_information',
		'https://skhs.skschools.org/athletics/athletic_medicine/athletic_medicine_facility',
		'https://skhs.skschools.org/athletics/athletic_medicine/athletic_medicine_club',
		'https://skhs.skschools.org/athletics/athletic_medicine/visiting_teams',
		'https://skhs.skschools.org/athletics/weight_room',
		'https://skhs.skschools.org/athletics/summer_camps',
		'https://skhs.skschools.org/athletics/link_to_web_store',
		'https://skhs.skschools.org/athletics/college_bound',
		'https://skhs.skschools.org/athletics/college_bound/college_signing_days',
		'https://skhs.skschools.org/athletics/faqs',
		'https://skhs.skschools.org/athletics/questions___answers',
		'https://skhs.skschools.org/athletics/skhs_athletics',
		'https://skhs.skschools.org/athletics/sports_calendars',
		'https://skhs.skschools.org/athletics/kitsap_bank_stadium_reservations',
		'https://skhs.skschools.org/athletics/athlete_handbook',
		'https://skhs.skschools.org/athletics/fall',
		'https://skhs.skschools.org/athletics/fall/soccer_girls',
		'https://skhs.skschools.org/athletics/fall/boys_tennis',
		'https://skhs.skschools.org/athletics/fall/football',
		'https://skhs.skschools.org/athletics/fall/girls_volleyball_',
		'https://skhs.skschools.org/athletics/fall/girls_swim',
		'https://skhs.skschools.org/athletics/fall/boys_golf_',
		'https://skhs.skschools.org/athletics/fall/boys_water_polo',
		'https://skhs.skschools.org/athletics/fall/_girls_golf_-_wip',
		'https://skhs.skschools.org/athletics/fall/Copy%20X%20Country',
		'https://skhs.skschools.org/athletics/fall/soccer_girls',
		'https://skhs.skschools.org/athletics/fall/boys_tennis',
		'https://skhs.skschools.org/athletics/fall/football',
		'https://skhs.skschools.org/athletics/fall/girls_volleyball_',
		'https://skhs.skschools.org/athletics/fall/girls_swim',
		'https://skhs.skschools.org/athletics/fall/boys_golf_',
		'https://skhs.skschools.org/athletics/fall/boys_water_polo',
		'https://skhs.skschools.org/athletics/winter',
		'https://skhs.skschools.org/athletics/winter/boys_basketball',
		'https://skhs.skschools.org/athletics/winter/girls_basketball',
		'https://skhs.skschools.org/athletics/winter/bowling_',
		'https://skhs.skschools.org/athletics/winter/boys_swim_',
		'https://skhs.skschools.org/athletics/winter/wrestling',
		'https://skhs.skschools.org/athletics/winter/boys_basketball',
		'https://skhs.skschools.org/athletics/winter/girls_basketball',
		'https://skhs.skschools.org/athletics/spring/baseball_',
		'https://skhs.skschools.org/athletics/spring/girls_fastpitch',
		'https://skhs.skschools.org/athletics/spring/boys_soccer',
		'https://skhs.skschools.org/athletics/spring/girls_tennis',
		'https://skhs.skschools.org/athletics/spring/baseball_',
		'https://skhs.skschools.org/athletics/college_bound',
		'https://skhs.skschools.org/athletics/college_bound/college_signing_days',
		'https://skhs.skschools.org/athletics/faqs',
		'https://skhs.skschools.org/teachers',
		'https://skhs.skschools.org/teachers/field_trips',
		'https://skhs.skschools.org/teachers/coach__advisor__booster_resource_site',
		'https://skhs.skschools.org/teachers/field_trips',
		'https://skhs.skschools.org/teachers/coach__advisor__booster_resource_site',
	]
	# mainfolder = all_sites[0].split('.')[1]
	mainfolder = 'south_kitsap'
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
		school_name = 'south_kitsap'

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
