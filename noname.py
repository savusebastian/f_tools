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
		web_link = requests.get(web_page, headers=headers, timeout=20, verify=False).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(id='page-content').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='page-content').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='page-content').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='page-content').find_all(class_='calendargrid') != []:
			calendar = 'calendar'

		if web_soup.find(id='page-content').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='page-content').find_all(class_='news-info-cont') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='page-content') != None and web_soup.find(id='page-content') != '':
			col1 = web_soup.find(id='page-content')
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
		'https://www.newbritainct.gov/howdoi/default.htm',
		'https://www.newbritainct.gov/howdoi/apply/default.htm',
		'https://permits.newbritainpolice.org',
		'https://www.newbritainct.gov/services/civil/employment/default.htm',
		'https://www.newbritainct.gov/howdoi/apply/food_truck_license.htm',
		'http://www.nbpl.info/librarycard.html',
		'https://portal.viewpermit.com/preloginviews/loginpage.aspx?enc=Tbiq5Hp49GVlSaaosHC2Ow==',
		'https://www.newbritainct.gov/howdoi/find/default.htm',
		'https://www.newbritainct.gov/services/purchasing/bids.htm',
		'https://www.newbritainct.gov/services/finance/budget_management.htm',
		'https://www.newbritainct.gov/howdoi/find/history.htm',
		'http://www.stanleygolf.com/',
		'http://newbritainct.gov/services/public_works/programs_n_services/spring_collection.htm',
		'http://newbritainct.gov/services/public_works/programs_n_services/fall_collection.htm',
		'http://www.nbpl.info/main.html',
		'https://www.newbritainct.gov/howdoi/find/parking.htm',
		'https://www.newbritainct.gov/howdoi/find/parks_open_spaces_n_trails.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/pavement_management_program.htm',
		'https://www.newbritainct.gov/services/public_works/default.htm',
		'https://nbparksnrec.org/wbwsc/webtrac.wsc/wbsplash.html?wbp=1',
		'https://www.newbritainct.gov/howdoi/learn/default.htm',
		'https://www.newbritainct.gov/services/health/emergency_preparedness.htm',
		'https://www.newbritainct.gov/howdoi/pay/default.htm',
		'https://www.newbritainct.gov/services/parking_ticket/payments.htm',
		'https://www.newbritainct.gov/services/tax_collector/online_tax_payments.htm',
		'https://www.newbritainct.gov/services/tax_collector/online_utility_payments.htm',
		'https://www.newbritainct.gov/howdoi/lease/default.htm',
		'https://www.newbritainct.gov/howdoi/lease/beachpark.htm',
		'https://www.newbritainct.gov/howdoi/lease/facility.htm',
		'https://www.newbritainct.gov/howdoi/lease/meetroom.htm',
		'https://www.newbritainct.gov/howdoi/report/default.htm',
		'http://viewnforce.cloudapp.net/LoginPage.aspx?tid=17',
		'https://www.newbritainct.gov/new_britain/seeclickfix.htm',
		'https://www.newbritainct.gov/howdoi/view/default.htm',
		'https://www.newbritainct.gov/gov/boards/default.htm',
		'https://www.newbritainct.gov/howdoi/view/city_charter.htm',
		'https://www.newbritainct.gov/gov/common_council/members.htm',
		'https://www.newbritainct.gov/howdoi/view/faqs.htm',
		'https://www.municode.com/library/CT/New Britain',
		'http://newbritain.mapxpress.net/',
		'http://gis.vgsi.com/newbritainct/',
		'https://nbparksnrec.org/wbwsc/webtrac.wsc/wbsplash.html?wbp=1',
		'https://www.newbritainct.gov/howdoi/view/permit_status.htm',
		'https://www.newbritainct.gov/howdoi/view/regulations.htm',
		'https://www.newbritainct.gov/gov/common_council/agenda_minutes_live_stream_n_video.htm',
		'https://www.newbritainct.gov/gov/default.htm',
		'https://www.newbritainct.gov/gov/mayors_office/default.htm',
		'https://www.newbritainct.gov/gov/mayors_office/stewart.htm',
		'https://www.newbritainct.gov/gov/mayors_office/building_hope/default.htm',
		'https://www.newbritainct.gov/gov/mayors_office/building_hope/2019_annual_plan_.htm',
		'https://www.newbritainct.gov/gov/mayors_office/building_hope/2018_annual_plan_.htm',
		'https://www.newbritainct.gov/gov/mayors_office/mayors_budget/default.htm',
		'https://www.newbritainct.gov/gov/mayors_office/smart_city/default.htm',
		'https://www.newbritainct.gov/civicax/filebank/blobdload.aspx?BlobID=26176',
		'https://www.newbritainct.gov/gov/mayors_office/smart_city/energy_n_innovation_2019.htm',
		'https://www.newbritainct.gov/gov/mayors_office/smart_city/energyinnovation.htm',
		'https://www.newbritainct.gov/gov/mayors_office/plan_to_end_homlessness/default.htm',
		'https://www.newbritainct.gov/gov/common_council/default.htm',
		'https://www.newbritainct.gov/gov/common_council/members.htm',
		'https://www.newbritainct.gov/gov/common_council/meeting_calendar.htm',
		'https://www.newbritainct.gov/gov/common_council/subcommittees/default.htm',
		'https://www.newbritainct.gov/gov/common_council/subcommittees/administration_finance_n_law.htm',
		'https://www.newbritainct.gov/gov/common_council/subcommittees/planning_zoning.htm',
		'https://www.newbritainct.gov/gov/common_council/subcommittees/consolidated.htm',
		'https://www.newbritainct.gov/gov/common_council/agenda_minutes_live_stream_n_video.htm',
		'https://www.newbritainct.gov/gov/common_council/audio_recording.htm',
		'https://www.newbritainct.gov/gov/boards/default.htm',
		'https://www.newbritainct.gov/gov/boards/animal_welfare.htm',
		'https://www.newbritainct.gov/gov/boards/board_of_education.htm',
		'https://www.newbritainct.gov/gov/boards/board_of_finance.htm',
		'https://www.newbritainct.gov/gov/boards/board_of_health.htm',
		'https://www.newbritainct.gov/gov/boards/board_of_water_commissioners.htm',
		'https://www.newbritainct.gov/gov/boards/city_plan_commission.htm',
		'https://www.newbritainct.gov/services/community/senior/members.htm',
		'https://www.newbritainct.gov/gov/boards/commission_on_community_n_neighborhood_development.htm',
		'https://www.newbritainct.gov/gov/boards/commission_on_the_arts.htm',
		'https://www.newbritainct.gov/gov/boards/commission_on_persons_with_disabilities.htm',
		'https://www.newbritainct.gov/gov/boards/commission_on_youth_and_family_services.htm',
		'https://www.newbritainct.gov/gov/boards/conservation_commission.htm',
		'https://www.newbritainct.gov/gov/boards/fairview_cemetery.htm',
		'https://www.newbritainct.gov/gov/boards/fire_commission/default.htm',
		'https://www.newbritainct.gov/gov/boards/historic_preservation.htm',
		'https://www.newbritainct.gov/services/recreation/board_members.htm',
		'https://www.newbritainct.gov/gov/boards/police_commission/default.htm',
		'https://www.newbritainct.gov/gov/boards/police_commission/general_information.htm',
		'https://www.newbritainct.gov/gov/boards/police_commission/board_members.htm',
		'https://www.newbritainct.gov/gov/boards/public_works_commission.htm',
		'https://www.newbritainct.gov/gov/boards/school_building_committee.htm',
		'https://www.newbritainct.gov/services/community/veterans/board.htm',
		'https://www.newbritainct.gov/gov/boards/zoning_board.htm',
		'https://www.newbritainct.gov/gov/charter_and_city_ordinances.htm',
		'https://www.newbritainct.gov/services/default.htm',
		'https://www.newbritainct.gov/services/assessor/default.htm',
		'https://www.newbritainct.gov/services/assessor/estate.htm',
		'https://www.newbritainct.gov/services/assessor/vehicle.htm',
		'https://www.newbritainct.gov/services/assessor/personal_property.htm',
		'http://newbritain.mapxpress.net/',
		'https://www.newbritainct.gov/services/assessor/appeals.htm',
		'https://www.newbritainct.gov/services/assessor/revalaution.htm',
		'https://www.newbritainct.gov/services/assessor/tax_relief.htm',
		'https://www.newbritainct.gov/services/assessor/reports.htm',
		'https://www.newbritainct.gov/services/building/default.htm',
		'https://newbritainct.viewpointcloud.com/',
		'https://www.newbritainct.gov/services/building/staff.htm',
		'https://www.newbritainct.gov/services/building/ordinances.htm',
		'https://www.newbritainct.gov/services/building/fees.htm',
		'https://www.newbritainct.gov/services/building/enforcement.htm',
		'https://www.newbritainct.gov/services/building/commission.htm',
		'https://www.newbritainct.gov/services/building/housing.htm',
		'https://www.newbritainct.gov/gov/boards/zoning_board.htm',
		'https://www.newbritainct.gov/services/community/default.htm',
		'https://www.newbritainct.gov/services/community/senior/default.htm',
		'https://www.newbritainct.gov/services/community/senior/general_info.htm',
		'https://www.newbritainct.gov/services/community/senior/members.htm',
		'https://www.newbritainct.gov/services/community/senior/notes.htm',
		'https://www.newbritainct.gov/services/community/veterans/default.htm',
		'https://www.newbritainct.gov/services/community/veterans/overview.htm',
		'https://www.newbritainct.gov/services/community/veterans/board.htm',
		'https://www.newbritainct.gov/services/community/veterans/memorial.htm',
		'https://www.newbritainct.gov/services/community/ada30_poster_contest.htm',
		'https://www.newbritainct.gov/services/corporation_counsel/default.htm',
		'https://www.newbritainct.gov/services/planning_n_development/default.htm',
		'https://s3-us-west-2.amazonaws.com/cerc-pdfs/2019/new-britain-2019.pdf',
		'https://www.newbritainct.gov/civicax/filebank/blobdload.aspx?t=44248.96&amp;BlobID=26242',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/economic_development.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/economic_development/covid_19_business_assistance.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/economic_development/economic_development_toolkit.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/economic_development/new_britain_real_estate.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/economic_development/projects_in_the_news.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/economic_development/starting_a_business.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/planning/default.htm',
		'https://www.newbritainct.gov/gov/boards/city_plan_commission.htm',
		'https://www.newbritainct.gov/gov/boards/conservation_commission.htm',
		'https://www.newbritainct.gov/gov/boards/historic_preservation.htm',
		'https://www.newbritainct.gov/gov/boards/zoning_board.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/community_development/default.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/community_development/programs.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/community_development/project_bid_opportunities.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/community_development/neighborhood_revitalization_zones.htm',
		'https://www.newbritainct.gov/services/office_of_planning_n_development/enterprise_zone_addresses.htm',
		'https://www.newbritainct.gov/services/finance/default.htm',
		'https://www.newbritainct.gov/services/finance/liaison.htm',
		'https://www.newbritainct.gov/services/finance/budget_management.htm',
		'https://www.newbritainct.gov/services/finance/reports.htm',
		'https://www.newbritainct.gov/services/health/default.htm',
		'https://www.newbritainct.gov/services/health/overview.htm',
		'https://www.newbritainct.gov/services/health/board_members.htm',
		'https://www.newbritainct.gov/services/health/corona_virus.htm',
		'https://www.newbritainct.gov/services/health/community_health_needs_assessment.htm',
		'https://www.newbritainct.gov/services/health/emergency_preparedness.htm',
		'https://www.newbritainct.gov/services/health/environmental.htm',
		'https://www.newbritainct.gov/services/health/nursing.htm',
		'https://www.newbritainct.gov/services/health/opiod_epidemic_information.htm',
		'https://www.newbritainct.gov/services/health/programs.htm',
		'https://www.newbritainct.gov/services/health/vaccinations.htm',
		'https://www.newbritainct.gov/services/civil/default.htm',
		'https://www.newbritainct.gov/services/civil/board.htm',
		'https://www.newbritainct.gov/services/civil/policy_on_sexual_harassment.htm',
		'https://www.newbritainct.gov/services/civil/employment/default.htm',
		'https://www.newbritainct.gov/services/civil/employment/applications.htm',
		'https://www.newbritainct.gov/services/civil/employment/job_postings.htm',
		'https://www.newbritainct.gov/services/civil/documents.htm',
		'https://www.newbritainct.gov/services/human_rights/default.htm',
		'https://www.newbritainct.gov/services/human_rights/general_info.htm',
		'https://www.newbritainct.gov/services/human_rights/board_members.htm',
		'https://www.newbritainct.gov/services/human_rights/services.htm',
		'https://www.newbritainct.gov/services/human_rights/discrimination.htm',
		'https://www.newbritainct.gov/services/human_rights/affirmative_action.htm',
		'https://www.newbritainct.gov/services/parking_ticket/default.htm',
		'https://www.newbritainct.gov/services/parking_ticket/payments.htm',
		'https://www.newbritainct.gov/services/parking_ticket/parking_authority.htm',
		'https://www.newbritainct.gov/services/parking_ticket/smart_cards.htm',
		'https://www.newbritainct.gov/services/recreation/default.htm',
		'https://www.newbritainct.gov/services/recreation/150_anniversary.htm',
		'https://www.newbritainct.gov/services/recreation/board_members.htm',
		'https://nbparksnrec.org/wbwsc/webtrac.wsc/contactus.html',
		'https://www.newbritainct.gov/services/recreation/directions.htm',
		'https://www.newbritainct.gov/services/recreation/fairview_cemetery.htm',
		'https://www.newbritainct.gov/services/recreation/job_listings.htm',
		'https://nbparksnrec.org/wbwsc/webtrac.wsc/SPLASH.html',
		'https://www.newbritainct.gov/services/recreation/stanley_golf.htm',
		'https://www.newbritainct.gov/services/recreation/terrific_toys.htm',
		'https://www.newbritainct.gov/services/recreation/benefits.htm',
		'https://www.newbritainct.gov/services/public_safety/default.htm',
		'https://www.newbritainct.gov/services/public_safety/ems.htm',
		'https://www.newbritainct.gov/services/public_safety/fire.htm',
		'https://www.newbritainct.gov/services/public_safety/police/default.htm',
		'https://permits.newbritainpolice.org',
		'https://www.newbritainct.gov/services/public_safety/telecommunication_center.htm',
		'https://www.newbritainct.gov/services/public_works/default.htm',
		'https://www.newbritainct.gov/services/public_works/divisions/default.htm',
		'https://www.newbritainct.gov/services/public_works/divisions/administration.htm',
		'https://www.newbritainct.gov/services/public_works/divisions/field_services.htm',
		'https://www.newbritainct.gov/services/public_works/divisions/utilities.htm',
		'https://www.newbritainct.gov/services/public_works/divisions/fleet_management.htm',
		'https://www.newbritainct.gov/services/public_works/divisions/engineering_n_row_management.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/default.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/curbside_services/default.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/curbside_services/weekly_curbside_trash_collection.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/curbside_services/bi_weekly_recycling_collection.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/curbside_services/scheduled_curbside_burnable_collection.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/curbside_services/scheduled_curbside_non_burnable_collection.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/trash_collection_day_map.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/a_n_b_week_recycling_information.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/holiday_week_collection_schedule.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/guide.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/env_cal.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/recycling_center_operations.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/simple_recycling.htm',
		'https://www.newbritainct.gov/services/public_works/refuse_n_recycling/trash_and_recycling_containers.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/default.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/pavement_management_program.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/pothole.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/sidewalk.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/fall_collection.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/spring_collection.htm',
		'https://www.newbritainct.gov/services/public_works/programs_n_services/stormwater_management.htm',
		'https://www.newbritainct.gov/services/public_works/winter_storm_operations.htm',
		'https://www.newbritainct.gov/services/public_works/fees.htm',
		'https://www.newbritainct.gov/services/public_works/new_britains_complete_streets/default.htm',
		'https://www.newbritainct.gov/services/public_works/new_britains_complete_streets/bike.htm',
		'https://www.newbritainct.gov/services/public_works/new_britains_complete_streets/complete_streets_roadmap.htm',
		'https://www.newbritainct.gov/services/public_works/new_britains_complete_streets/ctfastrak.htm',
		'https://www.newbritainct.gov/services/public_works/capital_projects.htm',
		'https://www.newbritainct.gov/services/public_works/documents_n_reports.htm',
		'http://newbritain.mapxpress.net/',
		'https://www.newbritainct.gov/services/public_works/beehivebridge.htm',
		'https://www.newbritainct.gov/services/purchasing/default.htm',
		'https://www.newbritainct.gov/services/purchasing/bids.htm',
		'https://www.newbritainct.gov/services/purchasing/closed_bids.htm',
		'https://www.newbritainct.gov/services/registrar_of_voters/default.htm',
		'https://www.newbritainct.gov/services/registrar_of_voters/democrats.htm',
		'https://www.newbritainct.gov/services/registrar_of_voters/republicans.htm',
		'https://www.newbritainct.gov/services/registrar_of_voters/voting_locations.htm',
		'https://www.newbritainct.gov/services/support_services/default.htm',
		'https://www.newbritainct.gov/services/support_services/information_technology.htm',
		'https://www.newbritainct.gov/services/support_services/facilities_n_energy.htm',
		'https://www.newbritainct.gov/services/support_services/telecommunications.htm',
		'https://www.newbritainct.gov/services/tax_collector/default.htm',
		'https://www.newbritainct.gov/services/tax_collector/covid19_related_faqs.htm',
		'https://www.newbritainct.gov/services/tax_collector/online_tax_payments.htm',
		'https://www.newbritainct.gov/services/tax_collector/online_utility_payments.htm',
		'https://www.newbritainct.gov/services/tax_collector/legal_rulings.htm',
		'https://www.newbritainct.gov/services/tax_collector/faqs.htm',
		'https://www.newbritainct.gov/services/town_clerk/default.htm',
		'https://www.newbritainct.gov/services/town_clerk/meet_thetown_clerk.htm',
		'https://www.newbritainct.gov/services/town_clerk/meet_thetown_clerks_office.htm',
		'https://www.newbritainct.gov/services/town_clerk/land_records.htm',
		'https://www.newbritainct.gov/services/town_clerk/zone_change.htm',
		'https://www.newbritainct.gov/services/town_clerk/vital_records.htm',
		'https://www.newbritainct.gov/services/town_clerk/licenses.htm',
		'https://www.newbritainct.gov/services/town_clerk/elections.htm',
		'https://www.newbritainct.gov/gov/default.htm',
		'https://www.newbritainct.gov/services/town_clerk/business_commercial.htm',
		'https://www.newbritainct.gov/services/town_clerk/military_discharge.htm',
		'https://www.newbritainct.gov/services/town_clerk/basic_fee_schedule.htm',
		'https://www.newbritainct.gov/services/water_department/general_information.htm',
		'https://www.newbritainct.gov/services/water_department/board_members.htm',
		'https://www.newbritainct.gov/services/water_department/water_company_land_use.htm',
		'https://www.newbritainct.gov/services/water_department/water_company_summit.htm',
		'https://www.newbritainct.gov/services/water_department/water_main_flushing.htm',
		'https://www.newbritainct.gov/services/water_department/water_main_replacement.htm',
		'https://www.newbritainct.gov/services/water_department/water_sewer_line_protection.htm',
		'https://www.newbritainct.gov/services/water_department/water_n_sewer_rates.htm',
		'https://www.visitnbct.com/',
		'https://www.newbritainct.gov/about_new_britain.htm',
		'https://www.newbritainct.gov/civicax/filebank/blobdload.aspx?BlobID=26482',
		'https://www.visitnbct.com/business_list/category/arts/museums',
		'https://www.visitnbct.com/bees_across_nb',
		'https://www.visitnbct.com/explore_new_britain/downtown',
		'http://historicnb.org/home',
		'http://nbbees.com/',
		'https://www.newbritainct.gov/visit_nb/parks.htm',
		'https://www.visitnbct.com/sports/recreation',
		'https://www.visitnbct.com/business_list/category/restaurants/american',
		'https://www.visitnbct.com/sports/sports',
		'https://www.nbyouthprevention.com',
		'https://www.newbritainct.gov/documents/default.htm',
		'https://library.municode.com/ct/new_Britain',
		'https://www.newbritainct.gov/documents/online_emergency_registration_forms.htm',
		'https://www.newbritainct.gov/documents/policies_n_procedures.htm',
		'https://www.newbritainct.gov/notices/default.htm',
		'https://www.newbritainct.gov/notices/notices.htm',
		'https://www.newbritainct.gov/notices/press_releases.htm',
		'https://www.newbritainct.gov/notices/rss_news_feed.htm',
		'https://www.newbritainct.gov/contact/default.htm',
		'https://www.newbritainct.gov/contact/form/default.htm',
		'https://www.newbritainct.gov/contact/form/assessor.htm',
		'https://www.newbritainct.gov/contact/form/board_of_education.htm',
		'https://www.newbritainct.gov/contact/form/building_department.htm',
		'https://www.newbritainct.gov/contact/contact_forms/city_hall_commission.htm',
		'https://www.newbritainct.gov/contact/form/city_plan.htm',
		'https://www.newbritainct.gov/contact/form/common_council.htm',
		'https://www.newbritainct.gov/contact/form/community_services.htm',
		'https://www.newbritainct.gov/contact/form/corporation_counsel.htm',
		'https://www.newbritainct.gov/contact/form/economic_development.htm',
		'https://www.newbritainct.gov/contact/form/finance_department.htm',
		'https://www.newbritainct.gov/contact/form/fire_chief.htm',
		'https://www.newbritainct.gov/contact/form/health_department.htm',
		'https://www.newbritainct.gov/contact/form/human_resources.htm',
		'https://www.newbritainct.gov/contact/form/human_rights_n_opportunities.htm',
		'https://www.newbritainct.gov/contact/form/information_technology.htm',
		'https://www.newbritainct.gov/contact/form/mayors_office.htm',
		'https://www.newbritainct.gov/contact/form/municipal_development.htm',
		'https://www.newbritainct.gov/contact/form/parks_and_recreation.htm',
		'https://www.newbritainct.gov/contact/form/police_department.htm',
		'https://www.newbritainct.gov/contact/form/public_works.htm',
		'https://www.newbritainct.gov/contact/form/support_services.htm',
		'https://www.newbritainct.gov/contact/form/tax_collector.htm',
		'https://www.newbritainct.gov/contact/form/town_clerk.htm',
		'https://www.newbritainct.gov/sitemap.htm',
		'https://nbsvex2016.newbritainct.gov/owa/',
		'https://eo.newbritainct.gov/Finance/Edge/',
		'https://www.newbritainct.gov/civicax/filebank/blobdload.aspx?BlobID=25796',
	]
	# mainfolder = all_sites[0].split('.')[1]
	mainfolder = 'newbritainct'
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
		school_name = 'newbritainct'

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
