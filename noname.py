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
		# web_link = requests.get(web_page, headers=headers, timeout=20, verify=False).content
		web_link = requests.get(web_page, headers=headers, timeout=20).content
		web_soup = BeautifulSoup(web_link, 'html.parser')

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(id='mainbody').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='mainbody').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='mainbody').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='mainbody').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='mainbody').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='mainbody').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='mainbody') != None and web_soup.find(id='mainbody') != '':
			col1 = web_soup.find(id='mainbody')
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
		'https://www.carrollk12.org/schools/elementary/ces/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/specialeducation/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/PTAPTO.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/ces/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/About/Pages/OnTrackBehaviorSystem.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/SpecialAreas/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/SpecialAreas/Pages/Art.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/SpecialAreas/Pages/Health.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/SpecialAreas/Pages/Music.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/SpecialAreas/Pages/PhysicalEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/About/Pages/Diversity-Club.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/Before--After-School-Care.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/healthroominfo/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/healthroominfo/Pages/Nurse-Notes.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/PTAPTO.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/cse/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/specialareas/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/MusicDepartment/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/MusicDepartment/Pages/Chorus.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/MusicDepartment/Pages/Instrumental.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/MusicDepartment/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/Before--After-School-Care.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/PTO.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/eve/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/Before--After-School-Care.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/PTAPTO.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/ees/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/PTO.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/ewe/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/Before--After-School-Care.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/PTA.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/fes/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/specialareas/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/specialareas/Pages/Physical-Education.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/specialareas/Pages/Instrumental-Music.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/specialareas/Pages/Reading.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/PTO.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/fve/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/SpecialAreas/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/SpecialEducation/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/SpecialEducation/Pages/Autism.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/SpecialEducation/Pages/LFI.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/SpecialEducation/Pages/PREP.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/SpecialEducation/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/PTO.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/ham/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Pages/GiftAndTalented.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/Registration.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/healthroominfo/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/healthroominfo/Pages/Medical-Forms--Links.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/healthroominfo/Pages/Health-Room-Notes.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/pta/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/pta/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/lse/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/man/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/man/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/man/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/man/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/man/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/media/Pages/Reading-List.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/PTA.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/man/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/man/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/specialareas/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/PTA.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/mes/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/specialareas/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/PTAPTO.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/mae/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/par/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/par/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/par/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/par/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/par/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/PTO.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/par/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/par/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/About/Pages/VideoResources.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/About/Pages/PBIS.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Pages/SpecialEducation.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/FARM.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/HealthRoomInfo.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/HAC.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/OnlineResources.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/PTAPTO.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/SchoolSupplyList.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/StudentParentHandbook.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/SchoolRewardsPrograms.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/ParentsCommunity/Pages/VolunteerInformation.aspx',
		'https://www.carrollk12.org/schools/elementary/pre/Teams/Pages/SchoolCounselor.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/About/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/About/Pages/MissionStatement.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/About/Pages/SchoolImprovementPlan.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/About/Pages/StaffDirectory.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/PreK/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Kindergarten/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Grade1/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Grade2/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Grade3/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Grade4/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Grade5/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/media/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/media/Pages/Events.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/media/Pages/Programs.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/media/Pages/Resources.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/Teams/Pages/SpecialAreas.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/ParentsCommunity/Pages/default.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/ParentsCommunity/Pages/Attendance.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/ParentsCommunity/Pages/BusRoutes.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/ParentsCommunity/Pages/CafeteriaMenus.aspx',
		'https://www.carrollk12.org/schools/elementary/rme/ParentsCommunity/Pages/FARM.aspx',
	]
	mainfolder = 'carrollk12'
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
		school_name = 'carrollk12'

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
					t1 = tiers[-6].capitalize()
					t2 = tiers[-5].capitalize()
					t3 = tiers[-4].capitalize()
					t4 = tiers[-3].capitalize()
					t5 = tiers[-2].capitalize()
					t6 = tiers[-1].capitalize()
					print(len(tiers))

				page_link = link

				page_counter += 1
				col1, col2, col3, col4, col_num, nav_sec, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
				issue_pages_counter += content_ipc

				csv_writer.writerow([str(page_link), t1, t2, t3, t4, t5, t6, col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

				if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
					csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])

				# if nav_sec != None and nav_sec != '' and nav_sec != []:
				# 	for nav_link in nav_sec:
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
