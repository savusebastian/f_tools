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
		'https://add-lbusd.ca.schoolloop.com/visionandmission',
		'https://add-lbusd.ca.schoolloop.com/janeaddams',
		'https://add-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863794&vdid=i633icc1z1sh24l',
		'https://add-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863794&vdid=ib3k3vtc1z1sh253',
		'https://add-lbusd.ca.schoolloop.com/principal',
		'https://add-lbusd.ca.schoolloop.com/assistantprincipal',
		'https://add-lbusd.ca.schoolloop.com/supportstaff',
		'https://add-lbusd.ca.schoolloop.com/officestaff',
		'https://add-lbusd.ca.schoolloop.com/recreationstaff',
		'https://add-lbusd.ca.schoolloop.com/teachers',
		'https://add-lbusd.ca.schoolloop.com/gate',
		'https://add-lbusd.ca.schoolloop.com/music',
		'https://add-lbusd.ca.schoolloop.com/wrap',
		'https://add-lbusd.ca.schoolloop.com/kindergarten',
		'https://add-lbusd.ca.schoolloop.com/1stgrade',
		'https://add-lbusd.ca.schoolloop.com/2ndgrade',
		'https://add-lbusd.ca.schoolloop.com/3rdgrade',
		'https://add-lbusd.ca.schoolloop.com/4thgrade',
		'https://add-lbusd.ca.schoolloop.com/5thgrade',
		'https://add-lbusd.ca.schoolloop.com/parentresources',
		'https://add-lbusd.ca.schoolloop.com/communityresources',
		'https://add-lbusd.ca.schoolloop.com/parentcenter',
		'https://add-lbusd.ca.schoolloop.com/workshops',
		'https://add-lbusd.ca.schoolloop.com/events',
		'https://add-lbusd.ca.schoolloop.com/newsarchive',

		'https://alvarado-lbusd-ca.schoolloop.com/vision',
		'https://alvarado-lbusd-ca.schoolloop.com/bellsched',
		'https://alvarado-lbusd-ca.schoolloop.com/rules',
		'https://alvarado-lbusd-ca.schoolloop.com/Curriculum',
		'https://alvarado-lbusd-ca.schoolloop.com/charactered',
		'https://alvarado-lbusd-ca.schoolloop.com/supportstaff',
		'https://alvarado-lbusd-ca.schoolloop.com/teachingstaff',
		'https://alvarado-lbusd-ca.schoolloop.com/emergency',
		'https://alvarado-lbusd-ca.schoolloop.com/calendar',
		'https://alvarado-lbusd-ca.schoolloop.com/grade3_5math',
		'https://alvarado-lbusd-ca.schoolloop.com/studentwebsites',
		'https://alvarado-lbusd-ca.schoolloop.com/TeacherResources',
		'https://alvarado-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972398&vdid=i3f5wb2k6fv091hy',

		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863796&vdid=i35c1z1sh10p',
		'https://barton-lbusd-ca.schoolloop.com/principal_message',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863796&vdid=il35c28dhx12h',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863796&vdid=i35yc28dhx1c3',
		'https://barton-lbusd-ca.schoolloop.com/safetyuniform',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863808&vdid=i735ruc288k4h1d4',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863808&vdid=ip35c28dihx1g3',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863808&vdid=i35c28dhx1mr',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863808&vdid=ibgb35c258dhx1nk',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863808&vdid=ik35c28dhx1mb',
		'https://barton-lbusd-ca.schoolloop.com/positive',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863821&vdid=i35c28ydhx15g',
		'https://barton-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863821&vdid=i35c28dhx15k',
		'https://barton-lbusd-ca.schoolloop.com/friendsofbarton',
		'https://barton-lbusd-ca.schoolloop.com/ptt',
		'https://barton-lbusd-ca.schoolloop.com/library',
		'https://barton-lbusd-ca.schoolloop.com/parent_resources',
		'https://barton-lbusd-ca.schoolloop.com/sbac',
		'https://barton-lbusd-ca.schoolloop.com/student_resources',
		'https://barton-lbusd-ca.schoolloop.com/teacherresources',
		'https://barton-lbusd-ca.schoolloop.com/valuesinaction',

		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824488&vdid=i617w8a1fyb2f1bw',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824488&vdid=jji18al2wddpjaos',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=ii18a20yrcsr41',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824488&vdid=i185a1yb2f1cc',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824488&vdid=i18ahb1yb2f1cr',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824488&vdid=il18ar1ymnb2f1d7',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824490&vdid=i18b9ga1ybp2f1ee',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824490&vdid=i18a1eyb42f1dq',
		'https:/hd-lbusd-ca.schoolloop.com',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824493&vdid=i18a1dyb2f1ex',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824494&vdid=i18a1ybq2f1ff',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824494&vdid=i18a1yb2f1fv',
		'https://birney-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535349824494&vdid=i18a1yb2f1gb',
		'https://birney-lbusd-ca.schoolloop.com/BirneyPTA',
		'https://birney-lbusd-ca.schoolloop.com/BeeMember',
		'https://birney-lbusd-ca.schoolloop.com/PTABoardMembers',
		'https://birney-lbusd-ca.schoolloop.com/fundraisers',
		'https://birney-lbusd-ca.schoolloop.com/EventsActivities',
		'https://birney-lbusd-ca.schoolloop.com/Kudos',

		'https://bixby-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863845&vdid=ci23ah1z1shqh',
		'https://bixby-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863865&vdid=i23a1z1yshsi',

		'https://bry-lbusd.ca.schoolloop.com/about',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456393&vdid=ih33e2avhj6j0',
		'https://bry-lbusd.ca.schoolloop.com/map',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456393&vdid=iy3c3eg2ywdpj50g',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456393&vdid=iu33e16qwkydpe',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456393&vdid=3i33fe1wkiydpu',
		'https://bry-lbusd.ca.schoolloop.com/adminstaff',
		'https://bry-lbusd.ca.schoolloop.com/teachers',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456396&vdid=i33e1wkyds7',
		'https://www.lbschools.net/Departments/Newsroom/article.cfm?articleID=2908',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456396&vdid=ia3t3e2lz98ey6tz',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456396&vdid=i633el62rcsg6f4',
		'https://bry-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380456396&vdid=i33ev30674hw26c',
		'https://bry-lbusd.ca.schoolloop.com/stmath',

		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863905&vdid=ji1y0e1z71sh1dc',
		'https://bbk-lbusd.ca.schoolloop.com/schoolhistory',
		'https://bbk-lbusd.ca.schoolloop.com/lutherburbankbio',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863905&vdid=i1e0e1z1sh1dt',
		'https://bbk-lbusd.ca.schoolloop.com/uniformpolicy',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863905&vdid=4i104ek1z1sh1fq',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863905&vdid=ciy10e1zu1sh1g8',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863908&vdid=v3qi107e1z1sh1h8',
		'https:/www.groundeducation.org',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863908&vdid=i10e1z1sh1jp',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863910&vdid=iiu10em1z1ysh1kc',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863910&vdid=i10e32msg0m18c0',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863917&vdid=iq10e1z1fsh1lz',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863917&vdid=i910e1z1sh1mk',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863920&vdid=ij10e1z41sh1n9',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863920&vdid=i10e1z1ocs1sh1nq',
		'https://bbk-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863920&vdid=i10e1z31sh1o6',

		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863897&vdid=i37b91z1sh1fh',
		'https://lbburcham.schoolloop.com/elembellschedule',
		'https://lbburcham.schoolloop.com/menu',
		'https://lbburcham.schoolloop.com/elemschoolstaff',
		'https://lbburcham.schoolloop.com/Officedirectory',
		'https://lbburcham.schoolloop.com/Programs',
		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864149&vdid=ir37jb1z1sh1to',
		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864149&vdid=it3u7b1z1j9sh1u9',
		'https://lbburcham.schoolloop.com/pta',
		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864168&vdid=i07379b1z1jsh1vc',
		'https://lbburcham.schoolloop.com/PTAnewsletter',
		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864192&vdid=i37b1z1sh1wc',
		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864193&vdid=i137gb1inz1sh1ws',
		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864193&vdid=i137ba1z1sh1xg',
		'https://lbburcham.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864193&vdid=i371b1dkz1sh1y1',
		'https://lbburcham.schoolloop.com/typing',

		'https://carver-lbusd-ca.schoolloop.com/about',
		'https://carver-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863875&vdid=i11a1z1shft',
		'https://carver-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863875&vdid=i111a2o4b5y148',
		'https://carver-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863885&vdid=i11a1z1shgb',
		'https://carver-lbusd-ca.schoolloop.com/Staff',
		'https://carver-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863915&vdid=i11a1z1shhv',
		'https://carver-lbusd-ca.schoolloop.com/ptabulletinboard',
		'https://carver-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427863915&vdid=i11a2a1g5fe',
		'https://carver-lbusd-ca.schoolloop.com/CDC',
		'https://carver-lbusd-ca.schoolloop.com/studentlinks',
		'https://carver-lbusd-ca.schoolloop.com/klinks',
		'https://carver-lbusd-ca.schoolloop.com/first',
		'https://carver-lbusd-ca.schoolloop.com/second',
		'https://carver-lbusd-ca.schoolloop.com/third',
		'https://carver-lbusd-ca.schoolloop.com/fourth',
		'https://carver-lbusd-ca.schoolloop.com/fifth',

		'https://chavez-lbusd-ca.schoolloop.com/ourschool',
		'https://chavez-lbusd-ca.schoolloop.com/kindergarten',
		'https://chavez-lbusd-ca.schoolloop.com/kindergarten',
		'https://chavez-lbusd-ca.schoolloop.com/1stgrade',
		'https://chavez-lbusd-ca.schoolloop.com/2ndgrade',
		'https://chavez-lbusd-ca.schoolloop.com/3rdgrade',
		'https://chavez-lbusd-ca.schoolloop.com/4thgrade',
		'https://chavez-lbusd-ca.schoolloop.com/5thgrade',
		'https://chavez-lbusd-ca.schoolloop.com/support',
		'https://chavez-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864048&vdid=i1s3b1z1sh20x',
		'https://chavez-lbusd-ca.schoolloop.com/tcc',
		'https://chavez-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864059&vdid=ii1a3b13z1sh23n',
		'https://chavez-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178974499&vdid=i13fb2o5y626xo',
		'https://chavez-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864067&vdid=i13bp2q28n7ki',
		'https://chavez-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864067&vdid=i13b2wq8vtg8wt',
		'https://chavez-lbusd-ca.schoolloop.com/resources',
		'https://chavez-lbusd-ca.schoolloop.com/attendance',

		'https://chavez-lbusd-ca.schoolloop.com/childnet',

		'https://cleveland-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864029&vdid=ik35b1vz21sh1pa',
		'https://cleveland-lbusd-ca.schoolloop.com/about',
		'https://cleveland-lbusd-ca.schoolloop.com/bellschedule',
		'https://cleveland-lbusd-ca.schoolloop.com/map',
		'https://cleveland-lbusd-ca.schoolloop.com/SafenCivil',
		'https://cleveland-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864029&vdid=i35d4b2l8rt204',
		'https://cleveland-lbusd-ca.schoolloop.com/support',
		'https://cleveland-lbusd-ca.schoolloop.com/ATLAS',
		'https://cleveland-lbusd-ca.schoolloop.com/kidsclub',
		'https://cleveland-lbusd-ca.schoolloop.com/specialeducation1',
		'https://cleveland-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864031&vdid=ii635b1z1wsh1u5',
		'https://cleveland-lbusd-ca.schoolloop.com/WRAP',
		'https://cleveland-lbusd-ca.schoolloop.com/admin',
		'https://cleveland-lbusd-ca.schoolloop.com/preppyk1',
		'https://cleveland-lbusd-ca.schoolloop.com/kindergarten',
		'https://cleveland-lbusd-ca.schoolloop.com/Firstgrade',
		'https://cleveland-lbusd-ca.schoolloop.com/secondgrade',
		'https://cleveland-lbusd-ca.schoolloop.com/thirdgrade',
		'https://cleveland-lbusd-ca.schoolloop.com/fourthfifth',
		'https://cleveland-lbusd-ca.schoolloop.com/specialeducation',
		'https://cleveland-lbusd-ca.schoolloop.com/officestaff',

		'https://dooley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864051&vdid=i3655ab1z1gsh21t',
		'https://dooley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864045&vdid=i35b2v7of16c',
		'https://dooley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864052&vdid=i3u5b1kz1sh22n',
		'https://dooley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864053&vdid=i3y5b1z1sh235',
		'https://dooley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864057&vdid=oid35b1z1sh23p',
		'https://dooley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864057&vdid=i35b1z1sh24a',
		'https://dooley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972173&vdid=i35b1z1sh215',

		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113168&vdid=i9e1fy03k80',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113168&vdid=bi92eql1y03k8h',
		'https://edi-lbusd.ca.schoolloop.com/learninggarden',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113168&vdid=iq9ge18y03k9g',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113168&vdid=i89e1yso03kae',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113187&vdid=i9e1y0ipbk3kfq',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113189&vdid=ic9e1y03kh5',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113198&vdid=i9e1y03kjj',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=i9e1y03kaw',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=fi9e1y0m3kbc',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=ui9e1y03kbs',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=i9qe1y0q3kc8',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=i9e1kyy03kco',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=i9e1y03kd4',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=i9ke1y103kdk',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=i9xe1ye03ke4',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=il9geuh1y03ken',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113177&vdid=i9e1y03kf9',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113190&vdid=i9e1yy103khn',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113190&vdid=i9e1ty03ki3',
		'https://edi-lbusd.ca.schoolloop.com/studentresources',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113190&vdid=i9e1y0p3kj2',
		'https://edi-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404113188&vdid=3i9e1yd0h3kgo',

		'https://eme-lbusd.ca.schoolloop.com/principalsmessage',
		'https://eme-lbusd.ca.schoolloop.com/guidelines',
		'https://eme-lbusd.ca.schoolloop.com/programs',
		'https://eme-lbusd.ca.schoolloop.com/baldridge',
		'https://eme-lbusd.ca.schoolloop.com/song',
		'https://eme-lbusd.ca.schoolloop.com/honoraward',
		'https://eme-lbusd.ca.schoolloop.com/contact',
		'https://eme-lbusd.ca.schoolloop.com/pta',
		'https://eme-lbusd.ca.schoolloop.com/parent',
		'https://eme-lbusd.ca.schoolloop.com/foundation',
		'https://eme-lbusd.ca.schoolloop.com/menu',
		'https://eme-lbusd.ca.schoolloop.com/readinglist',
		'https://eme-lbusd.ca.schoolloop.com/counsel',
		'https://eme-lbusd.ca.schoolloop.com/mathlang',
		'https://eme-lbusd.ca.schoolloop.com/kinder',
		'https://eme-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536391371763&vdid=43ti35a278al5c4',

		'https://fre-lbusd.ca.schoolloop.com/principal',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864534&vdid=i16e1z1ssh1ae',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864534&vdid=ime1n6e1z1sh1av',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864534&vdid=i10r6e1z1sh1bb',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864534&vdid=ik716ee1z51sh1br',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864534&vdid=sig16e1mz1sh1cg',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864571&vdid=i168e1z1sh1d0',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864587&vdid=i196e1lz1sh1dh',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864587&vdid=i16e1z1sh1e1',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864633&vdid=i16l2e15z1sh1er',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864633&vdid=i16e1z1sh1f8',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864633&vdid=i16e1xz1sh1fo',
		'https://fre-lbusd.ca.schoolloop.com/technology',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864664&vdid=i1h6e1zt1sh1h3',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864620&vdid=abi1y6se1z1sh1i4',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864620&vdid=i1b6e1z1sh1ik',
		'https://fre-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864732&vdid=i1ly6e1z1sh1jp',

		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864539&vdid=i126fe1z01sh1x4',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864539&vdid=i1vk2re1z1sh1y3',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864539&vdid=i12e1z1sh1yl',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864539&vdid=ir12ep1z418sh1z8',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864539&vdid=i1e2eh14z1sh1zx',
		'https://gant-lbusd-ca.schoolloop.com/bell-schedule',
		'https://gant-lbusd-ca.schoolloop.com/uniforms',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864556&vdid=idkj12e1z1sh21o',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864556&vdid=i12e1wz41sh22p',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864556&vdid=9i122e29sn8j42nf',
		'https://gant-lbusd-ca.schoolloop.com/green-team',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864556&vdid=i12ye2b7d9i4er',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864556&vdid=i123e0y1nz1sh239',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864556&vdid=i12e29lw64if',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864576&vdid=i12tce1kz1sh23s',
		'https://gant-lbusd-ca.schoolloop.com/pta',
		'https://gant-lbusd-ca.schoolloop.com/pta-membership',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864576&vdid=i1o2e1z1jsh25l',
		'https://gant-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864613&vdid=i12e1z1sh263',

		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864639&vdid=i16a1z1shzk',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864639&vdid=i7w16ra1z01sh101',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864639&vdid=ci16ya1z1sh10i',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864639&vdid=i16a14z1sh110',
		'https://garfield-lbusd-ca.schoolloop.com/supportstaff',
		'https://garfield-lbusd-ca.schoolloop.com/uniformpolicy',
		'https://garfield-lbusd-ca.schoolloop.com/ELAC',
		'https://garfield-lbusd-ca.schoolloop.com/SSC',
		'https://garfield-lbusd-ca.schoolloop.com/PTK',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864702&vdid=fi16ya1z1ksh14h',
		'https://garfield-lbusd-ca.schoolloop.com/websites',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864726&vdid=i1v6a1zx16sh167',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1645244247160&vdid=i16a31kikba257b',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864802&vdid=ji16a1z1sh178',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864802&vdid=w1i16ba1z1sh17q',
		'https://garfield-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864802&vdid=if126a1z1sh188',

		'https://lbgompers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205668&vdid=i14f1ymvdrkp',
		'https://lbgompers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782205918&vdid=ia14f1bymdrjo',
		'https://lbgompers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206087&vdid=i14pfo1u2ymdrk7',
		'https://lbgompers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782206316&vdid=i14f1gymadrl8',
		'https://lbgompers.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535782207813&vdid=i1e4f1ymdrnb',
		'https://lbgompers.schoolloop.com/resources',

		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864562&vdid=i33d1z1sha8',
		'https://gra-lbusd.ca.schoolloop.com/principal',
		'https://gra-lbusd.ca.schoolloop.com/bell',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864568&vdid=i3c3dl1iz1shca',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864568&vdid=vi33df1z1shbs',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864568&vdid=i33d1z1shcw',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864574&vdid=if33d1z31shde',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864580&vdid=i33d41uz12sher',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864591&vdid=i4313d1z14shfr',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864591&vdid=iro3f3d1z1jshgp',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864591&vdid=i33d1z1shfa',
		'https://gra-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864591&vdid=xi33cd1z1shk2',

		'https://harte-lbusd-ca.schoolloop.com/contact',
		'https://harte-lbusd-ca.schoolloop.com/principal',
		'https://calendar.google.com/calendar/u/0?cid=Y185Y3JhY2MzOW1tNXI2YnE5ZXE2dXA5bnZkMEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=id1l3ch2p0fc2d3',
		'https://harte-lbusd-ca.schoolloop.com/bellschedule',
		'https://harte-lbusd-ca.schoolloop.com/schooluniforms',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864581&vdid=i137ac1z215shj3',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864581&vdid=i13c1z1shjr',
		'https://harte-lbusd-ca.schoolloop.com/library',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i13cg2pckf2ff',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i1mh3c42p6ckf2nl',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864593&vdid=vi1h3cd2pb3q52r9',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i13c2p4sg2fv',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i1e3cl2p1t3q529w',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=yi135c2pckf2ce',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864600&vdid=i13c1z1sho5',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864583&vdid=6i13c21nbl1yv',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1605257076533&vdid=iyp1i3c2o1yq2ia',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864604&vdid=i143c1z1shos',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864608&vdid=i1x31c1zyb1shpb',
		'https://harte-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864601&vdid=ir13c2oy6r294',

		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971526&vdid=i7d1z1sh8w',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864827&vdid=it7d1z1shbs',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864745&vdid=i7d1z1sh9e',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864937&vdid=i7d1z1shdi',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864937&vdid=i7d1z1shcs',
		'https://docs.google.com/document/d/10kyrK6KYh7IEin0Aw5hngPA8HpK7KguhAgcXbvWT3Io/edit?usp=sharing',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864701&vdid=i7r3kd1z1sh9u',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864701&vdid=vi7td2pcrko1ug',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864701&vdid=i7d41z1shb4',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864701&vdid=ci7d2pkdnezp',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864701&vdid=i7d1zw3b1shaj',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864701&vdid=i7d2pjae1br',
		'https:/docs.google.com/document/d/1nw0o5ppij0l-7_gnki1nbyxtohuhbcjw1cktm69hqyq/edit?usp=sharing',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427865062&vdid=i7d1z1shfm',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178971526&vdid=ina7d30r5q1qh',
		'https://henry-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1598173067412&vdid=i7d2pdne7i',

		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864586&vdid=i145kd14z1sh1k2',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864586&vdid=i15d1z1sh1kl',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864586&vdid=i15d10zc1sh1l0',
		'https://hol-lbusd.ca.schoolloop.com/bellschedule',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864586&vdid=mi15d1az1sh1lx',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864595&vdid=i15d1z1sh1me',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864595&vdid=ie15hde1zn1sh1mv',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864595&vdid=i15d1z1sh1na',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864618&vdid=si15hd1z1sh1t8',

		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=i1f5db1z1nsh1p2',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=i15d1z1sh1pk',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=qai15d1z1lsh1q3',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=i156d1z5s1sh1qm',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=0i15d1z1sh1r5',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=i15d1z1m4sh1ro',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=i15od1z1tsh1s7',
		'https://hol-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537427864615&vdid=i15d1z1sh1sq',

		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161783&vdid=qit16c2kkdf5is',
		'https://lbhudson.schoolloop.com/mission',
		'https://lbhudson.schoolloop.com/hawkpledge',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161783&vdid=i146c2mlwmh1z0',
		'https://lbhudson.schoolloop.com/behaviorstandards',
		'https://lbhudson.schoolloop.com/bellschedule',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161783&vdid=i16c1y198b1',
		'https://lbhudson.schoolloop.com/hudsonmap',
		'https://lbhudson.schoolloop.com/history',
		'https://lbhudson.schoolloop.com/elizabethhudson',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161787&vdid=i16c1y198d7',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161787&vdid=ci16cu1y198dn',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161787&vdid=i16c1yp198e3',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161787&vdid=i164c21l4y198ej',
		'https://lbhudson.schoolloop.com/elementarymusic',
		'https://lbhudson.schoolloop.com/visualarts',
		'https://lbhudson.schoolloop.com/highschoolchoice',
		'mailto:alancaster@lbschools.net'
		'https://www.lbschools.net/parentvue',
		'https://www.lbschools.net/Departments/Research/parent_vue.cfm',
		'https://lbhudson.schoolloop.com/portal/login',
		'https://www.lbschools.net',
		'https://www.lbschools.net/Departments/Nutrition_Services/menu_nutrient_info.cfm',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161789&vdid=i16c1y198iq',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161789&vdid=i16c21j2zx1df',
		'https://lbhudson.schoolloop.com/parentguidelines',
		'https://lbhudson.schoolloop.com/parents',
		'https://lbhudson.schoolloop.com/homework',
		'https://lbhudson.schoolloop.com/hudsonmap',
		'https://lbhudson.schoolloop.com/ccs',
		'https://lbhudson.schoolloop.com/safeplace',
		'https://lbhudson.schoolloop.com/titleix',
		'https://lbhudson.schoolloop.com/uniformcomplaint',
		'https://www.lbschools.net/Departments/Parent_U/vips.cfm',
		'https://lbschools.instructure.com',
		'https://studentlbusd.lbschools.net/LoginPolicy.jsp',
		'https://lbhudson.schoolloop.com/portal/login',
		'https://www.lbschools.net/studentvue',
		'https://accounts.google.com',
		'https://www.lbschools.net',
		'https://lbhudson.schoolloop.com/calendar',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161791&vdid=ia16c2jt2zx1f5',
		'https://lbhudson.schoolloop.com/elementary',
		'https://lbhudson.schoolloop.com/onlineresources',
		'https://quizlet.com',
		'https://www.lbschools.net/Departments/OMS/homework_helpline.cfm',
		'https://lbhudson.schoolloop.com/Math_Support',
		'https://www.longbeach.gov/library/locations/harte',
		'https://mylbusd.lbschools.net/LoginPolicy.jsp',
		'https://lbschools.instructure.com',
		'https://accounts.google.com',
		'https://outlook.lbschools.net',
		'https%3A%2F%2Fclever.com%2Fin%2Fauth_callback&response_type=code&state=27ffa9d5488e57a2778fba984f01b0ce61740295212d3f3938ffb319be69554e&district_id=5123f61b95f100c94e000001',
		'https://synergy.lbschools.net',
		'https://lroix.lbschools.net/Account/Login?ReturnUrl=%2fHome%2f',
		'https://asp.schoolmessenger.com/lbusd/index.php?',
		'https://adminweb.aesoponline.com/access',
		'https://lbhudson.schoolloop.com/portal/login',
		'https://app.peardeck.com/authPicker?finalDestinationUrl=%2Fhome%2F%3Faction%3Dsignin',
		'https://classroom.google.com/u/0/h',
		'https://lbhudson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404161793&vdid=ci16ac1y19814r',
		'https://lbhudson.schoolloop.com/lbusdcalendar',
		'https://www.lbschools.net',
		'https://connected.mcgraw-hill.com/connected/login.do',
		'https://www-k6.thinkcentral.com/ePC/start.do',
		'https://play.stmath.com/account.html',
		'https://clever.com/oauth/sis/login?target=NTEyM2Y2MWI5NWYxMDBjOTRlMDAwMDAx%3BZjg4Mjc0NDk0MmRiMzUwMGY5OGM%3D%3BaHR0cHM6Ly9hdXRoLm15bGV4aWEuY29tL2NsZXZlci9vYXV0aC5waHA%2FcHJvZD1teUxleGlhJnBsYXQ9d2Vi%3B%3BY29kZQ%3D%3D&skip=1&default_badge=',
		'https://online.sanfordprograms.org',
		'https://www.khanacademy.org/login',
		'https://www.caaspp.org',
		'https://kpop.ukp.io/login?view=83',
		'https://mysteryscience.com/log-in',
		'https://lbhudson.schoolloop.com/staff',
		'https://lbhudson.schoolloop.com/gallery',
		'https://lbhudson.schoolloop.com/garden',
		'https://lbhudson.schoolloop.com/honorschoir',

		'https://kettering-lbusd-ca.schoolloop.com/bells',
		'https://kettering-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345545&vdid=ia723e1y75kp712z',
		'https://kettering-lbusd-ca.schoolloop.com/programs',
		'https://kettering-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345569&vdid=i234e1y5p7141',
		'https://kettering-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345569&vdid=i23e1y5p714t',
		'https://kettering-lbusd-ca.schoolloop.com/KINDERGARTEN',
		'https://kettering-lbusd-ca.schoolloop.com/1ST',
		'https://kettering-lbusd-ca.schoolloop.com/2ND',
		'https://kettering-lbusd-ca.schoolloop.com/3RD',
		'https://kettering-lbusd-ca.schoolloop.com/4TH',
		'https://kettering-lbusd-ca.schoolloop.com/5TH',

		'https://starrking-lbusd-ca.schoolloop.com/test',
		'https://starrking-lbusd-ca.schoolloop.com/office',
		'https://starrking-lbusd-ca.schoolloop.com/teachers',
		'https://starrking-lbusd-ca.schoolloop.com/linksforstudents',
		'https://starrking-lbusd-ca.schoolloop.com/royalguidelines',
		'https://starrking-lbusd-ca.schoolloop.com/SSC',
		'https://drive.google.com/drive/folders/0B1aDW9Rtvb2tdkI2Z2wxM2pPTE0',
		'https://docs.google.com/document/d/1snJGNraygZtGjslT9yRBUryofvl3Nd4t/edit',
		'https://starrking-lbusd-ca.schoolloop.com/bellschedule',
		'https://starrking-lbusd-ca.schoolloop.com/disciplinepolicy',
		'https://starrking-lbusd-ca.schoolloop.com/schoolsafety',
		'https://drive.google.com/file/d/1imFvlwok9AGqzJjrjwukh03hJ9-Uc-5V/view?usp=sharing',
		'https://drive.google.com/file/d/10s_kt0gBg35PG1uVC84odUtkGUHDZ6Yd/view?usp=sharing',
		'https://drive.google.com/file/d/17vV7o_JD4BlaogTku-ITFgATiKEOYYlp/view?usp=sharing',

		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315220&vdid=i13tf1zns0rgz',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315220&vdid=i13f21zn0rhg',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315220&vdid=ije1w3f1zn0rhx',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315220&vdid=vi13f1zn0rie',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315220&vdid=iv13f1zn0riv',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315220&vdid=8i13f1gznb0rjc',
		'https://lafayette-lbusd-ca.schoolloop.com/di',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315252&vdid=i13f2e7ik2jj',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315267&vdid=i13fi1zn0rm9',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315267&vdid=i713f1zn0rmq',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315267&vdid=i13f1zn0rni',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315267&vdid=yni13f1z9ng0ro0',
		'https://lafayette-lbusd-ca.schoolloop.com/PBC',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315300&vdid=i13f211bzny0rp1',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315300&vdid=5io13fd1zn0rpj',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315300&vdid=aii1e31f1zn0rq0',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315300&vdid=i1x3f1zn80rql',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315300&vdid=xi13f1zn0rr2',
		'https://lafayette-lbusd-ca.schoolloop.com/LionVision',
		'https://lafayette-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315405&vdid=i13f1zn0rxn',
		'https://sites.google.com/lbschools.net/lafayettelions/home',

		'https://lincoln-lbusd-ca.schoolloop.com/vision',
		'https://lincoln-lbusd-ca.schoolloop.com/SARC',
		'https://lincoln-lbusd-ca.schoolloop.com/SSC',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345550&vdid=i18f1y5opi1h5',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345556&vdid=wgijt18f1y5pi1hn',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345556&vdid=i1f8f1y5rpi1ia',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345560&vdid=i1x8afk1y5pi1iw',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345560&vdid=i18f1fyg5gpi1jc',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345560&vdid=i1m8f1py5pi1jt',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345560&vdid=i18f2faafky82wm',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345560&vdid=di18f2m2r044u',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345560&vdid=hib18f2n006d35e',
		'https://lincoln-lbusd-ca.schoolloop.com/SBAC',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345563&vdid=oi18f621y5pi1ku',
		'https://lincoln-lbusd-ca.schoolloop.com/computerlabk2',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345563&vdid=i18fa4j1y5pi1lu',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345563&vdid=i18f1y5pi1mc',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345563&vdid=i18f1y5pi1mu',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345563&vdid=i18fi1y5pi1nc',
		'https://lincoln-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750345563&vdid=i185f1y5pi1nu',

		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=oi19d1szmzu85',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=i19hwrd2qx9g29n',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=si19da1zsmzu8m',
		'https://longfellow-lbusd-ca.schoolloop.com/cafeteria',
		'https://longfellow-lbusd-ca.schoolloop.com/schedules',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=i195d41zmzua8',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=i19d1zmzuar',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=i149d1zimzub7',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=i19dd1zmzubn',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=si19d1zmbzuc6',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=i19d1zmzucm',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315278&vdid=i119d2lzeh38l',
		'https://longfellow-lbusd-ca.schoolloop.com/staff',
		'https://longfellow-lbusd-ca.schoolloop.com/teachers',
		'https://longfellow-lbusd-ca.schoolloop.com/pta',
		'https://longfellow-lbusd-ca.schoolloop.com/PTABoard',
		'https://longfellow-lbusd-ca.schoolloop.com/FAQ',
		'https://longfellow-lbusd-ca.schoolloop.com/greenteam',
		'https://longfellow-lbusd-ca.schoolloop.com/vips',
		'https://longfellow-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315538&vdid=i1j92d81tzmzuh4',
		'https://longfellow-lbusd-ca.schoolloop.com/kindersites',
		'https://longfellow-lbusd-ca.schoolloop.com/firstgrade',
		'https://longfellow-lbusd-ca.schoolloop.com/secondgrade',
		'https://longfellow-lbusd-ca.schoolloop.com/thirdgrade',
		'https://longfellow-lbusd-ca.schoolloop.com/fourthgrade',
		'https://longfellow-lbusd-ca.schoolloop.com/fifthgrade',

		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315382&vdid=i16da1zmzur5',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315402&vdid=ih16cdh1zmzuro',
		'https://loscerritos-lbusd-ca.schoolloop.com/greenteam',
		'https://loscerritos-lbusd-ca.schoolloop.com/PALS/GATE',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315441&vdid=gig16d17zm8zuv7',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315455&vdid=i16jdk1uzmzuvt',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315618&vdid=i16d2m2tl7fv',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315635&vdid=i16d1zm3zu16f',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315649&vdid=i1g6d1zmmzu175',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315611&vdid=i16d1zmzu14s',
		'https://loscerritos-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315611&vdid=9id16d1zmzu15a',
		'https://loscerritos-lbusd-ca.schoolloop.com/pta',

		'https://lowell-lbusd-ca.schoolloop.com/calendar',
		'https://lowell-lbusd-ca.schoolloop.com/curriculum',
		'https://lowell-lbusd-ca.schoolloop.com/schedule',
		'https://lowell-lbusd-ca.schoolloop.com/facts',
		'https://lowell-lbusd-ca.schoolloop.com/map',
		'https://lowell-lbusd-ca.schoolloop.com/uniform',
		'https://lowell-lbusd-ca.schoolloop.com/adminsupport',
		'https://lowell-lbusd-ca.schoolloop.com/teachers',
		'https://lowell-lbusd-ca.schoolloop.com/districtresources',
		'https://lowell-lbusd-ca.schoolloop.com/TestScores',

		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315367&vdid=i192e1zn0k10f',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315367&vdid=i19e1zn0k11g',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315367&vdid=i19le1bzn0k10z',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315367&vdid=si19e14zn0k11x',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315367&vdid=i19e1zn0k12f',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315367&vdid=i19dmesm1zn0k12x',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315367&vdid=i19e1zn0k13n',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315378&vdid=sis19e28pi4q3b5',
		'https://macarthur-lbusd-ca.schoolloop.com/upcomingevents',
		'https://macarthur-lbusd-ca.schoolloop.com/ThankyouRecognition',
		'https://macarthur-lbusd-ca.schoolloop.com/KINDERGAREN',
		'https://macarthur-lbusd-ca.schoolloop.com/1STGRADE',
		'https://macarthur-lbusd-ca.schoolloop.com/2NDGRADE',
		'https://macarthur-lbusd-ca.schoolloop.com/3RDGRADE',
		'https://macarthur-lbusd-ca.schoolloop.com/4THGRADE',
		'https://macarthur-lbusd-ca.schoolloop.com/5thGRADE',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315384&vdid=i15v9e1vzfn0k18m',
		'https://macarthur-lbusd-ca.schoolloop.com/Keyboarding',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315386&vdid=7i19ed1pznt0k19m',
		'https://macarthur-lbusd-ca.schoolloop.com/parents',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315386&vdid=i19e1uzn0k1al',
		'https://macarthur-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315397&vdid=ii1n9e1znl0k1b6',

		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315429&vdid=i31c1zmfzlc8',
		'https://madison-lbusd-ca.schoolloop.com/attendance',
		'https://madison-lbusd-ca.schoolloop.com/calendar',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315429&vdid=i31c1dzmmzldd',
		'https://madison-lbusd-ca.schoolloop.com/schoolsitecouncil',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315429&vdid=pi31ci1zmkzlem',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315429&vdid=i31c1zmzlf6',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315429&vdid=i31c1zmzlfr',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315429&vdid=iy31c1zmzlg7',
		'https://madison-lbusd-ca.schoolloop.com/library',
		'https://madison-lbusd-ca.schoolloop.com/sbac',
		'https://madison-lbusd-ca.schoolloop.com/registration',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315429&vdid=i31c1s9zm4zlvd',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315473&vdid=ai3281c1rzmzlho',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315473&vdid=i03u1qc1zmzli7',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i31c1zmzliw',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i31c1zmzlji',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=ic31cqo1zmzljz',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i31fc1z1llmzlkg',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i31c1zmzlkx',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i31c1zmzllf',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i31c1zmzllx',
		'https://madison-lbusd-ca.schoolloop.com/mathfacts',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i31wqc91zm0zln1',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=u9i3d1c1zmzlno',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315510&vdid=i931c1zmzlo7',
		'https://madison-lbusd-ca.schoolloop.com/notices',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=i31cs1zmzlpj',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=i31c1zmzlyg',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=9i6e31c1zmzlq2',
		'https://madison-lbusd-ca.schoolloop.com/commoncore',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=i31c1gzmzlru',
		'https://madison-lbusd-ca.schoolloop.com/uniforms',
		'https://madison-lbusd-ca.schoolloop.com/mathfacts',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=i31c1zmzlto',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=ei31c1zudmzluv',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=i31c1zmzlvw',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=i31c1zmzlwj',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315514&vdid=6i321cr41zmzlx3',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315548&vdid=i31c1rr6zmzl10d',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315548&vdid=i31c1zmzl11n',
		'https://madison-lbusd-ca.schoolloop.com/meetthemasters2',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315548&vdid=i31c1zmzl135',
		'https://madison-lbusd-ca.schoolloop.com/studentcouncil',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315548&vdid=i31ac1zmzl14w',
		'https://madison-lbusd-ca.schoolloop.com/growthmindset',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315548&vdid=ai318cr1zmzlxs',
		'https://madison-lbusd-ca.schoolloop.com/PTA',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315597&vdid=i3c51c82oxgoj2gc',
		'https://madison-lbusd-ca.schoolloop.com/fundraiser',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315597&vdid=i31c2xv8y02fd',
		'https://madison-lbusd-ca.schoolloop.com/teachersfavoritethings',
		'https://madison-lbusd-ca.schoolloop.com/5thgrade',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315597&vdid=i31c2x8y02gg',
		'https://madison-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315597&vdid=i31g2c2jxgwoj2rx',
		'https://madison-lbusd-ca.schoolloop.com/ptabylaws',

		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826800&vdid=ie11p8a1x2ljks',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826800&vdid=ij1y8aj1xy2ljla',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826800&vdid=i1x82ad1xi2ljlq',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826800&vdid=1i1o876a1x2ljm6',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826801&vdid=ixg018a1x2ljmo',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826801&vdid=i18a11x2ljn8',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826802&vdid=i18a2xgojasg',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826802&vdid=i18a1x2ljnt',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826802&vdid=i18a1tx23sljo9',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826802&vdid=i18a1x2ljos',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826804&vdid=i18a1x2ljpp',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826804&vdid=i183a1x2ljq5',
		'https://mann-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531891826804&vdid=i18xa2mfc1j69d',

		'https://mckinley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315293&vdid=i9f1zn0vya',
		'https://mckinley-lbusd-ca.schoolloop.com/Counseling',
		'https://mckinley-lbusd-ca.schoolloop.com/InstructionalFocus',
		'https://mckinley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315294&vdid=i9kf28vts9jpe',
		'https://mckinley-lbusd-ca.schoolloop.com/WRAP',
		'https://mckinley-lbusd-ca.schoolloop.com/Staff',
		'https://mckinley-lbusd-ca.schoolloop.com/teachingstaff',
		'https://mckinley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537515315296&vdid=i9f2ovza6bh',
		'https://mckinley-lbusd-ca.schoolloop.com/PTA',

		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539089&vdid=wi20f2obmxx45gs',
		'https://naples-lbusd-ca.schoolloop.com/importantdates',
		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539089&vdid=i20f2qoaaun5y1',
		'https://naples-lbusd-ca.schoolloop.com/dolphindialogues',
		'https://naples-lbusd-ca.schoolloop.com/mission',
		'https://naples-lbusd-ca.schoolloop.com/schoolsitecouncil',
		'https://naples-lbusd-ca.schoolloop.com/nutrician',
		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539089&vdid=i20wwf2oaun5bv',
		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539089&vdid=wicv20f2obox4649',
		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539089&vdid=if20f2xoaun5xj',
		'https://naples-lbusd-ca.schoolloop.com/uniformdresscode',
		'https://naples-lbusd-ca.schoolloop.com/bellschedule',
		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539096&vdid=ivvw20f1xjepe7',
		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539096&vdid=i20f1xjjepep',
		'https://parentlbusd.lbschools.net/Login_Parent_PXP.aspx?regenerateSessionId=True&CFID=78285872&CFTOKEN=fc7669f606029403-D428F9B9-D83E-98CD-95326FF772722AA6',
		'https://naples-lbusd-ca.schoolloop.com/schoolsupplychecklists',
		'https://naples-lbusd-ca.schoolloop.com/parenthandbook',
		'https://naplespta.net',
		'https://naples-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973539101&vdid=7i2i0f1xjepfd',
		'https://shop.spreadshirt.com/1033827',
		'https://naples-lbusd-ca.schoolloop.com/ptafundraisers',
		'https://naples-lbusd-ca.schoolloop.com/attendance',

		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299586&vdid=ix15b202gm3zc',
		'https://herrera-lbusd-ca.schoolloop.com/Calendar',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299586&vdid=i15wb202gm3yf',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299586&vdid=i1f5b230m2gm40p',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299586&vdid=i15b2w0ec2sgm3zt',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299586&vdid=i15b202gm409',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299632&vdid=i15a58b202gm41n',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299632&vdid=i1n5b202gm428',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299663&vdid=ki15b202jgm42u',
		'https://herrera-lbusd-ca.schoolloop.com/pawcash',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299663&vdid=id15gb202gm43u',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299698&vdid=7i1i95b2029gm44c',
		'https://herrera-lbusd-ca.schoolloop.com/teacherresources',
		'https://herrera-lbusd-ca.schoolloop.com/ReadingLists',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299698&vdid=i105b202rgm464',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299698&vdid=i15b202gm46o',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299698&vdid=i15b202gm476',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299698&vdid=i15b202gm47m',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299850&vdid=li15bu5202ugm4c1',
		'https://herrera-lbusd-ca.schoolloop.com/CafeteriaMenu',
		'https://herrera-lbusd-ca.schoolloop.com/nutritionservices',
		'https://herrera-lbusd-ca.schoolloop.com/FreeBreakfast',
		'https://lbschools.instructure.com/login/canvas',
		'https://herrera-lbusd-ca.schoolloop.com/parentvue',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299730&vdid=i185b2l02gm485',
		'https://herrera-lbusd-ca.schoolloop.com/vips',
		'https://herrera-lbusd-ca.schoolloop.com/parentuniversity',
		'https://herrera-lbusd-ca.schoolloop.com/sarc',
		'https://www.lbschools.net/Schools/calendars.cfm',
		'https://www.lbschools.net/Departments/School_Support_Services/s-e-b-support.cfm',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178973877&vdid=xi1q5b2n15rb2zs',
		'https://lbschools.instructure.com',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i15qb2o098l4wx',
		'https://parentlbusd.lbschools.net/Login_Student_PXP.aspx?regenerateSessionId=True&CFID=63274060&CFTOKEN=2130aeccae088104-8C498263-BE9B-3D89-96E1573778DEFD33',
		'https://herrera-lbusd-ca.schoolloop.com/Kinder',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299838&vdid=i1a5b202gm4cy',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299838&vdid=i157b20t2gm4de',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299838&vdid=ji15b202gm4du',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299838&vdid=i15bd2s012gm4er',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299838&vdid=iu15ub20q2cgm4f7',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299838&vdid=i15b20b2gm4ft',
		'https://herrera-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299838&vdid=i15bpr2w02gm4g9',
		'https://herrera-lbusd-ca.schoolloop.com/colleges',

		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299480&vdid=yri1l68c202gm2m8',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299480&vdid=itlc16c20n2gm2n3',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299480&vdid=i16c202gm2ni',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299480&vdid=i16c2ya014lsh288',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299482&vdid=i1x62c27ewz73c5',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299484&vdid=i16c202gm2ox',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299484&vdid=i1016ic2020gm2ph',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299486&vdid=di16cg24s02gm2ri',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299486&vdid=i9126acj202gm2rz',
		'https://int-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299486&vdid=ji16qc202gm2sf',

		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=i349qdq1yhudfb',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=i9d1yhudfs',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=oi9d1uylhudg8',
		'https://prisk-lbusd-ca.schoolloop.com/dailyschedule',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=hio9d1yyhtudhn',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=i9d1yhudi4',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=i9d2swb42yn',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=qsi9d1yhnudil',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=i9ad1yhudj2',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931275&vdid=i9d2e4j3h6g40v',
		'https://prisk-lbusd-ca.schoolloop.com/Science',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1578975306810&vdid=i9dbl2pfwnc2qy',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931282&vdid=i9d1yhudtu',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931278&vdid=i9d1yhudkb',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931278&vdid=gi9d1yhudkz',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931291&vdid=i9ad51iyxhudy1',
		'https://prisk-lbusd-ca.schoolloop.com/commoncore',
		'https://prisk-lbusd-ca.schoolloop.com/parents',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931291&vdid=ia9do51yh4udzn',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931291&vdid=i9d1yhud105',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931291&vdid=1i9d1yhud10l',
		'https://prisk-lbusd-ca.schoolloop.com/PTA',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931286&vdid=i9d2amdpg2e3',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535781931288&vdid=i9n4d1vyhuduz',
		'https://prisk-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178973834&vdid=i9k9d2ice85clt',

		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299719&vdid=i20f2r06b2gmth',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299719&vdid=i204fn2v02gmtx',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299719&vdid=6i20f420y2gmue',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299719&vdid=i200fb202xgmuw',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299719&vdid=i20f26aydu1xb',
		'https://riley-lbusd-ca.schoolloop.com/programs',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299758&vdid=v6i203f202gmwm',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299758&vdid=6i270wf202dgmx8',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299768&vdid=hi20f210w2gmyf',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299768&vdid=bi20f26amczg621b',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299768&vdid=u59i20f26zg622f',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299768&vdid=i20f26zg624o',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299768&vdid=i20f202gmxx',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178973888&vdid=i20f30tw69rp',
		'https://riley-lbusd-ca.schoolloop.com/importantnotices',
		'https://riley-lbusd-ca.schoolloop.com/lbschools',
		'https://riley-lbusd-ca.schoolloop.com/homework',
		'https://riley-lbusd-ca.schoolloop.com/handbook',
		'https://riley-lbusd-ca.schoolloop.com/guidelines',
		'https://riley-lbusd-ca.schoolloop.com/development',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299784&vdid=i20f202ggm11v',
		'https://riley-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299839&vdid=i20f2350i2ggm147',

		'https://roosevelt-lbusd-ca.schoolloop.com/aboutrooseveltschool',
		'https://roosevelt-lbusd-ca.schoolloop.com/mission',
		'https://roosevelt-lbusd-ca.schoolloop.com/vision',
		'https://roosevelt-lbusd-ca.schoolloop.com/bells',
		'https://roosevelt-lbusd-ca.schoolloop.com/awards',
		'https://roosevelt-lbusd-ca.schoolloop.com/Announcements',
		'https://roosevelt-lbusd-ca.schoolloop.com/staff',
		'https://roosevelt-lbusd-ca.schoolloop.com/teacherstaff',
		'https://roosevelt-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299776&vdid=i19dajk20b2gm1dg',
		'https://roosevelt-lbusd-ca.schoolloop.com/kindergarten',
		'https://roosevelt-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299821&vdid=mi19d2a0248gm1e2',
		'https://roosevelt-lbusd-ca.schoolloop.com/parents',
		'https://roosevelt-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299800&vdid=i19d202gm1f5',
		'https://roosevelt-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299800&vdid=i19sd23k02gm1fm',
		'https://roosevelt-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279299800&vdid=i19fdu2a9me6h1sx',

		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442839&vdid=i20d204rv1dh',
		'https://signalhill-lbusd-ca.schoolloop.com/bellschedule',
		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442842&vdid=i20syda204rv1ep',
		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279443018&vdid=i20d204rv1g6',
		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279443018&vdid=5i20d204rv1gn',
		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279443020&vdid=is20d20m4jurv1he',
		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279443020&vdid=i20d201k48rv1i3',
		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279443023&vdid=i20dt20q4rv1il',
		'https://signalhill-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279443026&vdid=iv20de204rv1j9',

		'https://burnett-lbusd-ca.schoolloop.com/smithsong',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442966&vdid=5i824e2eo04sjus',
		'https://burnett-lbusd-ca.schoolloop.com/library',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442966&vdid=i24e204sjvp',
		'https://burnett-lbusd-ca.schoolloop.com/computerlabs',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442978&vdid=ifsl24e204sjwl',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442978&vdid=i24e204sjx3',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442982&vdid=i24e204sjxo',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=si324ema2o44n2i5',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i24e23q8pc4zy4rz',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=iyy24e2cve1ot4u5',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i524e0p2c1ot4up',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i24ep2c1ot4v6',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=li24oe2yo44n2oy',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i24g7e2o44n329',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i24e2o4o4n2pw',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i24exg2hlokbc14',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i2p4e5l2f5ez33em',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i2j4eu2ako44n2d5',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i24e12o44n2up',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=ig24ney2o44n33c',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i242bqe2o44n2nd',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i2m4e862cm1ot4vn',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i24le2c7i9f37z',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=i2i4euqx2o44n31s',
		'https://smith-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050558181&vdid=is24kei2o5ar2ho',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442991&vdid=li24ke2slpev2d9',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442991&vdid=i2m4ne02mezt2hk',
		'https://burnett-lbusd-ca.schoolloop.com/parentlinks',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442991&vdid=i2k4e2lg7iw2nb',
		'https://burnett-lbusd-ca.schoolloop.com/kindergarten',
		'https://burnett-lbusd-ca.schoolloop.com/firstgradelinks',
		'https://burnett-lbusd-ca.schoolloop.com/secondgradelinks',
		'https://burnett-lbusd-ca.schoolloop.com/thirdgradelinks',
		'https://burnett-lbusd-ca.schoolloop.com/fourthgradelinks',
		'https://burnett-lbusd-ca.schoolloop.com/fifthgradelinks',
		'https://burnett-lbusd-ca.schoolloop.com/sbac',
		'https://burnett-lbusd-ca.schoolloop.com/ScienceFair',
		'https://burnett-lbusd-ca.schoolloop.com/typingskills',
		'https://burnett-lbusd-ca.schoolloop.com/studentLBUSDPortal',
		'https://burnett-lbusd-ca.schoolloop.com/mobymax',
		'https://burnett-lbusd-ca.schoolloop.com/readworks',
		'https://burnett-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442996&vdid=i2l84e2sp04sj152',

		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442919&vdid=i19a204qnz7',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442919&vdid=i19a2h0x4nqnzp',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442919&vdid=i1l9a2hmms49gr',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442919&vdid=i19an204qn10g',
		'https://stevenson-lbusd-ca.schoolloop.com/SSC',
		'https://stevenson-lbusd-ca.schoolloop.com/uniforms',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442919&vdid=i19a2yrcs2heu',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442929&vdid=i19a20j4qn11m',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442931&vdid=i19ap204qn125',
		'https://stevenson-lbusd-ca.schoolloop.com/pta',
		'https://stevenson-lbusd-ca.schoolloop.com/spiritwear',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442940&vdid=i19ac2turgyaak',
		'https://stevenson-lbusd-ca.schoolloop.com/art-studio',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442940&vdid=i19a42k04lqn13p',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442940&vdid=iw1t9yad31kba34fd',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442940&vdid=i1m90a204qn147',
		'https://stevenson-lbusd-ca.schoolloop.com/photogallery',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442943&vdid=i91x9ado2qtx38nr',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442943&vdid=i19an42t4rgya92',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442943&vdid=i19av20k4nqn15c',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442943&vdid=i19a204qn161',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442945&vdid=ic19a20t4vdqn17s',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442947&vdid=i19jau30r4j150d',
		'https://stevenson-lbusd-ca.schoolloop.com/hlo',
		'https://stevenson-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442946&vdid=i19ia2ralla5d',

		'https://twain-lbusd-ca.schoolloop.com/abouttwain',
		'https://twain-lbusd-ca.schoolloop.com/staff',
		'https://twain-lbusd-ca.schoolloop.com/counselorcorner',
		'https://twain-lbusd-ca.schoolloop.com/enrollmentprocedures',
		'https://twain-lbusd-ca.schoolloop.com/awards',
		'https://twain-lbusd-ca.schoolloop.com/parentinvolvement',
		'https://twain-lbusd-ca.schoolloop.com/contactus',
		'https://twain-lbusd-ca.schoolloop.com/music',
		'https://twain-lbusd-ca.schoolloop.com/dailybellschedules',
		'https://twain-lbusd-ca.schoolloop.com/unifromguidelines',
		'https://twain-lbusd-ca.schoolloop.com/cafeteriameals',
		'https://twain-lbusd-ca.schoolloop.com/supplylists',
		'https://twain-lbusd-ca.schoolloop.com/pta',
		'https://twain-lbusd-ca.schoolloop.com/boxtops',

		'https://whittier-lbusd-ca.schoolloop.com/Messase',
		'https://whittier-lbusd-ca.schoolloop.com/dailyschedule',
		'https://whittier-lbusd-ca.schoolloop.com/dresscode',
		'https://whittier-lbusd-ca.schoolloop.com/quickfacts',
		'https://whittier-lbusd-ca.schoolloop.com/visionstatement',
		'https://whittier-lbusd-ca.schoolloop.com/learninggarden',
		'https://whittier-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279442925&vdid=i1x5ey2kwst95178y',
		'https://whittier-lbusd-ca.schoolloop.com/femineer',
		'https://whittier-lbusd-ca.schoolloop.com/steam',
		'https://whittier-lbusd-ca.schoolloop.com/adminsupportstaff',
		'https://whittier-lbusd-ca.schoolloop.com/teachers',
		'https://whittier-lbusd-ca.schoolloop.com/commoncore',
		'https://whittier-lbusd-ca.schoolloop.com/elac',
		'https://whittier-lbusd-ca.schoolloop.com/internetsafety',
		'https://whittier-lbusd-ca.schoolloop.com/k-2',
		'https://whittier-lbusd-ca.schoolloop.com/technologypractice',

		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411629&vdid=i16d1x0tjjhr',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411629&vdid=ni1hs6d71x0jji7',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411629&vdid=i1j6d1x0jjio',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411636&vdid=i16d21xc0jjj6',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411629&vdid=7i16d1x0jjjm',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411639&vdid=i16d71x70jjk3',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411639&vdid=ixuf16d1x05jjkj',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411639&vdid=i176nd1x0jjkz',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411641&vdid=id16d1x0jjlh',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411641&vdid=i16fird1x0jjm8',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411643&vdid=iu16d71x0jjmv',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411643&vdid=i16d1x0jjnb',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411646&vdid=i16d1x0jjnu',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411647&vdid=i16d1x0wbjjob',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411645&vdid=i1g6dy1xc0jjor',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411648&vdid=i16d1x0jjp8',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411649&vdid=ix16d1tsx0jjpq',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411649&vdid=ri16d1x0jjq7',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411649&vdid=i19e6d1x0xjjqo',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411649&vdid=i16d13x0jjr5',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411649&vdid=ji16d1xj0jjrl',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411649&vdid=i1m6dw1x0jjs1',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411650&vdid=i916d1d5x60jjsi',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411651&vdid=i1r6d41x0jjsz',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411652&vdid=i16d1xsw0jjtg',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411653&vdid=ni160d1x0jjtz',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411653&vdid=i16rd1x0jjuw',
		'https://wld-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973411655&vdid=i16d1x0djjvn',

		'https://but-lbusd.ca.schoolloop.com/buffum',
		'https://but-lbusd.ca.schoolloop.com/bells',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106589&vdid=fi019b02yyg382z6',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106589&vdid=im1f9b2ygj382zn',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106590&vdid=i319bvh20hwme14x',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106590&vdid=i19b31kba95l',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106590&vdid=i19b20wme15d',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106590&vdid=i1e9b2g0wjme15u',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106590&vdid=i1t5u79b20wme16e',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106590&vdid=i19b20wme16u',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106590&vdid=i19gb20kwme17a',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178974187&vdid=4i1hr9b20yg382xe',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178974187&vdid=i019b2y5puif3bi',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106591&vdid=i19b62eaac51yr',
		'https://but-lbusd.ca.schoolloop.com/test',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178974187&vdid=i199b2505h1p1lj',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106592&vdid=i189b20kfwme187',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106593&vdid=itev19b20wume18o',
		'https://but-lbusd.ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1542443106594&vdid=3i159ob2q0wme194',

		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788690&vdid=i14e27g2v1cd',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788691&vdid=i0xp14e27g2v1cu',
		'https://hd-lbusd-ca.schoolloop.com/adminoffice',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788693&vdid=il1b4ey27g2v1e2',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788693&vdid=i1o4e27g2v1ep',
		'https://hd-lbusd-ca.schoolloop.com/hscalendar',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788694&vdid=i14e427tg2v1g0',
		'https://hd-lbusd-ca.schoolloop.com/pc',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1562686940206&vdid=i14e284m01uz',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1581409235828&vdid=3i14e625epri32vx',
		'https://hd-lbusd-ca.schoolloop.com/tutoring',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=7i14e27dag2v1t7',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=li14e27g2v1tv',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i14e27g2v1uf',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i14e27g2v1ux',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i14e27g2v1ww',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=gyin14e27g2v1xd',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i714e2o7gi2v1xv',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i14e27gg2v1yc',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i14e27g2v1yt',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=ai14e27g2v1zb',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i14e27g2v1zs',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=8i14e27gq2v209',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=0i14eg27g2v20q',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=i134e27g2v217',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638788696&vdid=ki14e207g2v21o',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1584169978464&vdid=ti14e2g2qa4j3k6',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1584169978464&vdid=0rig14ne2g24j3in',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1584169978464&vdid=ni14pe23g274j3gz',
		'https://hd-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1591860367707&vdid=i714he2i6hsr376',
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
