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
		'https://lbavalon.schoolloop.com/historyschool',
		'https://lbavalon.schoolloop.com/policies',
		'https://lbavalon.schoolloop.com/schedule',
		'https://lbavalon.schoolloop.com/welcome',
		'https://lbavalon.schoolloop.com/staffdirectory',
		'https://lbavalon.schoolloop.com/calendar',
		'https://lbavalon.schoolloop.com/avid',
		'https://lbavalon.schoolloop.com/counselingandcollege',
		'https://lbavalon.schoolloop.com/lancersgotocollege',
		'https://lbavalon.schoolloop.com/hschecklist',
		'https://lbavalon.schoolloop.com/draduation',
		'https://lbavalon.schoolloop.com/choices',
		'https://lbavalon.schoolloop.com/avalonlancers',
		'https://lbavalon.schoolloop.com/crosscountry',
		'https://lbavalon.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750286287&vdid=i933b1y5ny19j',
		'https://lbavalon.schoolloop.com/girlsvolleyball',
		'https://lbavalon.schoolloop.com/boysbasketball',
		'https://lbavalon.schoolloop.com/girlsbasketball',
		'https://lbavalon.schoolloop.com/cheer',
		'https://lbavalon.schoolloop.com/boyssoccer',
		'https://lbavalon.schoolloop.com/girlssoccer',
		'https://lbavalon.schoolloop.com/baseball',
		'https://lbavalon.schoolloop.com/boysgolf',
		'https://lbavalon.schoolloop.com/boysvolleyball',
		'https://lbavalon.schoolloop.com/softball',
		'https://lbavalon.schoolloop.com/title-IX',
		'https://lbavalon.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750286274&vdid=ij33jb1y55tny15p',
		'https://lbavalon.schoolloop.com/pta',
		'https://lbavalon.schoolloop.com/elac',
		'https://lbavalon.schoolloop.com/sitecouncil',

		'https://ilp-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i243ek1zly111o',
		'https://ilp-lbusd-ca.schoolloop.com/parents',
		'https://ilp-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972792&vdid=i243e24wt795q8z',
		'https://ilp-lbusd-ca.schoolloop.com/about',
		'https://ilp-lbusd-ca.schoolloop.com/principal',
		'https://ilp-lbusd-ca.schoolloop.com/resources',
		'https://ilp-lbusd-ca.schoolloop.com/counseling',
		'https://ilp-lbusd-ca.schoolloop.com/dual-enrollment',

		'https://browning-lbusd-ca.schoolloop.com/rdb',
		'https://browning-lbusd-ca.schoolloop.com/announcements',
		'https://browning-lbusd-ca.schoolloop.com/BrowningBellSchedule',
		'https://browning-lbusd-ca.schoolloop.com/lbusd',
		'https://browning-lbusd-ca.schoolloop.com/principalsmessage',
		'https://browning-lbusd-ca.schoolloop.com/staff',
		'https://browning-lbusd-ca.schoolloop.com/academics',
		'https://browning-lbusd-ca.schoolloop.com/advanced-placement',
		'https://browning-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296081&vdid=i10ea29x51ol4r1x',
		'https://browning-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296081&vdid=i10e1xaixvz',
		'https://browning-lbusd-ca.schoolloop.com/btsn',
		'https://browning-lbusd-ca.schoolloop.com/library',
		'https://browning-lbusd-ca.schoolloop.com/pathways',
		'https://browning-lbusd-ca.schoolloop.com/activities',
		'https://browning-lbusd-ca.schoolloop.com/ABS',
		'https://browning-lbusd-ca.schoolloop.com/bhsclubs',
		'https://browning-lbusd-ca.schoolloop.com/keyclub',
		'https://browning-lbusd-ca.schoolloop.com/college&career',
		'https://browning-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296089&vdid=i108e1xaixy8',
		'https://browning-lbusd-ca.schoolloop.com/career&college',
		'https://browning-lbusd-ca.schoolloop.com/internships',
		'https://browning-lbusd-ca.schoolloop.com/ecpp',
		'https://browning-lbusd-ca.schoolloop.com/thehangout',
		'https://browning-lbusd-ca.schoolloop.com/parents',
		'https://docs.google.com/presentation/d/1-n9YGpwo8qdGQGM-TUqY6W2TLhLQajPDNnCs0U1cBW0/edit?usp=sharing',
		'https://ca-lbusd-psv.edupoint.com/PXP2_Login_Parent.aspx?regenerateSessionId=True',
		'https://browning-lbusd-ca.schoolloop.com/ptsa',
		'https://go.schoolmessenger.com/',
		'https://www.lbschools.net/Departments/School_Choice/hs_choice.cfm',
		'https://browning-lbusd-ca.schoolloop.com/sscbrowning',
		'https://browning-lbusd-ca.schoolloop.com/sbdm',
		'https://browning-lbusd-ca.schoolloop.com/title1',
		'https://browning-lbusd-ca.schoolloop.com/studentresources',
		'https://browning-lbusd-ca.schoolloop.com/freshman',

		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=i55f1xajv2fl',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=iq5u5f2i27vu73u',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=i55f1xajv2f3',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=i55f13xajv1ls',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=ih55f1xat2ejv1fq',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=ii55fu1xa2jv1f4',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=ni55f2f584z5po',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=wi55f2ozan5nd',
		'https://lbcabrillo.schoolloop.com/principal',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=i55fo0t1xrajv1iv',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=i55ef1xajv1zf',
		'https://lbcabrillo.schoolloop.com/sdm',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296144&vdid=i55f1aexaujv21m',
		'https://lbcabrillo.schoolloop.com/wasc',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296149&vdid=i54u5f1xe9ajv1py',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296149&vdid=i5594f2wdpj7sw',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296149&vdid=i55f1qxajv2yc',
		'https://lbcabrillo.schoolloop.com/calj',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296149&vdid=i55f1xriajv3dx',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296149&vdid=tfi55f461xajv3ba',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296149&vdid=i55f21xajv3lc',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296062&vdid=i55ff2pwlpo0f9p',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f22mltj5t3',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296062&vdid=i55f28wlo0f8i',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296062&vdid=i5m5f2wlo0fnw',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296062&vdid=ig55ff2wlo07zq',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=i55fi0t1x2ajv2ac',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=i55lf19xtajv2dh',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=i554if1xajv2ej',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=qdi55gf1xgajv2g4',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=i556owf25i7vu74y',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638725952&vdid=i55f2a78cx72p',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296177&vdid=i55hfy1xahsjv23q',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=i5e5ft1x7a4jv2k3',
		'https://ca-lbusd-psv.edupoint.com/PXP2_Login.aspx',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=i55f30q0u6ni',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296176&vdid=i585fr1xsawjv1l9',
		'https://lbcabrillo.schoolloop.com/parents',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296174&vdid=i55f61xajv20n',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296174&vdid=i55f1xbajv1ve',
		'https://lbcabrillo.schoolloop.com/athletics',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f22mltj5t3',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55fn2d4xmx69g',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f22elm8tj5mu',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=ij55f23t264ui',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=ki557f22mtj5pa',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f245a04t7',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f23xsp4y4',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=di545f2dmv8s6ey',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f245a0534',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f522mfutj65q',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296173&vdid=i55f245a04ka',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296357&vdid=i55f1n8xajv4rk',
		'https://lbcabrillo.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973296357&vdid=i55f10xajv4ur',

		'https://lbcams.schoolloop.com/ourschool',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973733849&vdid=i35c313r95sk',
		'https://lbcams.schoolloop.com/admissions',
		'https://lbcams.schoolloop.com/remotelearning',
		'https://lbcams.schoolloop.com/camsinthemedia',
		'https://lbcams.schoolloop.com/dailyschedules',
		'https://lbcams.schoolloop.com/directionstocams',
		'https://lbcams.schoolloop.com/faculty',
		'https://lbcams.schoolloop.com/eslr',
		'https://lbcams.schoolloop.com/howtocontactcams',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973733849&vdid=i35tc1xq3je7',
		'https://lbcams.schoolloop.com/Parking',
		'https://lbcams.schoolloop.com/WASC2015',
		'https://lbcams.schoolloop.com/video',
		'https://lbcams.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=it356c2bawjzz2cm',
		'https://lbcams.schoolloop.com/CTE',
		'https://lbcams.schoolloop.com/AP',
		'https://lbcams.schoolloop.com/courseofstudy',
		'https://lbcams.schoolloop.com/PhysicalEd',
		'https://lbcams.schoolloop.com/ASB',
		'https://lbcams.schoolloop.com/clubs',
		'https://lbcams.schoolloop.com/Rebels',
		'https://lbcams.schoolloop.com/FRC',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050727534&vdid=i35c1xq3jq8',
		'https://lbcams.schoolloop.com/cscclub',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1579926543630&vdid=i35c2te9q81gn',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1599895008366&vdid=i35c2lw5inm9218h',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1579926543630&vdid=i35c2y9fc3fe',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973733857&vdid=4i35mc1xqxb3jrb',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973733858&vdid=i35c1swxoq3jqu',
		'https://lbcams.schoolloop.com/seniors',
		'https://lbcams.schoolloop.com/studentsupport',
		'https://lbcams.schoolloop.com/WBL',
		'https://drive.google.com/file/d/1B8ycL6pZ_pjmdRgo1vy9QLgfU0Vw7pY0/view?usp=sharing',
		'https://lbcams.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1602920572601&vdid=e16i35c2gmtfh13e',
		'https://lbcams.schoolloop.com/parents',
		'https://lbcams.schoolloop.com/sitecouncil',
		'https://lbcams.schoolloop.com/pf4/cms2/news_themed_display?id=1630733518403',
		'https://lbcams.schoolloop.com/pf4/cms2/news_themed_display?id=1629526709222',

		'https://ephs-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605796238&vdid=i39c1wykecx271',
		'https://ephs-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605796238&vdid=i39c1yecx27i',
		'https://ephs-lbusd-ca.schoolloop.com/Parent_Center',
		'https://ephs-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605796241&vdid=i39c1ycencx28i',
		'https://ephs-lbusd-ca.schoolloop.com/enrollment',
		'https://ephs-lbusd-ca.schoolloop.com/administrativeandsupportstaff',
		'https://ephs-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605796244&vdid=ii3293cj1yecx29z',
		'https://ephs-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605796253&vdid=ig439c1xyexcx2b1',

		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=i56f1xvnfb4',
		'https://lbjordan.schoolloop.com/bellschedules',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=i56f29hcd61x',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=i56fe1x9vanfcg',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=i5c6f2xegoj5h8',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=ia56f2luyw4ar',
		'https://lbjordan.schoolloop.com/policies',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=i56f21ee91ft',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1543480307971&vdid=ie56f218ns9m2sv',
		'https://lbjordan.schoolloop.com/ssc',
		'https://lbjordan.schoolloop.com/jac',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=xi56f23j0p373',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135282&vdid=i56hf12a5wk36j',
		'https://lbjordan.schoolloop.com/campushistory',
		'https://lbjordan.schoolloop.com/donate',
		'https://lbjordan.schoolloop.com/visual',
		'https://lbjordan.schoolloop.com/cte',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135443&vdid=ic56f81xdxvnflr',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135423&vdid=i56f1xvnfl7',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135423&vdid=c2i5u6f2bnc3s3xi',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135459&vdid=i56f1xfvnfma',
		'https://lbjordan.schoolloop.com/alg',
		'https://docs.google.com/document/d/1QUQLX3frkCb8eW0Xke8pCkffj5EYIuKRvWY8zJC4wDs/edit?usp=sharing',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135496&vdid=in56f1xvnfp7',
		'https://lbjordan.schoolloop.com/jhsscienceft',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135578&vdid=ic5s6f1xsvnfw2',
		'https://lbjordan.schoolloop.com/modernworld',
		'https://lbjordan.schoolloop.com/ushistory',
		'https://lbjordan.schoolloop.com/govecon',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974135597&vdid=i5cl067f1xvnfy5',
		'https://lbjordan.schoolloop.com/dance',
		'https://lbjordan.schoolloop.com/pe',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974144445&vdid=i56f2w517m6112',
		'https://sites.google.com/lbschools.net/jhs-advanced-panthers/home',
		'https://lbjordan.schoolloop.com/activities',
		'https://lbjordan.schoolloop.com/asb',
		'https://lbjordan.schoolloop.com/banker',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974144511&vdid=i56af24s6ebm34lm',
		'https://lbjordan.schoolloop.com/seniors',
		'https://lbjordan.schoolloop.com/yearbook',
		'https://lbjordan.schoolloop.com/athletics',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974144588&vdid=ii56f1xvnf18f',
		'https://lbjordan.schoolloop.com/badminton',
		'https://lbjordan.schoolloop.com/baseball',
		'https://lbjordan.schoolloop.com/boysbasketball',
		'https://lbjordan.schoolloop.com/crosscountry',
		'https://lbjordan.schoolloop.com/football',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974144798&vdid=i56fe1px0vnf1l9',
		'https://lbjordan.schoolloop.com/boyssoccer',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974145512&vdid=i5i6f1xv8vnf1nk',
		'https://lbjordan.schoolloop.com/tennis',
		'https://lbjordan.schoolloop.com/trackandfield',
		'https://lbjordan.schoolloop.com/volleyball',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146073&vdid=i56f1x2vnf1r4',
		'https://lbjordan.schoolloop.com/title-ix',
		'https://lbjordan.schoolloop.com/careercenter',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1569050949244&vdid=i56f2lirp42t',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1599894680805&vdid=di56f2lhpm438',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146085&vdid=i56f29vuv3g3',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146097&vdid=il5f6f2c1n9m2yc',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146097&vdid=fi56gf29usd3cp',
		'https://lbjordan.schoolloop.com/counselors',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146130&vdid=i56f31hxvnf1yn',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146144&vdid=r6i56df18xvnf1zh',
		'https://lbjordan.schoolloop.com/maleacademy',
		'https://lbjordan.schoolloop.com/jordanwrap',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146097&vdid=i56f3135r98df',
		'https://lbjordan.schoolloop.com/counselors',
		'https://lbjordan.schoolloop.com/counselingacademic',
		'https://lbjordan.schoolloop.com/graduationrequirements',
		'https://lbjordan.schoolloop.com/FinancialAidandScholarships',
		'https://lbjordan.schoolloop.com/freshmanbrochure',
		'https://lbjordan.schoolloop.com/personalsocial',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146110&vdid=ai56f2eju3q3453',
		'https://lbjordan.schoolloop.com/seniors',
		'https://lbjordan.schoolloop.com/parentcenter',
		'https://lbjordan.schoolloop.com/jordanpta',
		'https://lbjordan.schoolloop.com/jpac',
		'https://lbjordan.schoolloop.com/elac',
		'https://lbjordan.schoolloop.com/vips',
		'https://lbjordan.schoolloop.com/slc',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974146217&vdid=ik56f1xvnf2hz',
		'https://lbjordan.schoolloop.com/ace',
		'https://lbjordan.schoolloop.com/ib',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531974151221&vdid=i56f1xvnf2xj',
		'https://lbjordan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1537514580157&vdid=i56f1z8jlv1',
		'https://lbjordan.schoolloop.com/perkinsinfo',

		'https://lblakewood.schoolloop.com/principal',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231157508&vdid=i53e1xxm1jlm',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231157576&vdid=i53o6he1xfx1jsk',
		'https://lblakewood.schoolloop.com/Bulletin',
		'https://lblakewood.schoolloop.com/map',
		'https://lblakewood.schoolloop.com/facts',
		'https://lblakewood.schoolloop.com/interventions',
		'https://lblakewood.schoolloop.com/medicalpolicies',
		'https://lblakewood.schoolloop.com/ProspectiveStudents',
		'https://lblakewood.schoolloop.com/SaturdaySchool',
		'https://lblakewood.schoolloop.com/SARC',
		'https://lblakewood.schoolloop.com/StaffDirectory',
		'https://lblakewood.schoolloop.com/WASC',
		'https://lblakewood.schoolloop.com/welcome',
		'https://lblakewood.schoolloop.com/new',
		'https://lblakewood.schoolloop.com/Academics',
		'https://lblakewood.schoolloop.com/AVID',
		'https://lblakewood.schoolloop.com/cte',
		'https://lblakewood.schoolloop.com/English',
		'https://lblakewood.schoolloop.com/ell',
		'https://lblakewood.schoolloop.com/FLA',
		'https://lblakewood.schoolloop.com/library',
		'https://lblakewood.schoolloop.com/Math',
		'https://lblakewood.schoolloop.com/njrotc',
		'https://lblakewood.schoolloop.com/PE',
		'https://lblakewood.schoolloop.com/science',
		'https://lblakewood.schoolloop.com/history',
		'https://lblakewood.schoolloop.com/SpecialEducation',
		'https://lblakewood.schoolloop.com/VAPA',
		'https://lblakewood.schoolloop.com/ForeignLanguage',
		'https://lblakewood.schoolloop.com/atm',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231157839&vdid=i5163nde1xx1j23j',
		'https://lblakewood.schoolloop.com/AboutATM',
		'https://lblakewood.schoolloop.com/AMTCOS',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231157839&vdid=i53e24nek75bc',
		'https://lblakewood.schoolloop.com/atmteam',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231157839&vdid=tij53e1xx1j28t',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231157839&vdid=i53e1xx1j29b',
		'https://lblakewood.schoolloop.com/eMail_Standards',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231157839&vdid=i53e2unek75bz',
		'https://lblakewood.schoolloop.com/lancerathletics',
		'https://lblakewood.schoolloop.com/athleticorientation',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231159207&vdid=i53e2hw8925dl',
		'https://lblakewood.schoolloop.com/clearance',
		'https://lblakewood.schoolloop.com/contractbehavior',
		'https://lblakewood.schoolloop.com/Baseball',
		'https://lblakewood.schoolloop.com/badminton',
		'https://lblakewood.schoolloop.com/boysbasketball',
		'https://lblakewood.schoolloop.com/boysgolff',
		'https://lblakewood.schoolloop.com/soccerboys',
		'https://lblakewood.schoolloop.com/swimboys',
		'https://lblakewood.schoolloop.com/BoysTennis',
		'https://lblakewood.schoolloop.com/volleyballboys',
		'https://lblakewood.schoolloop.com/waterpoloboys',
		'https://cifstate.org/covid-19/6.12.20_release',
		'https://lblakewood.schoolloop.com/crosscountry',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231159260&vdid=2i53e1xx1j3rk',
		'https://lblakewood.schoolloop.com/girlsbasketball',
		'https://lblakewood.schoolloop.com/girlsgolf',
		'https://lblakewood.schoolloop.com/girlssoccer',
		'https://lblakewood.schoolloop.com/swimgirls',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1587875090102&vdid=iw53em1yxx1j45i',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231159307&vdid=si53e1xtdx1j47v',
		'https://lblakewood.schoolloop.com/waterpologirls',
		'https://lblakewood.schoolloop.com/gymnastics',
		'https://lblakewood.schoolloop.com/ncaa',
		'https://lblakewood.schoolloop.com/softball',
		'https://lblakewood.schoolloop.com/summersports',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231159181&vdid=i53e1xx1j4t0',
		'https://lblakewood.schoolloop.com/track',
		'https://lblakewood.schoolloop.com/wrestling',
		'https://lblakewood.schoolloop.com/ASB',
		'https://lblakewood.schoolloop.com/activities',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231168263&vdid=i5xo3e23yng6f2',
		'https://lblakewood.schoolloop.com/boosterclub',
		'https://lblakewood.schoolloop.com/Calendar',
		'https://lblakewood.schoolloop.com/cheer',
		'https://lblakewood.schoolloop.com/clubs',
		'https://lblakewood.schoolloop.com/ColorGuard',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231159383&vdid=i53e61nxx1j58y',
		'https://lblakewood.schoolloop.com/fundraisers',
		'https://lblakewood.schoolloop.com/GradNite',
		'https://lblakewood.schoolloop.com/Music',
		'https://lblakewood.schoolloop.com/Lancerettes',
		'https://lblakewood.schoolloop.com/LinkCrew',
		'https://lblakewood.schoolloop.com/studentstore',
		'https://lblakewood.schoolloop.com/graduation',
		'https://lblakewood.schoolloop.com/yearbook',
		'https://lblakewood.schoolloop.com/YearbookInventory',
		'https://lblakewood.schoolloop.com/NHSCSF',
		'https://lblakewood.schoolloop.com/attendance',
		'https://lblakewood.schoolloop.com/bell',
		'https://lblakewood.schoolloop.com/map',
		'https://lblakewood.schoolloop.com/celebrations',
		'https://lblakewood.schoolloop.com/careercenter',
		'https://lblakewood.schoolloop.com/dresscode',
		'https://lblakewood.schoolloop.com/packet',
		'https://lblakewood.schoolloop.com/CodeOfConduct',
		'https://classroom.google.com/u/0/c/NTUxOTkwNDk3NDRa',
		'https://www.everyoneon.org/find-offers-longbeach?partner=longbeach&custom=1',
		'https://lblakewood.schoolloop.com/medicalpolicies',
		'https://www.lbschools.net/Departments/Nutrition_Services/',
		'https://longbeach.rocketscanapps.com/',
		'https://lblakewood.schoolloop.com/bellschedule',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231159455&vdid=i53e2pps6y5jy',
		'https://parentlbusd.lbschools.net/PXP2_Login_Student.aspx?regenerateSessionId=True&CFID=102348354&CFTOKEN=179b1cc7d7ffc22a-ABAB4D27-B23B-821D-2AEF46ED8BFA3405',
		'https://lblakewood.schoolloop.com/attendance',
		'https://www.youtube.com/watch?v=t-5sWZODhY8&feature=youtu.be&fbclid=IwAR2W8CmKhY2wAd2wDvi8vATD0bLv-bSc8AkCbMGBUq7Nlrb-h2RLHme1tPU',
		'https://lblakewood.schoolloop.com/careercenter',
		'https://lblakewood.schoolloop.com/Complaint',
		'https://lblakewood.schoolloop.com/Counseling',
		'https://lbschools.instructure.com/courses/43807',
		'https://drive.google.com/file/d/17LvzOEke0dpjKnMVoyDmJ-03PL22XOPD/view',
		'https://lblakewood.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231168206&vdid=i503e2yykdpr4kt',
		'https://lblakewood.schoolloop.com/homelessprogram',
		'https://lblakewood.schoolloop.com/packet',
		'https://classroom.google.com/u/0/c/NTUxOTkwNDk3NDRa',
		'https://www.everyoneon.org/find-offers-longbeach?partner=longbeach&custom=1',
		'https://lblakewood.schoolloop.com/medicalpolicies',
		'https://lblakewood.schoolloop.com/Volunteers',
		'https://parentlbusd.lbschools.net/PXP2_Login_Parent.aspx?regenerateSessionId=True&CFID=102347619&CFTOKEN=324406e28107c9-AAB6324B-98F4-A602-92FD6786D6197ED0',
		'https://lblakewood.schoolloop.com/ptsa',
		'https://www.lbschools.net/Departments/School_Choice/hs_choice.cfm',
		'https://lblakewood.schoolloop.com/SchoolSiteCouncil',

		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864799&vdid=i11fl1yqebfoh1k3',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864799&vdid=ji11f1w3yfoh1ko',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864799&vdid=i116f1yfoh1ln',
		'https://lbsa-lbusd-ca.schoolloop.com/willow-campus-map',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i1j1f23bak2fb',
		'https://lbsa-lbusd-ca.schoolloop.com/certified-nurses-assistant',
		'https://lbsa-lbusd-ca.schoolloop.com/animal-care',
		'https://lbsa-lbusd-ca.schoolloop.com/esl',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864805&vdid=i11fa1fypgfoh1nl',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864805&vdid=i11f1y1ofo1oh1o6',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864805&vdid=i11f1yfoh1op',
		'https://lbsa-lbusd-ca.schoolloop.com/hiset',
		'https://lbsa-lbusd-ca.schoolloop.com/hiset-home-study',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864805&vdid=i11fi9k1ykfoh1qq',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864805&vdid=i11f31kbaw0g',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864805&vdid=i711f1yefooh1r7',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864806&vdid=i1pb1pf1yfroh1u0',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864806&vdid=i11fr1lyfoh1ug',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864808&vdid=i11f1yfnoh1ux',
		'https://lbsa-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1535605864808&vdid=vi11f1yf9oh1vn',
		'https://lbsa-lbusd-ca.schoolloop.com/calendar',
		'https://lbsa-lbusd-ca.schoolloop.com/classes',

		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347331&vdid=i4e1wtwphbt9',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=i4be1wthbmd',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=i4he21wwthbmu',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=i4e1wjthbq1',
		'https://mcbride-lbusd-ca.schoolloop.com/3-pathways',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=i4e1swtehbna',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=i4ey1wthbnq',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=hi4se1wthbp5',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=il4e1wthbo7',
		'https://mcbride-lbusd-ca.schoolloop.com/wasc',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=i4e1wtnhbop',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347322&vdid=i4e1wthbpl',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347324&vdid=i4te1cwthbr3',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347336&vdid=i4e2aajd43ey',
		'https://mcbride-lbusd-ca.schoolloop.com/cji',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347336&vdid=if4de1wtmhbza',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347339&vdid=ij4pe1wtmhbw9',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347366&vdid=i4aes2qyjfc82hz',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347366&vdid=i4e2rdum2ky',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347366&vdid=i82v4ev2x3uh62z',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347374&vdid=i45e1wthb1bd',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347376&vdid=i4e1wthb1di',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347376&vdid=i4m5e23lby8i39i',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347376&vdid=i24ofe1wt6hb1fa',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347377&vdid=i4e14wthb1iy',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=i4e2gd6w31s',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347389&vdid=i4e1ze3w19g',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=qi4dex1wthb1uv',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=mi4e1wthb1vg',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=i4e1wthb1wt',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=i4e1wtohb1z0',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=i4e1wthb1zt',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347390&vdid=i4ew1wthb1yb',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347406&vdid=i4e1wthb20h',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=i4e1wt9thb22y',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347382&vdid=i4e1dfwnthb23w',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347407&vdid=i4de3o1jwthb25q',
		'https://linktr.ee/mcbrideasb',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347407&vdid=i4e2wat95bmz',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347407&vdid=i4e21tgm61yi',
		'https://mcbride-lbusd-ca.schoolloop.com/wolfpacksportsclub',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347407&vdid=i4e26x3uh7xv',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347412&vdid=i4e1wthb2sk',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347412&vdid=imm4ye1twthb2t2',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347412&vdid=mi4ex1ywtbhb2tn',
		'https://mcbride-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530973347412&vdid=i4e1wthb2u5',

		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1585383465783&vdid=1i584e2g8rjst4mg',
		'https://lbmillikan.schoolloop.com/schoolinfo',
		'https://lbmillikan.schoolloop.com/BellSched',
		'https://lbmillikan.schoolloop.com/Attendance',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1621057501101&vdid=wi54e2t1wc4tn',
		'https://lbmillikan.schoolloop.com/School_Profile',
		'https://lbmillikan.schoolloop.com/SiteCouncil',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1567840238579&vdid=li54e2a1el5hv',
		'https://lbmillikan.schoolloop.com/HonorCode',
		'https://lbmillikan.schoolloop.com/DressCode',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404120212&vdid=ii54e1y04336j',
		'https://lbmillikan.schoolloop.com/Teachers',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1619243368753&vdid=i5vc4e2sfmpd4j9',
		'https://lbmillikan.schoolloop.com/AP',
		'https://lbmillikan.schoolloop.com/slcs',
		'https://lbmillikan.schoolloop.com/compass',
		'https://lbmillikan.schoolloop.com/mbahome',
		'https://lbmillikan.schoolloop.com/sega',
		'https://lbmillikan.schoolloop.com/peace',
		'https://lbmillikan.schoolloop.com/qwelcome',
		'https://lbmillikan.schoolloop.com/LibraryInformation',
		'https://lbmillikan.schoolloop.com/citationtools',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404121768&vdid=i54e1y0432rx',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404121299&vdid=i54e02peug5i3',
		'https://lbmillikan.schoolloop.com/activities',
		'https://lbmillikan.schoolloop.com/seniors',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404122379&vdid=i54e1y80433k9',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404122317&vdid=ci54e1y0433io',
		'https://lbmillikan.schoolloop.com/MillikanStore',
		'https://millikancorydon.com/',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1614414815651&vdid=m24i54e2r2tp4nl',
		'https://lbmillikan.schoolloop.com/athletics',
		'https://lbmillikan.schoolloop.com/athleticpacket',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404122398&vdid=i5l4eg1y0434b3',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1552638646237&vdid=i854e272es258q',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404143515&vdid=i654e11y0434bk',
		'https://lbmillikan.schoolloop.com/ptsa',
		'https://lbmillikan.schoolloop.com/Counseling',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404122262&vdid=i54ke1y04337r',
		'https://lbmillikan.schoolloop.com/GradReq',
		'https://lbmillikan.schoolloop.com/FourYearPlan',
		'https://lbmillikan.schoolloop.com/HonorsAP',
		'https://lbmillikan.schoolloop.com/RevTranscripts',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404122262&vdid=7iao54em1y0433a8',
		'https://lbmillikan.schoolloop.com/Tutoring',
		'https://lbmillikan.schoolloop.com/StudyTestingStrategies',
		'https://lbmillikan.schoolloop.com/CSUUCReq',
		'https://lbmillikan.schoolloop.com/PrivateColleges',
		'https://lbmillikan.schoolloop.com/CommunityColleges',
		'https://lbmillikan.schoolloop.com/ACTSATtest',
		'https://lbmillikan.schoolloop.com/FinancialAid',
		'https://lbmillikan.schoolloop.com/Scholarships',
		'https://lbmillikan.schoolloop.com/ASVAB',
		'https://lbmillikan.schoolloop.com/NCAAClearinghouse',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534404122262&vdid=iu54e1y0433fu',
		'https://lbmillikan.schoolloop.com/CollegeCareerCenter',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1634995008665&vdid=i54e2y5bk7nz',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1634995008665&vdid=ii5w4e3o0x878ug',
		'https://lbmillikan.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972388&vdid=i54e2ncf04sq',

		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i3dmb7d1zrhqez',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=ix37d290537e3v0',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d2957e3xw',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=xi37d2srqgkt7oe',
		'https://lbpaal.schoolloop.com/administrators',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d29957e3xv',
		'https://lbpaal.schoolloop.com/preregistration',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i3e7d2vy36thrf',
		'https://lbpaal.schoolloop.com/english',
		'https://lbpaal.schoolloop.com/socialscience',
		'https://lbpaal.schoolloop.com/math',
		'https://lbpaal.schoolloop.com/art',
		'https://lbpaal.schoolloop.com/science',
		'https://lbpaal.schoolloop.com/pe',
		'https://lbpaal.schoolloop.com/interdepartmental',
		'https://lbpaal.schoolloop.com/cte',
		'https://lbpaal.schoolloop.com/familyhumanservices',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i337d2957e3y5',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=xi37d2957e3y7',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=yi37d2957e3ye',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d2957e3yg',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=ikd37d2957e3yh',
		'https://lbpaal.schoolloop.com/paallibrary',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=id537d2btm2c2gi',
		'https://lbpaal.schoolloop.com/workpermits',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d2mkwl3307',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37dqkb2ndenf3d2',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i3sn87d82x3uh42f',
		'https://lbpaal.schoolloop.com/canvaslogin',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i237wd2957e3y8',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d2957e3yb',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=4i37dr295kc7e3yc',
		'https://lbpaal.schoolloop.com/parentresources',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37vdd2liqv3mt',
		'https://lbpaal.schoolloop.com/canvasparent',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i307d2blc4bc4x4',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i307d1o23957e40k',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=ij37d2971y2w1wg',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=9in37d29y2w1xl',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d29y2w1y5',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37bd2a4t21k6',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d2lzev3k8',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37d2m4ys404',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37db2n18a3rg',
		'https://lbpaal.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i37dg2pfzys2lr',

		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267805&vdid=i52d1x4oywsr',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267805&vdid=i559g2nd2nv9g3mk',
		'https://lbpoly.schoolloop.com/Accolades',
		'https://lbpoly.schoolloop.com/Mission',
		'https://lbpoly.schoolloop.com/factsheet',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267805&vdid=i5g2od15x4ywuk',
		'https://lbpoly.schoolloop.com/staffdirectory',
		'https://lbpoly.schoolloop.com/enrollment',
		'https://lbpoly.schoolloop.com/Attendance',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267808&vdid=i52d1x4yw147',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267808&vdid=i582d1xp24yw115',
		'https://lbpoly.schoolloop.com/APbenefits',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267808&vdid=i52npd1x4u0yw17c',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1567840249796&vdid=i5xf2d2aw1hs44m',
		'https://lbpoly.schoolloop.com/polyctecourses',
		'https://www.cde.ca.gov/ci/ct/',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1616224784449&vdid=i52d2qivb34r',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267811&vdid=i52d1ze3t1n0',
		'https://lbpoly.schoolloop.com/beach',
		'https://lbpoly.schoolloop.com/CIC',
		'https://lbpoly.schoolloop.com/justice',
		'https://lbpoly.schoolloop.com/meds',
		'https://lbpaal.schoolloop.com/',
		'https://lbpoly.schoolloop.com/pacrim',
		'https://lbpoly.schoolloop.com/PACE',
		'https://lbpoly.schoolloop.com/parts',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1615965122405&vdid=i52d1x4yw1ty',
		'https://lbpoly.schoolloop.com/specialedprogram',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267808&vdid=i52d1x4yw147',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1567840249796&vdid=i5xf2d2aw1hs44m',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1616224784449&vdid=i52d2qivb34r',
		'https://lbpaal.schoolloop.com/',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267811&vdid=i52d1ze3t1n0',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1615965122405&vdid=i52d1x4yw1ty',
		'https://lbpoly.schoolloop.com/TestPrep',
		'https://lbpoly.schoolloop.com/Activities',
		'https://lbpoly.schoolloop.com/ASB',
		'https://lbpoly.schoolloop.com/clubs',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267822&vdid=id52dj1x4eyw23l',
		'https://lbpoly.schoolloop.com/JROTC',
		'https://lbpoly.schoolloop.com/seniorinformation',
		'https://lbpoly.schoolloop.com/FemaleLeadership',
		'https://lbpoly.schoolloop.com/fundraisers',
		'https://lbpoly.schoolloop.com/gradnite',
		'https://lbpoly.schoolloop.com/MaleAcademy',
		'https://lbpoly.schoolloop.com/music',
		'https://lbpoly.schoolloop.com/polynorth',
		'https://lbpoly.schoolloop.com/studentstore',
		'https://lbpoly.schoolloop.com/volunteeropportunities',
		'https://lbpoly.schoolloop.com/ASB',
		'https://lbpoly.schoolloop.com/Seniors',
		'https://lbpoly.schoolloop.com/clubs',
		'https://lbpoly.schoolloop.com/rabbotics',
		'https://lbpoly.schoolloop.com/MESA',
		'https://lbpoly.schoolloop.com/GQ',
		'https://lbpoly.schoolloop.com/JROTC',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267824&vdid=i52vdi1xe4kyw2aq',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267824&vdid=dci52d1x4oyw2b7',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267824&vdid=i52d12fx4yw2bs',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267824&vdid=i6g52sd1x4jyw2ci',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267824&vdid=i52bd1x4myw2d1',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267824&vdid=i52d1x4yw2dh',
		'https://lbpoly.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i52d2wtc95blh',
		'https://lbpoly.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=i572sd2ql0a429',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267827&vdid=ih5q2d2hgt53347',
		'https://lbpoly.schoolloop.com/clearancepacket',
		'https://lbpoly.schoolloop.com/title-IX',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267845&vdid=i582d1xx8o4yw37c',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267847&vdid=il52d1hx74yw37u',
		'https://lbpoly.schoolloop.com/carecenter',
		'https://lbpoly.schoolloop.com/collegeandcareercenter',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267847&vdid=il52d1hx74yw37u',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267847&vdid=fi52d1x4yw38l',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267847&vdid=i52dr1x4yw392',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267847&vdid=di52dt1x44qyw39i',
		'https://lbpoly.schoolloop.com/carecenter',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267850&vdid=i52d1ox4yw3ag',
		'https://lbpoly.schoolloop.com/TUPE',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267850&vdid=pi52d17cx4yw3bj',
		'https://lbpoly.schoolloop.com/collegeandcareercenter',
		'https://lbpoly.schoolloop.com/CampusAccessibility',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1614414319091&vdid=i52yd2qtyo3ir',
		'https://lbpoly.schoolloop.com/library',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267852&vdid=di52ed2ebzf3sq',
		'https://lbpoly.schoolloop.com/resources',
		'https://lbpoly.schoolloop.com/Regpackets',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973267852&vdid=i52d1x4yw3rc',
		'https://lbpoly.schoolloop.com/studentstore',
		'https://lbpoly.schoolloop.com/portal/login?d=x&return_url=1532129619051',
		'https://ca-lbusd-psv.edupoint.com/PXP2_Login_Student.aspx?CFID=924991&CFTOKEN=d25cbbf21ffdd7c-60685C6F-D94F-E7BE-D9F93B106D261F7A&regenerateSessionId=True',
		'https://genesis.lbschools.net/Login.aspx?err=1025',
		'https://lroix.lbschools.net/Account/Login?ReturnUrl=%2fHome%2f',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1579926792103&vdid=i52d1x4ibyw3he',
		'https://lbpoly.schoolloop.com/boosterclub',
		'https://lbpoly.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1536995906404&vdid=i52fod29z19540z',
		'https://lbpoly.schoolloop.com/PTSA',
		'https://lbpoly.schoolloop.com/schoolsitecouncil',

		'https://reid-lbusd-ca.schoolloop.com/admin',
		'https://reid-lbusd-ca.schoolloop.com/office',
		'https://reid-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534750201640&vdid=i9b1y4hl1gf',
		'https://reid-lbusd-ca.schoolloop.com/bell',
		'https://reid-lbusd-ca.schoolloop.com/truancy',
		'https://reid-lbusd-ca.schoolloop.com/2018-Grads',
		'https://reid-lbusd-ca.schoolloop.com/parents',
		'https://reid-lbusd-ca.schoolloop.com/newsletter',
		'https://reid-lbusd-ca.schoolloop.com/resources',
		'https://reid-lbusd-ca.schoolloop.com/reidinformation',
		'https://reid-lbusd-ca.schoolloop.com/technologyuse',
		'https://reid-lbusd-ca.schoolloop.com/resources',

		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246735&vdid=loi37e1xlxwywb',
		'https://lbrhsa.schoolloop.com/principalsmessage',
		'https://lbrhsa.schoolloop.com/RHSAhistory',
		'https://lbrhsa.schoolloop.com/missionvission',
		'https://lbrhsa.schoolloop.com/directory',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246731&vdid=i3770e2vy6t10j1',
		'https://lbrhsa.schoolloop.com/video',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246740&vdid=i3p7e81xxwywx',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246740&vdid=i3p7e81xxwywx',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246740&vdid=i37e1xxwyxh',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246740&vdid=i37e1xxwyyz',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246740&vdid=i37he1xxwy10q',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246741&vdid=4si37e1xxwy117',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=qi37e1xxwy17e',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=i37e1xbxwy11n',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=i375eg1nxxwy13e',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=i3o7be1xxwy16r',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=ufi37e1xxwy12p',
		'https://lbrhsa.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=fiwl37e2y9fc2lf',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=iy37e1xxwy13z',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=i37e1xxwy15s',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246736&vdid=i373e1x57vxwy18d',
		'https://lbrhsa.schoolloop.com/English',
		'https://lbrhsa.schoolloop.com/mathdept',
		'https://lbrhsa.schoolloop.com/pe',
		'https://lbrhsa.schoolloop.com/science',
		'https://lbrhsa.schoolloop.com/specialed',
		'https://lbrhsa.schoolloop.com/socialscience',
		'https://lbrhsa.schoolloop.com/spanish',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246742&vdid=i37e1gxxwy1fj',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246751&vdid=i37e1r0wxxwy1gd',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246751&vdid=i37e1xxwy1h2',
		'https://lbrhsa.schoolloop.com/financialaid',
		'https://lbrhsa.schoolloop.com/Scholarships',
		'https://lbrhsa.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1534231246751&vdid=i30k7e1xrxwy1ii',
		'https://lbrhsa.schoolloop.com/satactexams',
		'https://lbrhsa.schoolloop.com/resourcesundocumentedstudents',
		'https://lbrhsa.schoolloop.com/fosteryouth',
		'https://lbrhsa.schoolloop.com/studentcouncil',
		'https://lbrhsa.schoolloop.com/clubs',
		'https://lbrhsa.schoolloop.com/studentstore',
		'https://lbrhsa.schoolloop.com/tardy&earlyouts',
		'https://lbrhsa.schoolloop.com/rulespolicies',
		'https://lbrhsa.schoolloop.com/schoolsitecouncil',
		'https://lbrhsa.schoolloop.com/partsboosterclub',
		'https://lbrhsa.schoolloop.com/parentvue',

		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693691&vdid=i52a2yrcs50c',
		'https://sato-lbusd-ca.schoolloop.com/Eunice',
		'https://sato-lbusd-ca.schoolloop.com/reopening',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693691&vdid=i52pa1kxpcs0hb7',
		'https://sato-lbusd-ca.schoolloop.com/calendar',
		'https://sato-lbusd-ca.schoolloop.com/BellSchedule',
		'https://sato-lbusd-ca.schoolloop.com/sato_planner',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693691&vdid=pxi52a16exp0har',
		'https://sato-lbusd-ca.schoolloop.com/ssc',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693691&vdid=is52a1xp0hc5',
		'https://sato-lbusd-ca.schoolloop.com/lbusd',
		'https://sato-lbusd-ca.schoolloop.com/satosalutes',
		'https://sato-lbusd-ca.schoolloop.com/SARC',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693691&vdid=i5r2ga2ovo87240',
		'https://sato-lbusd-ca.schoolloop.com/requiredcourseofstudy',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693693&vdid=5i582pa41xp0hgc',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693693&vdid=i5m2aqe2e45i113',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693693&vdid=i0o5m2a1dxp0hgs',
		'https://sato-lbusd-ca.schoolloop.com/mathematics',
		'https://sato-lbusd-ca.schoolloop.com/physicaleducation',
		'https://sato-lbusd-ca.schoolloop.com/science',
		'https://sato-lbusd-ca.schoolloop.com/socialscience',
		'https://sato-lbusd-ca.schoolloop.com/worldlanguages',
		'https://sato-lbusd-ca.schoolloop.com/biomedical',
		'https://sato-lbusd-ca.schoolloop.com/engineering',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693693&vdid=iy52a1xp0hje',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693694&vdid=viy252a1xp0hkf',
		'https://docs.google.com/presentation/d/17k2baz1TtfqNj5FmabOMrP1l8lRlBLKHPichdX3Nr7I/edit',
		'https://sato-lbusd-ca.schoolloop.com/parentresources',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693694&vdid=i52ba2vy51753kz',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2_site/viewFirstPageOfMenuSection?d=x&id=ilmu52a2bqrpi16w',
		'https://sato-lbusd-ca.schoolloop.com/graduation',
		'https://sato-lbusd-ca.schoolloop.com/dragonsden',
		'https://sato-lbusd-ca.schoolloop.com/9th',
		'https://sato-lbusd-ca.schoolloop.com/freshmenresources',
		'https://sato-lbusd-ca.schoolloop.com/dragon_crew',
		'https://sato-lbusd-ca.schoolloop.com/sophomoreresources',
		'https://sato-lbusd-ca.schoolloop.com/juniors',
		'https://sato-lbusd-ca.schoolloop.com/seniors',
		'https://sato-lbusd-ca.schoolloop.com/onlineaccounts',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693697&vdid=i52a1xp0hrd',
		'https://sato-lbusd-ca.schoolloop.com/forms',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693697&vdid=i52a1xup0htg',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693696&vdid=i52a2eby4yt',
		'https://sato-lbusd-ca.schoolloop.com/counseling',
		'https://sato-lbusd-ca.schoolloop.com/scholarships',
		'https://sato-lbusd-ca.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1531973693696&vdid=i529a2e5by4zd',
		'https://sato-lbusd-ca.schoolloop.com/summerprograms',
		'https://sato-lbusd-ca.schoolloop.com/ASB',
		'https://sato-lbusd-ca.schoolloop.com/clubs',
		'https://sato-lbusd-ca.schoolloop.com/intramurals',
		'https://sato-lbusd-ca.schoolloop.com/businesspartnerships',
		'https://sato-lbusd-ca.schoolloop.com/competitions',
		'https://sato-lbusd-ca.schoolloop.com/workbasedlearning',
		'https://sato-lbusd-ca.schoolloop.com/advisoryboard',
		'https://sato-lbusd-ca.schoolloop.com/alumni',

		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455832&vdid=ix55ca1wjtxp3z4',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455832&vdid=8i55c1wjxp3zo',
		'https://lbwilson.schoolloop.com/Alumni',
		'https://lbwilson.schoolloop.com/campusaccess',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455832&vdid=il455hc1wjxp41u',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455832&vdid=i5b5uc1wjxp46l',
		'https://lbwilson.schoolloop.com/sarc',
		'https://lbwilson.schoolloop.com/schoolsitecouncil',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455832&vdid=i555c28ln7323u',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455839&vdid=i46i55yc1wjxp48d',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455832&vdid=ik55c1wvljvxp48t',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455832&vdid=i558c1w3jxp49t',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455662&vdid=if955kc12wjxpz4',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455662&vdid=i55c1wjxpzn',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455662&vdid=bi5u5c1twjxp125',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455662&vdid=i55c1wjxp14f',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455662&vdid=i55c1wjxp15l',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455662&vdid=wi55ec1wmjxp16l',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=i545c1wjxp18k',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455666&vdid=i55c1wjxp1az',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=mi5l5c1w2juxp1kn',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=ic559c1cwjxp1lv',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=i85b5cc1wjxp1ml',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=i55c1wjxp1n3',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=ie55c1cwjxp1o0',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=ic55cv1wfjxp1ol',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=i525ac1wjjxp1qv',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455657&vdid=gir55c1wjxp179',
		'https://lbwilson.schoolloop.com/activities',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455810&vdid=i3o55sc1wjxp23d',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455810&vdid=i55cx1wjm4xp240',
		'https://lbwilson.schoolloop.com/campanile',
		'https://lbwilson.schoolloop.com/club',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455810&vdid=i5v5qc1kwbjxp25x',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455810&vdid=i55xc1wjxp26g',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455810&vdid=i655clc1wj4xp273',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455810&vdid=vij55c1w8j9xp27q',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455810&vdid=2i55cj1wtjxp29g',
		'https://lbwilson.schoolloop.com/athletics',
		'https://lbwilson.schoolloop.com/athleticclearance',
		'https://lbwilson.schoolloop.com/athleticstaffdirectory',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1563002540363&vdid=i55c2w18gth35y',
		'https://lbwilson.schoolloop.com/wilsonncaa',
		'https://lbwilson.schoolloop.com/summercamp',
		'https://lbwilson.schoolloop.com/bruinettes',
		'https://lbwilson.schoolloop.com/title-IX',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1563866270921&vdid=i55c28hwb2ri',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455788&vdid=i55c1w7jxp1re',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455788&vdid=i55c2dzap754l',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455791&vdid=ib55rc1wjxp1s9',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455866&vdid=i55c1fw7jxp4gl',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455866&vdid=i55c2xpx23to',
		'https://lbwilson.schoolloop.com/servicelearning',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279710186&vdid=i55c20a33bu1t8',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279709583&vdid=ki55c22p1659f',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279709583&vdid=i55ci1zqb32m0',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279709583&vdid=i55c2bc2k4cd',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279710344&vdid=i5f5c2n6uq342',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1540279710284&vdid=i55tc203wvi572d7',
		'https://www.lbschools.net/Departments/Student_Support_Services/frc.cfm',
		'https://wilsonhscollegeadvisers.ucraft.site/',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455870&vdid=i55c1wjxp4ke',
		'https://lbwilson.schoolloop.com/library_resources',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455870&vdid=i455c1yzn52ms',
		'https://lbwilson.schoolloop.com/databases',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455842&vdid=i5q5c1ww1jxp4do',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455842&vdid=i55c1wjxp4ag',
		'https://lbwilson.schoolloop.com/cafecitos',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455842&vdid=i55c1wjxp4d2',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455842&vdid=i55qcv1hiwjxp4er',
		'https://docs.google.com/presentation/d/15HKDbyR51bgiunl0I5KXTH_h4ZDvwDyRC0yhOc7JMQU/edit?usp=sharing',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972306&vdid=di55c288a363ed',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972306&vdid=ai55gc28ax363gg',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972306&vdid=i55wkc28ap363hb',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972306&vdid=3i55tc28bs9i2vh',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972306&vdid=i55c28l731ys',
		'https://lbwilson.schoolloop.com/wellness',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972306&vdid=i550c1wjxp41d',
		'https://lbwilson.schoolloop.com/attendancepolicies',
		'https://lbwilson.schoolloop.com/attendance',
		'https://lbwilson.schoolloop.com/codeofhonor',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1530380455837&vdid=i55c1wjxp45o',
		'https://lbwilson.schoolloop.com/dresscode',
		'https://lbwilson.schoolloop.com/skateboards',
		'https://lbwilson.schoolloop.com/visitationpolicy',
		'https://lbwilson.schoolloop.com/pf4/cms2/view_page?d=x&group_id=1500178972306&vdid=ik55c1wjxp47e',
		'https://lbwilson.schoolloop.com/health',
		'https://lbwilson.schoolloop.com/wellness',
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
