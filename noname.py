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

		if web_soup.find(id='sl-cms2-main-section').find_all('form') != []:
			form = 'form'

		if web_soup.find(id='sl-cms2-main-section').find_all('embed') != []:
			embed = 'embed'

		if web_soup.find(id='sl-cms2-main-section').find_all('iframe') != []:
			iframe = 'iframe'

		if web_soup.find(id='sl-cms2-main-section').find_all(class_='calendar') != []:
			calendar = 'calendar'

		if web_soup.find(id='sl-cms2-main-section').find_all(class_='staff-directory') != []:
			staff = 'staff'

		if web_soup.find(id='sl-cms2-main-section').find_all(class_='news') != []:
			news = 'news'

		# if web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn') != None:
		# 	page_nav = web_soup.find(class_='hidden-xs show-on-olc col-sm-4 col-md-3 col-lg-3 backgroundcolor leftColumn').find_all('a')
		# elif web_soup.find(id='quicklinks') != None:
		# 	page_nav = web_soup.find(id='quicklinks').find_all('a')

		# Content
		if web_soup.find(id='sl-cms2-main-section') != None and web_soup.find(id='sl-cms2-main-section') != '':
			col1 = web_soup.find(id='sl-cms2-main-section')
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
		'https://lbbancroft.schoolloop.com/os',
		'https://lbbancroft.schoolloop.com/staff',
		'https://lbbancroft.schoolloop.com/bell',
		'https://lbbancroft.schoolloop.com/hs',
		'https://lbbancroft.schoolloop.com/dresscode',
		'https://lbbancroft.schoolloop.com/nursing',
		'https://lbbancroft.schoolloop.com/nutrition',
		'https://lbbancroft.schoolloop.com/clubs',
		'https://lbbancroft.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404143710&vdid=i1k33f1y0p44gs',
		'https://lbbancroft.schoolloop.com/dp',
		'https://lbbancroft.schoolloop.com/6gradeelectives',
		'https://lbbancroft.schoolloop.com/7thelectives',
		'https://lbbancroft.schoolloop.com/8thgrade',
		'https://lbbancroft.schoolloop.com/char_ed',
		'https://lbbancroft.schoolloop.com/cjsf',
		'https://lbbancroft.schoolloop.com/health',
		'https://lbbancroft.schoolloop.com/history',
		'https://lbbancroft.schoolloop.com/la',
		'https://lbbancroft.schoolloop.com/math',
		'https://lbbancroft.schoolloop.com/pe',
		'https://lbbancroft.schoolloop.com/science',
		'https://lbbancroft.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404143752&vdid=i13f1yv8k120',
		'https://lbbancroft.schoolloop.com/summit',
		'https://lbbancroft.schoolloop.com/atm',
		'https://lbbancroft.schoolloop.com/vapa',
		'https://lbbancroft.schoolloop.com/technology',
		'https://lbbancroft.schoolloop.com/atm',
		'https://lbbancroft.schoolloop.com/videos',
		'https://lbbancroft.schoolloop.com/pta',
		'https://lbbancroft.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404143766&vdid=i1n3f1yhq0f44wt',
		'https://lbbancroft.schoolloop.com/cybersafety',

		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205246&vdid=pi35e1ymdjj2',
		'https://lbcubberley.schoolloop.com/academicattire',
		'https://lbcubberley.schoolloop.com/bellscheduleselementary',
		'https://lbcubberley.schoolloop.com/bellschedulesmiddleschool',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205246&vdid=i35c9ae1ymodjl5',
		'https://lbcubberley.schoolloop.com/parenthandbookimportantdates',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205246&vdid=i35eov14ymddjm7',
		'https://lbcubberley.schoolloop.com/mapdrivingdirections',
		'https://lbcubberley.schoolloop.com/aboutusschoolmenus',
		'https://lbcubberley.schoolloop.com/schoolanddistrictforms',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205246&vdid=li35e1y0xmdjo7',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205246&vdid=iu735ei1ymdjon',
		'https://lbcubberley.schoolloop.com/programs',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205269&vdid=6ib35e2qfmm6o1hx',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205273&vdid=i358e1ymtdjpu',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205278&vdid=i35e1ley0mdjqb',
		'https://lbcubberley.schoolloop.com/mesa',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205269&vdid=ui35e2po4r4n193',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205306&vdid=i35e1y6mdjrz',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205309&vdid=i35e1ymdjsj',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205321&vdid=i35e9rdj1ymdjta',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205329&vdid=i3j5e1ymldjty',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205339&vdid=i35e1ymdjuk',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205339&vdid=ig3g5ie1ymdjv7',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205348&vdid=i35e1ymdjw4',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205348&vdid=i32t5ep1ymdjwn',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205348&vdid=i35e1ymdjxa',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205391&vdid=i35e1ymdjxy',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205632&vdid=2i35e1ymjdj15n',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205655&vdid=i3a5e1ymdj165',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205741&vdid=sie53o5e1ymdj189',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205632&vdid=pi35e276351ci',
		'https://lbcubberley.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205632&vdid=i356e71ym2tdj1cu',

		'https://lbfranklin.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205223&vdid=i202e1hxymndj147',
		'https://lbfranklin.schoolloop.com/dresscode',
		'https://lbfranklin.schoolloop.com/staff',
		'https://lbfranklin.schoolloop.com/parents',
		'https://lbfranklin.schoolloop.com/canvasparents',
		'https://lbschools.instructure.com/courses/16155',
		'https://drive.google.com/file/d/1PbZVT9PvUlkbHc8HswqSdf1toFfkOBCW/view?usp=sharing',
		'https://lbfranklin.schoolloop.com/giving',
		'https://lbfranklin.schoolloop.com/elac',
		'https://www.lbschools.net/Departments/Student_Support_Services/frc.cfm',
		'https://lbfranklin.schoolloop.com/hsc',
		'https://lbfranklin.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205338&vdid=i20e1ymdj1q8',
		'https://lbfranklin.schoolloop.com/file/1535782205338/1282485006358/3030268355381419912.pdf',
		'https://lbfranklin.schoolloop.com/caaspp',
		'https://lbfranklin.schoolloop.com/title1',
		'https://lbfranklin.schoolloop.com/ix',
		'https://lbfranklin.schoolloop.com/ucp',
		'https://lbfranklin.schoolloop.com/vips',
		'https://lbfranklin.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205338&vdid=i20e1ymjayedj1sf',
		'https://lbfranklin.schoolloop.com/students',
		'https://lbfranklin.schoolloop.com/camera',
		'https://lbfranklin.schoolloop.com/mic',
		'https://lbfranklin.schoolloop.com/update',
		'https://lbfranklin.schoolloop.com/zoom',
		'https://lbfranklin.schoolloop.com/password',
		'https://lbfranklin.schoolloop.com/canvas',
		'https://lbfranklin.schoolloop.com/remote',
		'https://lbfranklin.schoolloop.com/troubleshooting',
		'https://lbfranklin.schoolloop.com/wifi',
		'https://lbfranklin.schoolloop.com/own',
		'https://lbfranklin.schoolloop.com/other',
		'https://lbfranklin.schoolloop.com/teachers',
		'https://lbfranklin.schoolloop.com/canvasparents',
		'https://lbfranklin.schoolloop.com/canvasparentapp',
		'https://lbschools.instructure.com/courses/16155',
		'https://drive.google.com/file/d/1PbZVT9PvUlkbHc8HswqSdf1toFfkOBCW/view?usp=sharing',
		'https://lbfranklin.schoolloop.com/canvas',
		'https://lbfranklin.schoolloop.com/canvasstudentapp',
		'https://lbfranklin.schoolloop.com/chromebooks',
		'https://lbfranklin.schoolloop.com/cloud',
		'https://lbfranklin.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205400&vdid=i20e1ymdj2l7',
		'https://lbfranklin.schoolloop.com/msoffice',
		'https://lbfranklin.schoolloop.com/practice',
		'https://lbfranklin.schoolloop.com/technology',
		'https://lbfranklin.schoolloop.com/email',
		'https://lbfranklin.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205400&vdid=i20e1ymdj22m',

		'https://lbhamilton.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1641456435206&vdid=i124e3513r8du7',
		'https://lbhamilton.schoolloop.com/college_board_khan_signups',
		'https://lbhamilton.schoolloop.com/puppies',
		'https://lbhamilton.schoolloop.com/attendance',
		'https://lbhamilton.schoolloop.com/bellschedule',
		'https://lbhamilton.schoolloop.com/uniform',
		'https://lbhamilton.schoolloop.com/hs_readiness',
		'https://lbhamilton.schoolloop.com/create_college_board_id',
		'https://lbhamilton.schoolloop.com/khan_troubleshooting',
		'https://lbhamilton.schoolloop.com/Core_Survey_Students',
		'https://lbhamilton.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205395&vdid=i24xe1xymdju4',
		'https://lbhamilton.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205396&vdid=i24e1ymdjve',
		'https://lbhamilton.schoolloop.com/dress_for_success_2017',
		'https://lbhamilton.schoolloop.com/split_window_a',
		'https://lbhamilton.schoolloop.com/split_window_b',
		'https://lbhamilton.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1641456435206&vdid=i24l6e30v7lw3by',
		'https://lbhamilton.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=ti24e308upw2u5',
		'https://lbhamilton.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i24ofue3008pw2u7',
		'https://lbhamilton.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i2xg4e23s07lw3n9',
		'https://lbhamilton.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i24qve3307lw3n8',
		'https://lbhamilton.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1641456435206&vdid=i124e3513r8du7',
		'https://lbhamilton.schoolloop.com/Staff',
		'https://lbhamilton.schoolloop.com/tech_team',
		'https://lbhamilton.schoolloop.com/chromebooks',
		'https://lbhamilton.schoolloop.com/lanschool_notes',
		'https://lbhamilton.schoolloop.com/synergy_assessments',
		'https://lbhamilton.schoolloop.com/misc_resources',
		'https://lbhamilton.schoolloop.com/staff_locker',
		'https://lbhamilton.schoolloop.com/staff_tutorials',
		'https://lbhamilton.schoolloop.com/wifi',
		'https://lbhamilton.schoolloop.com/reserve_lab',
		'https://lbhamilton.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205457&vdid=i2g4e1yqmndj1ql',
		'https://lbhamilton.schoolloop.com/use_messenger',
		'https://lbhamilton.schoolloop.com/professional_page',
		'https://lbhamilton.schoolloop.com/portal',
		'https://lbhamilton.schoolloop.com/add_link',
		'https://lbhamilton.schoolloop.com/join_board',
		'https://lbhamilton.schoolloop.com/auditorium_signup',
		'https://lbhamilton.schoolloop.com/bootstrap_badge',
		'https://lbhamilton.schoolloop.com/exercise_room_av',
		'https://lbhamilton.schoolloop.com/google_drive',
		'https://lbhamilton.schoolloop.com/add_shared_folder',
		'https://lbhamilton.schoolloop.com/complete_department_template',
		'https://lbhamilton.schoolloop.com/lanschool_lab_warmup',
		'https://lbhamilton.schoolloop.com/redeploy_google_quiz',
		'https://lbhamilton.schoolloop.com/hamiltonprograms',
		'https://lbhamilton.schoolloop.com/girls_volleyball_2015-16',
		'https://lbhamilton.schoolloop.com/gearup',
		'https://lbhamilton.schoolloop.com/ICES',
		'https://lbhamilton.schoolloop.com/male_academy',
		'https://lbhamilton.schoolloop.com/webprogram',
		'https://lbhamilton.schoolloop.com/parent_involvement',
		'https://lbhamilton.schoolloop.com/tutoring',
		'https://lbhamilton.schoolloop.com/resources',
		'https://lbhamilton.schoolloop.com/Library',
		'https://lbhamilton.schoolloop.com/labs',
		'https://lbhamilton.schoolloop.com/Math_Support',
		'https://lbhamilton.schoolloop.com/academics',
		'https://lbhamilton.schoolloop.com/piqe',
		'https://lbhamilton.schoolloop.com/id_creator',
		'https://lbhamilton.schoolloop.com/collaborative_conversation_grit',
		'https://lbhamilton.schoolloop.com/8th_PSAT',
		'https://lbhamilton.schoolloop.com/why_college',
		'https://lbhamilton.schoolloop.com/fundraiser_prizes_2016',
		'https://lbhamilton.schoolloop.com/9am_group_2018',
		'https://lbhamilton.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205501&vdid=i2t4sxe17zx22bj',

		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102261&vdid=5i16a2lw2ia9n',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102261&vdid=il516a29ln0l3mz',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102261&vdid=i16a1y0u5o8t',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102261&vdid=ni16a1y0e5o9b',
		'https://lbhoover.schoolloop.com/map',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102261&vdid=i16a1y05oaa',
		'https://lbhoover.schoolloop.com/highschool',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102286&vdid=i16a1y05obb',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102338&vdid=hie16af1ky05ogz',
		'https://lbhoover.schoolloop.com/alps',
		'https://lbhoover.schoolloop.com/sports',
		'https://lbhoover.schoolloop.com/wrap',
		'https://lbhoover.schoolloop.com/CalculateGPA',
		'https://lbhoover.schoolloop.com/commoncore',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102675&vdid=i1p6al51yx05omh',
		'https://lbhoover.schoolloop.com/parents',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102675&vdid=imn16a1ely05op9',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102675&vdid=imn16a1ely05op9',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102713&vdid=ilj16a1y0i5ot8',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102713&vdid=i16a1tfy05ouq',
		'https://lbhoover.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404102748&vdid=ihj1d6a1yb05ovb',
		'https://lbhoover.schoolloop.com/stafflistdept',
		'https://lbhoover.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i16a2byfb65x',

		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205593&vdid=skwi38c1ymcvm9',
		'https://lbhughes.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i3f8c2wht952pn',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205593&vdid=i38c41ymmcvq1',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205593&vdid=i38c1yqmcvre',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205593&vdid=i3o348c2v8sgzz',
		'https:/hughes.myschoolcentral.com/',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205643&vdid=i38c1ymcvnw',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205660&vdid=vi38cd1o2v6kd1by',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205660&vdid=iw38c3g1ycmcvp1',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205660&vdid=i38c1ymcvof',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206149&vdid=ei38c1ymcv1vy',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205889&vdid=i378oc1bym6cv154',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205911&vdid=ci38c18vymcv15s',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206043&vdid=i38dyc1dymcv1pr',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205959&vdid=i38c2uae2136',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i38c1wiy9mcv1h5',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205864&vdid=ik1c38c2yg3724p',
		'https://lbhughes.schoolloop.com/news',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206076&vdid=i378c1ymcv1rt',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205864&vdid=i38ce2enemr10c',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206058&vdid=i3j98co1ymcv1qf',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i38c1wiy9mcv1h5',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i3q8c9b1ymcv1i0',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i381c1oymfkcv1iq',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i38c1ymcv1jl',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i3b8c1ymcv1ke',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i038c1ymdcv1l7',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=0wi381c1ymjcv1m1',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=i383c15y43mcv1mt',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205976&vdid=7i38c1ymcv1no',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971736&vdid=i38c30q2a2u0',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971736&vdid=wi38dc2vqkozg',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971736&vdid=i3k8c2y751bj1ap',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971736&vdid=2i38c2mh4yf1fk',
		'https://lbhughes.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971736&vdid=i38c2vqkozx',

		'https://lbjefferson.schoolloop.com/access',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205787&vdid=uir1hs2c1ymcl1l8',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205787&vdid=i12cb1ymcl1kl',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205787&vdid=i12ccu1ym5cl1jz',
		'https://www.lbschools.net/Departments/Board_of_Education/policies.cfm',
		'https://lbjefferson.schoolloop.com/spiritwear',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205787&vdid=i12c19oymlcl1n0',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205808&vdid=i12c1yhmcl1nr',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205808&vdid=i12c1ymcl1oi',
		'https://lbjefferson.schoolloop.com/library',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205888&vdid=di12c1hyqmdcl1xw',
		'https://lbjefferson.schoolloop.com/Math_Support',
		'https://lbjefferson.schoolloop.com/hsinfo',
		'https://www.lbschools.net/studentvue',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205888&vdid=i12c2ifnj2ab',
		'https://www.lbschools.net/Departments/Board_of_Education/policies.cfm',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205878&vdid=i12cp21y8mcl1tx',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205878&vdid=scpi12c1ywmcl1ur',
		'https://lbjefferson.schoolloop.com/parentvue',
		'https://lbjefferson.schoolloop.com/elac',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205878&vdid=i12c1oydsmcl1vj',
		'https://lbjefferson.schoolloop.com/ssc',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205823&vdid=in12c2wt95n7e',
		'https://lbjefferson.schoolloop.com/clubs',
		'https://lbjefferson.schoolloop.com/gogreen',
		'https://lbjefferson.schoolloop.com/gate/acc',
		'https://lbjefferson.schoolloop.com/electives',
		'https://lbjefferson.schoolloop.com/ices',
		'https://lbjefferson.schoolloop.com/robotics',
		'https://lbjefferson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1609231426748&vdid=i1w2c2pjpa13ku',

		'https://kellerms-lbusd-ca.schoolloop.com/principalsmessage',
		'https://kellerms-lbusd-ca.schoolloop.com/bellschedule',
		'https://kellerms-lbusd-ca.schoolloop.com/uniforms',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205699&vdid=i56c2fpvd24l',
		'https://kellerms-lbusd-ca.schoolloop.com/menus',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1567840701475&vdid=i56llc2aacu214',
		'https://kellerms-lbusd-ca.schoolloop.com/teachin',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205729&vdid=di56c1ymcxvd',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205770&vdid=i5u6t9c1y3mcxvx',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=ip56c20a7l1h1be',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i56c24a7o1h29r',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i56c2a96j30u',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i56c22a96j31d',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=mi56c2c71o42aq',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=mi56c2ke46j2br',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i568c2av9x6j31x',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i56c2a96j32n',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=ir56cjx2a9k6j33g',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i56c2aacu1za',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=io56c2aacu1sp',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i56c2aajcu1tf',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i5k6vc2aahcu1u3',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i56ice472aacu1up',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205755&vdid=i56dc52ugaacu1vc',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1567840302574&vdid=i56auci2a2jv20p',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1567840302574&vdid=i56c24a2jv268',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205779&vdid=ii5f6jc2a871h1pn',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205779&vdid=i56cm2a853x1wd',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205779&vdid=wxiv56c2a83x1vm',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205779&vdid=ia56c2a8g63x1xz',
		'https://kellerms-lbusd-ca.schoolloop.com/CollabResources',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205779&vdid=i56c4l2a83x28i',
		'https://kellerms-lbusd-ca.schoolloop.com/examenestatal',
		'https://kellerms-lbusd-ca.schoolloop.com/Resources',
		'https://kellerms-lbusd-ca.schoolloop.com/statetestinfo',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205799&vdid=i5q6c2a9ful1p7',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205799&vdid=i5966c1ymcx15m',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205799&vdid=i56c1ymcx161',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205799&vdid=si56cn1ymcx16m',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=i56c2od5a22yj',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=i56cy2co5a22vc',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=i56g5c72alno91dg',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=it56tcj2o5a22wd',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=i56c2oe5a22xt',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=e1i56c2vqbb061ub',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=i56c2bba062e8',
		'https://www.lbschools.net/Asset/Files/School_Choice/19-20/8th-Grade-Mailer-EN.pdf',
		'https://www.lbschools.net/Departments/High-Schools/Pathways/industry.cfm',
		'https://www.lbschools.net/Departments/High-Schools/Pathways/school.cfm',
		'https://drive.google.com/file/d/1qWffNty1h9BF0qBrgv7OO5nplBRsJ5OL/view',
		'https://www.lbschools.net/Asset/Files/School_Choice/18-19/2018-2019-Minimum-Critera-SP-v2.pdf',
		'https://www.lbschools.net/Asset/Files/School_Choice/18-19/2018-2019-School-Descriptions-EN-v2.pdf',
		'https://www.lbschools.net/Asset/Files/School_Choice/18-19/2018-2019-School-Descriptions-SP-v2.pdf',
		'https://kellerms-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205820&vdid=i5s6oc2o5ta22qt',

		'https://lblindbergh.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206166&vdid=yi15c2yv9fcbbj',
		'https://lblindbergh.schoolloop.com/uniforms',
		'https://lblindbergh.schoolloop.com/bellschedule',
		'https://lblindbergh.schoolloop.com/sarc',
		'https://lblindbergh.schoolloop.com/schoolwidediscipline',
		'https://lblindbergh.schoolloop.com/emergency',
		'https://lblindbergh.schoolloop.com/community',
		'https://lblindbergh.schoolloop.com/frc',
		'https://lblindbergh.schoolloop.com/title1',
		'https://lblindbergh.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=iw15c2ays85q8',
		'https://lblindbergh.schoolloop.com/parentcommunication',
		'https://lblindbergh.schoolloop.com/elac',
		'https://lblindbergh.schoolloop.com/ssc',
		'https://lblindbergh.schoolloop.com/vips',
		'https://lblindbergh.schoolloop.com/canvasforparents',
		'https://lblindbergh.schoolloop.com/admin',
		'https://lblindbergh.schoolloop.com/supportstaff',
		'https://lblindbergh.schoolloop.com/teachers',
		'https://eagleswebstore.myschoolcentral.com/',
		'https://lblindbergh.schoolloop.com/studentresources',
		'https://lblindbergh.schoolloop.com/library',
		'https://lblindbergh.schoolloop.com/Sports',
		'https://lblindbergh.schoolloop.com/netiquette',
		'https://lblindbergh.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206269&vdid=i15c2j2pr0fd5fl',
		'https://lblindbergh.schoolloop.com/Robotics',
		'https://lblindbergh.schoolloop.com/PLTW',
		'https://lblindbergh.schoolloop.com/HSChoice',

		'https://lblindsey.schoolloop.com/perrywlindsey',
		'https://drive.google.com/file/d/1fkX2tIbV9uqvh_lSFQpCA0istzt-T8nn/view?usp=sharing',
		'https://lblindsey.schoolloop.com/antibully',
		'https://lblindsey.schoolloop.com/netiquette',
		'https://lblindsey.schoolloop.com/calculate.your.gpa',
		'https://lblindsey.schoolloop.com/safe&civil',
		'https://lblindsey.schoolloop.com/technews',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206178&vdid=i10c1ymcn197',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206061&vdid=i610vc19ymvcnw7',
		'https://lblindsey.schoolloop.com/history6',
		'https://lblindsey.schoolloop.com/history7',
		'https://lblindsey.schoolloop.com/history8',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206074&vdid=i10ce1ymcnyr',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206129&vdid=ic610c1yomcnzg',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206143&vdid=vi110c1y2mcnzx',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206157&vdid=ik1a0c1ymcn11g',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206170&vdid=3iv10c1aymcn11z',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206053&vdid=im010ce2fufax4f2',
		'https://lblindsey.schoolloop.com/lindseysports',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206041&vdid=i1n0c10ywpmcnop',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206041&vdid=i11x00c1yrmcnu8',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206041&vdid=i1j30c1ymcnng',
		'https://lblindsey.schoolloop.com/boysbasketball',
		'https://lblindsey.schoolloop.com/girlssoccer',
		'https://lblindsey.schoolloop.com/boyssoccer',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206041&vdid=i10c1ymvmcnrt',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206041&vdid=pi10c715dymcnt2',
		'https://lblindsey.schoolloop.com/crosscountry',
		'https://lblindsey.schoolloop.com/library',
		'https://lblindsey.schoolloop.com/Research',
		'https://lblindsey.schoolloop.com/evaluation',
		'https://lblindsey.schoolloop.com/Parents',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206217&vdid=i10wc731ymcn1bz',
		'https://lblindsey.schoolloop.com/highschoolchoice',
		'https://lblindsey.schoolloop.com/title1',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206229&vdid=i10c1ymcn1dj',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206229&vdid=i10y9c1ymcn1e2',
		'https://lblindsey.schoolloop.com/teacherresources',
		'https://lblindsey.schoolloop.com/Parents',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206217&vdid=i10wc731ymcn1bz',
		'https://lblindsey.schoolloop.com/highschoolchoice',
		'https://lblindsey.schoolloop.com/title1',
		'https://lblindsey.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206248&vdid=i1kh0c2a11h44pg',

		'https://lbmarshall.schoolloop.com/principalsmessage',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206301&vdid=dbi15d1jypmcv1qn',
		'https://lbmarshall.schoolloop.com/uniformguidelines',
		'https://lbmarshall.schoolloop.com/schoolanddistrictforms',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206301&vdid=i15d1ymtcv1s3',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206301&vdid=i1ed5d1yqmcv1sj',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206306&vdid=i1o5d21o8kw96b',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206319&vdid=i1hy5md1ymcv250',
		'https://lbmarshall.schoolloop.com/extremeread',
		'https://lbmarshall.schoolloop.com/adminsupportstaff',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206405&vdid=i15d1ymabscv3dz',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206408&vdid=i1l5d1tymcv3en',
		'https://lbmarshall.schoolloop.com/MAAperformingarts',
		'https://lbmarshall.schoolloop.com/studentcouncil',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206444&vdid=i15d2io528kw9nj',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206428&vdid=h1i15dl1y8mcv3k4',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206431&vdid=ri1x5da1ymacv3kp',
		'https://lbmarshall.schoolloop.com/parentresources',
		'https://lbmarshall.schoolloop.com/staffresources',
		'https://lbmarshall.schoolloop.com/Math_Support',
		'https://lbmarshall.schoolloop.com/wrap',
		'https://www.lbschools.net/Departments/High-Schools/Pathways/',
		'https://lbmarshall.schoolloop.com/ELAC',
		'https://lbmarshall.schoolloop.com/parentinvolvement',
		'https://lbmarshall.schoolloop.com/pta',
		'https://lbmarshall.schoolloop.com/SSC',
		'https://lbmarshall.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206448&vdid=3i15d200cvjj',

		'https://lbmuir.schoolloop.com/principal',
		'https://lbmuir.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782207320&vdid=i10gc1ypj2mcn1mb',
		'https://lbmuir.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782207320&vdid=i10c1ymcn1mx',
		'https://lbmuir.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782207320&vdid=i1d0cp1ymcn1ne',
		'https://lbmuir.schoolloop.com/events',
		'https://lbmuir.schoolloop.com/dresscode',
		'https://lbmuir.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782207321&vdid=iw10xcv72p7144tb',
		'https://lbmuir.schoolloop.com/reportingperiods',
		'https://lbmuir.schoolloop.com/accountability',
		'https://lbmuir.schoolloop.com/emergency',
		'https://lbmuir.schoolloop.com/library',
		'https://lbmuir.schoolloop.com/programs',
		'https://lbmuir.schoolloop.com/excel',
		'https://lbmuir.schoolloop.com/multiage',
		'https://lbmuir.schoolloop.com/specialed',
		'https://lbmuir.schoolloop.com/WRAP',
		'https://lbmuir.schoolloop.com/tradexcel',
		'https://lbmuir.schoolloop.com/administration',
		'https://lbmuir.schoolloop.com/staff',
		'https://lbmuir.schoolloop.com/EDGE',
		'https://lbmuir.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1609230013221&vdid=i130c2otpa4qf',
		'https://lbmuir.schoolloop.com/EDGEPE',
		'https://lbmuir.schoolloop.com/sports',
		'https://lbmuir.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1611648775715&vdid=i10c2pkda4rw',
		'https://lbmuir.schoolloop.com/studentlinks',

		'https://na-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178973589&vdid=i189wapi1yu3o2ae',
		'https://na-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536391409741&vdid=i19a2dppv5pm',
		'https://na-lbusd-ca.schoolloop.com/bell_schedules',
		'https://na-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i19a2bee25c4',
		'https://na-lbusd-ca.schoolloop.com/calendar',
		'https://na-lbusd-ca.schoolloop.com/documentsforparents',
		'https://www.lbschools.net/Departments/Newsroom/article.cfm?articleID=2695',
		'https://na-lbusd-ca.schoolloop.com/library',
		'https://na-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536391409764&vdid=i19a23b8e74s',
		'https://na-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536391409777&vdid=i19a1yu3o2df',
		'https://na-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i19a2n0fo4abg',
		'https://www.lbschools.net/Departments/High-Schools/Pathways/',
		'https://na-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536391409778&vdid=i19a1y6u3o2e2',
		'https://na-lbusd-ca.schoolloop.com/Comprehensives',
		'https://na-lbusd-ca.schoolloop.com/SmallThematics',

		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995898834&vdid=i35c2vy6t12d',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995898834&vdid=i35c1yyk8yq',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995898834&vdid=i35c1yyk8z7',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995898834&vdid=i3o5cc1yyk8zn',
		'https://lbnewcomb.schoolloop.com/schoolmap',
		'https://lbnewcomb.schoolloop.com/Uniform',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899187&vdid=ic35qnc1yyk811m',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899187&vdid=bi352chq1yyk8122',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899187&vdid=yiu35c81yyck812j',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995900337&vdid=ir35c31yyik81di',
		'https://lbnewcomb.schoolloop.com/pres_message',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995900337&vdid=i35c2vbhpz147',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995900337&vdid=i3at5c2vglo18c',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995900138&vdid=i355c31y2yk819m',
		'https://lbnewcomb.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995900138&vdid=li35c1yyk81a8',
		'https://lbnewcomb.schoolloop.com/foundationevents',
		'https://lbnewcomb.schoolloop.com/ssc',
		'https://lbnewcomb.schoolloop.com/mssports',

		'https://lbpowell.schoolloop.com/ColinPowellBiographyLink',
		'https://lbpowell.schoolloop.com/schoolhistory',
		'https://lbpowell.schoolloop.com/dresscode',
		'https://lbpowell.schoolloop.com/bellschedules',
		'https://lbpowell.schoolloop.com/administrators',
		'https://lbpowell.schoolloop.com/specialistsandteachersupport',
		'https://lbpowell.schoolloop.com/officesupportstaff',
		'https://lbpowell.schoolloop.com/nursingservices',
		'https://lbpowell.schoolloop.com/elementary',
		'https://lbpowell.schoolloop.com/middleschool',
		'https://lbpowell.schoolloop.com/specialed',
		'https://lbpowell.schoolloop.com/nutrition',
		'https://lbpowell.schoolloop.com/physicalplant',
		'https://lbpowell.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995898986&vdid=ic720fx1yylh11e',

		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778444&vdid=i17e1ysecxfx',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778444&vdid=8ni17e1myecxgd',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778444&vdid=i17e91yiecxlf',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778444&vdid=i1777ed1yjecxnb',
		'https://lbrobinson.schoolloop.com/schoolcalendar',
		'https://lbrobinson.schoolloop.com/enrollment',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778444&vdid=i17e1tsyecxoq',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=i17e1y9ecxqp',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=i17e1mmy9fecxr5',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=4i17ea19yercxrn',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=i17e1eryetcxs3',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=iq17e1yenjcxsj',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=iv17e1ecy8ecxsz',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=i17e1yecxtf',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=iak17e1yvecxtv',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778477&vdid=i17be11yecxub',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778507&vdid=i017e19wytecxus',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778507&vdid=i1c7se1yef4cxvl',
		'https://lbrobinson.schoolloop.com/ROV',
		'https://lbrobinson.schoolloop.com/CollegePromise',
		'https://lbrobinson.schoolloop.com/WRAPRobinson',
		'https://lbrobinson.schoolloop.com/cotsenfoundation',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778649&vdid=id17e2lrn72dq',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778649&vdid=yi17e1yecx12e',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778649&vdid=i17e1yecx12t',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778649&vdid=i17e1yecx13f',
		'https://lbrobinson.schoolloop.com/cybersafety',
		'https://www.lbschools.net/Asset/files/District/Stay_in_the_Loop_EN.pdf',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778669&vdid=i1k7ded1ye8cx14c',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778669&vdid=ip17e19yecx151',
		'https://lbrobinson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605778669&vdid=i17one20r0w1jw',

		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177427&vdid=5i13by1ymbyod',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177427&vdid=qi13b1ymbyot',
		'https://lbrogers.schoolloop.com/generalinformation',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177427&vdid=i13kb1dhnymbypt',
		'https://lbrogers.schoolloop.com/schoolculture',
		'https://lbrogers.schoolloop.com/yearbooks',
		'https://lbrogers.schoolloop.com/8thgrade',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177427&vdid=i91l3hxb1ymbytn',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177427&vdid=i913b1yqmbyu5',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177449&vdid=i13b1ymbyvd',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177449&vdid=i13b1ymbyvt',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177449&vdid=i13b1zzg9ab7',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177449&vdid=i13b1uyvm7byx5',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178974394&vdid=5i13b2kwht395q2c',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177460&vdid=i13b1ymbyxm',
		'https://lbrogers.schoolloop.com/elac',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177460&vdid=id13b1quymbyym',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177482&vdid=iyb13bd1ymby10z',
		'https://lbrogers.schoolloop.com/health',
		'https://lbrogers.schoolloop.com/history',
		'https://lbrogers.schoolloop.com/english',
		'https://lbrogers.schoolloop.com/math',
		'https://lbrogers.schoolloop.com/science',
		'https://lbrogers.schoolloop.com/specialeducation',
		'https://lbrogers.schoolloop.com/electives',
		'https://lbrogers.schoolloop.com/coding',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177507&vdid=i139b1soymby18i',
		'https://lbrogers.schoolloop.com/debate',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177507&vdid=ixf13bi25xwjt886',
		'https://lbrogers.schoolloop.com/globalclassroom',
		'https://lbrogers.schoolloop.com/psychology',
		'https://lbrogers.schoolloop.com/greenteam',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177507&vdid=i13bb1uymby19w',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177507&vdid=i1y3ib19ym7by1b2',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177507&vdid=i1e35bc1ymoby1am',
		'https://lbrogers.schoolloop.com/marinebiology',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177507&vdid=i13b1ymby1bm',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177507&vdid=i13b25wjt8df',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177518&vdid=i13b1ymby1cp',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177518&vdid=iy13b2e7gm75w',
		'https://lbrogers.schoolloop.com/acapellaclub',
		'https://lbrogers.schoolloop.com/africanamericancultureclub',
		'https://lbrogers.schoolloop.com/artclub',
		'https://lbrogers.schoolloop.com/asianamericanheritageclub',
		'https://lbrogers.schoolloop.com/cjsf',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177537&vdid=i13b2b6kzb2e',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177537&vdid=i13b1ymby1db',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177537&vdid=4ir13b2nb6kzb2w',
		'https://lbrogers.schoolloop.com/esports',
		'https://lbrogers.schoolloop.com/fingersoffury',
		'https://lbrogers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782177537&vdid=i13b2dpq88kb',
		'https://lbrogers.schoolloop.com/lgbtqia',
		'https://lbrogers.schoolloop.com/literaryclub',
		'https://lbrogers.schoolloop.com/movieclub',
		'https://lbrogers.schoolloop.com/mylittlemustangs',
		'https://lbrogers.schoolloop.com/rogersmusicclub',
		'https://lbrogers.schoolloop.com/socialclub',
		'https://lbrogers.schoolloop.com/tradingcardgame',
		'https://lbrogers.schoolloop.com/library',

		'https://lbstanford.schoolloop.com/dress',
		'https://lbstanford.schoolloop.com/bells',
		'https://lbstanford.schoolloop.com/library',
		'https://lbstanford.schoolloop.com/mission',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899090&vdid=i142f4w1yyld11a',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899090&vdid=i12fk3d13r962k',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899120&vdid=i12f1yyld175',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899130&vdid=i1r2f1yyld185',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899134&vdid=i12f313r964l',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899120&vdid=i12fyn3q1g3r9641',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899130&vdid=i1r2f1yyld185',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899130&vdid=i12f1yhyjld190',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899130&vdid=i1vw2fb1yy8ld19o',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899130&vdid=i12f1yyld1af',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899130&vdid=i12f1yyld1d3',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899134&vdid=i12f313r964l',
		'https://lbstanford.schoolloop.com/hs_info',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899134&vdid=5i12qdf1jyyld1bq',
		'https://lbstanford.schoolloop.com/acronyms',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899169&vdid=i12hf1yiyld1fq',
		'https://lbstanford.schoolloop.com/cc',
		'https://lbstanford.schoolloop.com/contacts',
		'https://lbstanford.schoolloop.com/forms',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899188&vdid=2i12yf1yyld1jg',
		'https://lbstanford.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i12f1z8jala',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899169&vdid=i12wfp3136r9667',
		'https://lbstanford.schoolloop.com/ssc',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515382155&vdid=ie12f3x13hxr95or',
		'https://lbstanford.schoolloop.com/Bestfriends',
		'https://lbstanford.schoolloop.com/cjsf',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956399863&vdid=i12f31iu3r950g',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956399863&vdid=i12f3133r95lf',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956399863&vdid=i128of3j13r95mf',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956399863&vdid=iq12f31l3gkr94y5',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956399863&vdid=bi12sf313ur952b',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956399863&vdid=i12f313r95nz',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956399863&vdid=i1u24f313er9518',
		'https://lbstanford.schoolloop.com/gate',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178974587&vdid=i1f2f231i3r94uh',
		'https://lbstanford.schoolloop.com/cheer',
		'https://lbstanford.schoolloop.com/studentcouncil',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956385871&vdid=ir12mf313r93tr',
		'https://lbstanford.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1643956385871&vdid=id12f3s51x3r93nk',

		'https://lbstephens.schoolloop.com/Admin',
		'https://lbstephens.schoolloop.com/teachers',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995900066&vdid=i1w9f1jyfyle2b1',
		'https://lbstephens.schoolloop.com/English',
		'https://docs.google.com/document/d/1rNp_q9iF5ADMg1ode4-dWZ1pINCEMeUMSwwxIpAgt0Q/edit?usp=sharing',
		'https://lbstephens.schoolloop.com/Math',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995901333&vdid=i19f1yyle2dj',
		'https://docs.google.com/document/d/1rNp_q9iF5ADMg1ode4-dWZ1pINCEMeUMSwwxIpAgt0Q/edit?usp=sharing',
		'https://lbstephens.schoolloop.com/Science',
		'https://lbstephens.schoolloop.com/history',
		'https://docs.google.com/document/d/1rNp_q9iF5ADMg1ode4-dWZ1pINCEMeUMSwwxIpAgt0Q/edit?usp=sharing',
		'https://lbstephens.schoolloop.com/PE',
		'https://lbstephens.schoolloop.com/SPED',
		'https://docs.google.com/document/d/1rNp_q9iF5ADMg1ode4-dWZ1pINCEMeUMSwwxIpAgt0Q/edit?usp=sharing',
		'https://lbstephens.schoolloop.com/GATE',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995905951&vdid=ri19f1yykle2me',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995906955&vdid=s6i19f1yyle2nv',
		'https://docs.google.com/document/d/1rNp_q9iF5ADMg1ode4-dWZ1pINCEMeUMSwwxIpAgt0Q/edit?usp=sharing',
		'https://www.surveymonkey.com/r/28YMYV5',
		'https://lbstephens.schoolloop.com/behavior',
		'https://lbstephens.schoolloop.com/bell',
		'https://lbstephens.schoolloop.com/BusSafety',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899346&vdid=ti19f1yyle221',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899346&vdid=1i19f1yysle22k',
		'https://lbstephens.schoolloop.com/charactercounts',
		'https://lbstephens.schoolloop.com/counsel',
		'https://lbstephens.schoolloop.com/earth',
		'https://lbstephens.schoolloop.com/firedrill',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899346&vdid=if169jf1ygyle25e',
		'https://lbstephens.schoolloop.com/map',
		'https://lbstephens.schoolloop.com/nurse',
		'https://lbstephens.schoolloop.com/policies',
		'https://lbstephens.schoolloop.com/acctreport',
		'https://lbstephens.schoolloop.com/library',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899346&vdid=kxi19f1yayle296',
		'https://docs.google.com/document/d/1rNp_q9iF5ADMg1ode4-dWZ1pINCEMeUMSwwxIpAgt0Q/edit?usp=sharing',
		'https://lbstephens.schoolloop.com/Parents',
		'https://lbstephens.schoolloop.com/hschoiceparents',
		'https://lbstephens.schoolloop.com/ptaabout',
		'https://lbstephens.schoolloop.com/vips',
		'https://www.lbschools.net/parentvue',
		'https://docs.google.com/document/d/1rNp_q9iF5ADMg1ode4-dWZ1pINCEMeUMSwwxIpAgt0Q/edit?usp=sharing',
		'https://lbstephens.schoolloop.com/cjsf',
		'https://lbstephens.schoolloop.com/ASB',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908074&vdid=iv1934f1yyxle2tf',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908074&vdid=9sci19fm1yyle2tv',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908074&vdid=i1u9f1yyle2ua',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908074&vdid=i19f1yyle2up',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908074&vdid=i19f1yyqle2v4',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908917&vdid=i19f1ryyle2vk',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908074&vdid=i19f1yuyle2w0',
		'https://lbstephens.schoolloop.com/afterschool',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995908074&vdid=i19fu1yyle2xb',
		'https://lbstephens.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515994534&vdid=i19f5e2m00dq2rl',

		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899211&vdid=i24c22pi3v6c',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899211&vdid=i24c3i2os2ne50b',
		'https://lbtincher.schoolloop.com/office',
		'https://sites.google.com/lbschools.net/tincherpreparatoryfacts/home',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899211&vdid=i24c2y9fc641',
		'https://lbtincher.schoolloop.com/counselingprogram',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899276&vdid=pisr24c2p8d7d5o0',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899276&vdid=io24c1yiyk6hi',
		'https://lbtincher.schoolloop.com/academicskills',
		'https://lbtincher.schoolloop.com/selskills',
		'https://lbtincher.schoolloop.com/collegeandcareer',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1609230912416&vdid=i24c2pafj4pc',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1609230912416&vdid=3i264cj42ph1u614',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1609230912416&vdid=i24cf2p87d6gx',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1609230912416&vdid=i2k4c2ph1u61z',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1609230912416&vdid=ti24cc2ph1u63m',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899062&vdid=i24c2xcvy6ti5k',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899062&vdid=i24c2iaop8j5h8',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899062&vdid=i247c2ovyf6tey9',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899062&vdid=i24c1yyk68z',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899086&vdid=i274c02oqer5o5',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899086&vdid=i24c2gv4y6thka',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899086&vdid=i24c62vrm12lci',
		'https://lbtincher.schoolloop.com/teachers',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899127&vdid=i2o4c2oqer5qs',
		'https://lbtincher.schoolloop.com/electives',
		'https://lbtincher.schoolloop.com/clubs',
		'https://lbtincher.schoolloop.com/hsreadiness',
		'https://lbtincher.schoolloop.com/Library',
		'https://lbtincher.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971841&vdid=i24c2pmm257v',
		'https://lbtincher.schoolloop.com/ptamain',
		'https://lbtincher.schoolloop.com/contact',
		'https://lbtincher.schoolloop.com/ptaprograms',
		'https://lbtincher.schoolloop.com/ptafundraising',
		'https://lbtincher.schoolloop.com/ptavolunteering',

		'https://lbwashington.schoolloop.com/bellschedule',
		'https://lbwashington.schoolloop.com/staff',
		'https://lbwashington.schoolloop.com/contact',
		'https://lbwashington.schoolloop.com/partners',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899174&vdid=i350teq1yyl5uo',
		'https://lbwashington.schoolloop.com/guidelines_for_success',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899441&vdid=ia35en1yhmyl511z',
		'https://lbwashington.schoolloop.com/math',
		'https://lbwashington.schoolloop.com/history',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899441&vdid=i351eh2flvi04qf',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899441&vdid=iu35qex22xwig6oc',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899441&vdid=i35e20fw4kk19x',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899441&vdid=i35e2fwkk17y',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899441&vdid=i47335e1ymyl514r',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899441&vdid=i35e2fwkkk1cl',
		'https://sites.google.com/a/lbschools.net/wms-library/home',
		'https://lbwashington.schoolloop.com/HSSchoolChoice',
		'https://lbwashington.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995899832&vdid=iaw35e1yyrl517h',
		'https://lbwashington.schoolloop.com/ssc',
		'https://lbwashington.schoolloop.com/wrap',
		'https://lbwashington.schoolloop.com/community',
		'https://lbwashington.schoolloop.com/career',
		'https://lbwashington.schoolloop.com/gate',
		'https://lbwashington.schoolloop.com/sports',
		'https://lbwashington.schoolloop.com/materials',
		'https://lbwashington.schoolloop.com/synergy',
		'https://lbschools.instructure.com/courses/16155',
	]
	mainfolder = 'schoolloop'
	school_name = 'schoolloop'
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
