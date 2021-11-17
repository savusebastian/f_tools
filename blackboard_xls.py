from pathlib import Path
from time import time
import csv
import re

from bs4 import BeautifulSoup
import requests
import xlwt


def remove_attrs(tags):
	for tag in tags:
		del tag['align']
		del tag['aria-controls']
		del tag['aria-disabled']
		del tag['aria-expanded']
		del tag['aria-hidden']
		del tag['aria-label']
		del tag['border']
		del tag['checked']
		del tag['class']
		del tag['cs-data']
		del tag['data-height']
		del tag['data-firstname']
		del tag['data-image-height']
		del tag['data-image-width']
		del tag['data-lastname']
		del tag['data-phone']
		del tag['data-room']
		del tag['data-shared-department']
		del tag['data-site']
		del tag['data-target']
		del tag['data-toggle']
		del tag['data-value']
		del tag['data-width']
		del tag['dir']
		del tag['for']
		del tag['height']
		del tag['onerror']
		del tag['id']
		del tag['itemid']
		del tag['name']
		del tag['rel']
		del tag['role']
		del tag['summary']
		del tag['start']
		del tag['style']
		del tag['tabindex']
		del tag['title']
		del tag['type']
		del tag['value']


def remove_tags(text):
	div = re.compile(r'<div[^>]+>')
	dive = re.compile(r'<div+>')
	divc = re.compile(r'</div+>')
	span = re.compile(r'<span+>')
	spane = re.compile(r'<span[^>]+>')
	spanc = re.compile(r'</span+>')

	text = div.sub('', text)
	text = dive.sub('', text)
	text = divc.sub('', text)
	text = span.sub('', text)
	text = spane.sub('', text)
	text = spanc.sub('', text)

	return text.strip()


def get_column(col, splitter, mainfolder, school):
	col_forms = col.find_all('form')
	col_images = col.find_all('img')
	col_links = col.find_all('a')
	i = 0
	ii = ''
	d = 0
	id = ''

	while col.link != None:
		col.link.decompose()

	while col.script != None:
		col.script.decompose()

	while col.style != None:
		col.style.decompose()

	while col.nav != None:
		col.nav.decompose()

	with open('resources_dump.csv', 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		for image in col_images:
			try:
				if image.get('src') != None and image.get('src') != '':
					extension = str(image.get('src')).split('/')[-1].split('.')[-1]

					if len(extension) < 5:
						filename = str(image.get('src')).split('/')[-1].replace(' ', '').replace('`', '').replace('~', '').replace('!', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('+', '').replace('=', '').replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace('?', '').replace(',', '').replace('<', '').replace('>', '')

						while len(filename.split('.')) > 2:
							filename = filename.replace('.', '', 1)

					else:
						filename = str(image.get('src')).split('/')[-1].split('?')[0].replace(' ', '').replace('`', '').replace('~', '').replace('!', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('+', '').replace('=', '').replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace('?', '').replace(',', '').replace('<', '').replace('>', '')

						while len(filename.split('.')) > 2:
							filename = filename.replace('.', '', 1)

					if image.get('src')[:6] == '../../':
						try:
							response = requests.get(str(splitter[0] + '//' + splitter[2] + image.get('src')[5:]), timeout=30)

							with open('../f_web_interface/static/files/' + mainfolder + '/' + school + '/images/' + filename, 'wb') as f:
								f.write(response.content)
								i += 1

						except:
							ii += splitter[0] + '//' + splitter[2] + image.get('src')[5:] + '\n'
							print('1 Failed:', splitter[0] + '//' + splitter[2] + image.get('src')[5:])

					elif image.get('src')[0] == '/':
						try:
							response = requests.get(str(splitter[0] + '//' + splitter[2] + image.get('src')), timeout=30)

							with open('../f_web_interface/static/files/' + mainfolder + '/' + school + '/images/' + filename, 'wb') as f:
								f.write(response.content)
								i += 1

						except:
							ii += splitter[0] + '//' + splitter[2] + image.get('src') + '\n'
							print('2 Failed:', splitter[0] + '//' + splitter[2] + image.get('src'))

					else:
						try:
							response = requests.get(str(image.get('src')), timeout=30)

							with open('../f_web_interface/static/files/' + mainfolder + '/' + school + '/images/' + filename, 'wb') as f:
								f.write(response.content)
								i += 1

						except:
							ii += image.get('src') + '\n'
							print('3 Failed:', image.get('src'))

					# for row in csv_reader:
					#	 if filename == row[0].split('/')[-1]:
					#		 image['data-resource-uuid'] = row[1]
					#		 image['src'] = row[2]
					#		 image['data-image-sizes'] = row[3].replace(':u', '%22u').replace(':w', '%22w').replace('"', '%22').replace('=', '%22').replace('>', ':')
					#		 image['data-resource-filename'] = filename

				# del image['id']
				# del image['role']
				# del image['style']
				# del image['width']
				del image['data-image-sizes']
				del image['data-resource-filename']
				del image['data-resource-uuid']

				image['id'] = ''
				image['role'] = 'presentation'
				image['style'] = ''
				image['width'] = '250'

				del image['align']
				del image['aria-hidden']
				del image['border']
				del image['class']
				del image['cs-data']
				del image['data-firstname']
				del image['data-lastname']
				del image['data-image-height']
				del image['data-image-width']
				del image['data-height']
				del image['data-width']
				del image['height']
				del image['onerror']

			except:
				print('Image:', image)

		for link in col_links:
			try:
				if link.get('href') != None and link.get('href') != '':
					extension = str(link.get('href')).split('.')[-1]

					if str(link.get('href')).find('=') != -1:
						filename = str(link.get('href')).split('=')[-1].replace(' ', '').replace('`', '').replace('~', '').replace('!', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('+', '').replace('=', '').replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace('?', '').replace(',', '').replace('<', '').replace('>', '')

						while len(filename.split('.')) > 2:
							filename = filename.replace('.', '', 1)

					else:
						filename = str(link.get('href')).split('/')[-1].replace(' ', '').replace('`', '').replace('~', '').replace('!', '').replace('@', '').replace('#', '').replace('$', '').replace('%', '').replace('^', '').replace('&', '').replace('+', '').replace('=', '').replace('"', '').replace("'", '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace('?', '').replace(',', '').replace('<', '').replace('>', '')

						while len(filename.split('.')) > 2:
							filename = filename.replace('.', '', 1)

					if link.get('href')[:6] == '../../':
						if extension == 'pdf' or extension == 'doc' or extension == 'docx' or extension == 'xls' or extension == 'xlsx' or extension == 'ppt' or extension == 'pptx' or extension == 'txt':
							try:
								response = requests.get(str(splitter[0] + '//' + splitter[2] + link.get('href')[5:]), timeout=30)

								with open('../f_web_interface/static/files/' + mainfolder + '/' + school + '/docs/' + filename, 'wb') as f:
									f.write(response.content)
									d += 1

							except:
								id += str(splitter[0] + '//' + splitter[2] + link.get('href')[5:]) + '\n'
								print('1 Failed:', splitter[0] + '//' + splitter[2] + link.get('href')[5:])

					elif link.get('href')[0] == '/':
						if extension == 'pdf' or extension == 'doc' or extension == 'docx' or extension == 'xls' or extension == 'xlsx' or extension == 'ppt' or extension == 'pptx' or extension == 'txt':
							try:
								response = requests.get(str(splitter[0] + '//' + splitter[2] + link.get('href')), timeout=30)

								with open('../f_web_interface/static/files/' + mainfolder + '/' + school + '/docs/' + filename, 'wb') as f:
									f.write(response.content)
									d += 1

							except:
								id += str(splitter[0] + '//' + splitter[2] + link.get('href')) + '\n'
								print('2 Failed:', splitter[0] + '//' + splitter[2] + link.get('href'))

					else:
						if extension == 'pdf' or extension == 'doc' or extension == 'docx' or extension == 'xls' or extension == 'xlsx' or extension == 'ppt' or extension == 'pptx' or extension == 'txt':
							try:
								response = requests.get(str(link.get('href')), timeout=30)

								with open('../f_web_interface/static/files/' + mainfolder + '/' + school + '/docs/' + filename, 'wb') as f:
									f.write(response.content)
									d += 1

							except:
								id += str(link.get('href')) + '\n'
								print('3 Failed:', link.get('href'))

					# for row in csv_reader:
					#	 if filename == row[0].split('/')[-1]:
					#		 link['data-resource-uuid'] = row[1]
					#		 link['href'] = row[2]
					#		 link['data-resource-filename'] = filename
					#		 link['target'] = '_blank'

				# if link.get('href')[0] != 'h' and link.string != None:
				# 	initial_text = link.get_text()
				# 	link.string.replace_with(initial_text + ' INTERNAL LINK')

				del link['data-file-sizes']
				del link['data-resource-filename']
				del link['data-resource-uuid']

				del link['align']
				del link['aria-controls']
				del link['aria-disabled']
				del link['aria-expanded']
				del link['aria-label']
				del link['class']
				del link['contenteditable']
				del link['data-event']
				del link['data-height']
				del link['data-phone']
				del link['data-target']
				del link['data-toggle']
				del link['data-width']
				del link['id']
				del link['rel']
				del link['role']
				del link['style']
				del link['tabindex']
				del link['title']
				del link['type']

			except:
				print('Link:', link)

	col_tags = col.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'p', 'table', 'em', 'strong', 'br', 'hr', 'fieldset', 'label', 'input', 'legend'])
	remove_attrs(col_tags)
	col = remove_tags(str(col))
	column = col

	return column, i, ii, d, id, col_forms


def get_content(web_page, splitter, mainfolder, school):
	content_i = 0
	content_ii = ''
	content_d = 0
	content_id = ''
	issue_pages_counter = 0
	issue_pages_links = ''

	if web_page[0] == '/' and web_page[1] == '/':
		web_page = splitter[0] + web_page

	if web_page[0] == '/':
		web_page = splitter[0] + '//' + splitter[2] + web_page

	try:
		web_link = requests.get(web_page)
		web_soup = BeautifulSoup(web_link.content, 'html.parser')

		col1 = web_soup.find(id='sw-content-container1')
		page_nav = None
		col_num = ''
		forms = ''
		meta_title = ''
		meta_keywords = ''
		meta_desc = ''

		if web_soup.find_all('meta', attrs={'name': 'title'}) != []:
			meta_title = str(web_soup.find_all('meta', attrs={'name': 'title'}))

		if web_soup.find_all('meta', attrs={'name': 'keywords'}) != []:
			meta_keywords = str(web_soup.find_all('meta', attrs={'name': 'keywords'}))

		if web_soup.find_all('meta', attrs={'name': 'description'}) != []:
			meta_desc = str(web_soup.find_all('meta', attrs={'name': 'description'}))

		if web_soup.find(class_='section-navigation') != None:
			page_nav = web_soup.find(class_='section-navigation').find_all('a')
		elif web_soup.find(class_='page-navigation') != None:
			page_nav = web_soup.find(class_='page-navigation').find_all('a')

		# First column
		if col1 != None and col1 != '':
			col1, i, ii, d, id, forms1 = get_column(col1, splitter, mainfolder, school)
			col_num = 'One column'
			content_i += i
			content_ii += ii
			content_d += d
			content_id += id

			if forms1 != []:
				forms = 'form'

		if col1 == None:
			col1 = 'Flagged'
			issue_pages_counter = 1
			issue_pages_links += web_page + '\n'

		col1 = str(col1)

		# Second Column
		if web_soup.find(id='sw-content-container2') != None and web_soup.find(id='sw-content-container2') != '':
			col2 = web_soup.find(id='sw-content-container2')
			col2, i, ii, d, id, forms2 = get_column(col2, splitter, mainfolder, school)
			col_num = 'Two column'
			content_i += i
			content_ii += ii
			content_d += d
			content_id += id

			if forms2 != []:
				forms = 'form'

		else:
			col2 = ''

		if web_soup.find(id='sw-content-container3') != None and web_soup.find(id='sw-content-container3') != '':
			col3 = web_soup.find(id='sw-content-container3')
			col3, i, ii, d, id, forms3 = get_column(col3, splitter, mainfolder, school)
			col_num = 'Two column'
			content_i += i
			content_ii += ii
			content_d += d
			content_id += id

			if forms3 != []:
				forms = 'form'

		else:
			col3 = ''

		if web_soup.find(id='sw-content-container4') != None and web_soup.find(id='sw-content-container4') != '':
			col4 = web_soup.find(id='sw-content-container4')
			col4, i, ii, d, id, forms4 = get_column(col4, splitter, mainfolder, school)
			col_num = 'Two column'
			content_i += i
			content_ii += ii
			content_d += d
			content_id += id

			if forms4 != []:
				forms = 'form'

		else:
			col4 = ''

		col2 = str(col2) + str(col3) + str(col4)

		if len(col1) > 50000 or len(col2) > 50000:
			col1 = 'Flagged'
			col2 = 'This page has more than 50000 chars'
			issue_pages_counter = 1
			issue_pages_links += web_page + '\n'

		return col1, col2, col3, col4, col_num, page_nav, forms, meta_title, meta_keywords, meta_desc, content_i, content_ii, content_d, content_id, issue_pages_counter

	except:
		issue_pages_counter = 1
		issue_pages_links += web_page + '\n'

		return 'Flagged', '', '', '', '', '', '', '', content_i, content_ii, content_d, content_id, issue_pages_counter


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		# 'https://www.satsumaschools.com/site/default.aspx?pagetype=15&SiteID=4&DirectoryType=6&SectionMax=15',
		'https://www.satsumaschools.com/site/default.aspx?pagetype=15&SiteID=8&DirectoryType=6&SectionMax=15',
		# 'https://www.satsumaschools.com/site/default.aspx?pagetype=15&SiteID=9&DirectoryType=6&SectionMax=15'
		# 'https://www.mooreschools.com/site/Default.aspx?PageType=15&SiteID=1&SectionMax=15&DirectoryType=6',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=4848&DirectoryType=6&SectionMax=15',
		# 'https://www.mooreschools.com/site/default.aspx?pagetype=15&SiteID=2244&DirectoryType=6&SectionMax=15'
		# 'https://www.cherrycreekschools.org/site/Default.aspx?PageType=15&SiteID=4&SectionMax=40&DirectoryType=6',
		# 'https://www.cherrycreekschools.org/site/default.aspx?pagetype=15&SiteID=8&DirectoryType=6&SectionMax=40',
		# 'https://www.cherrycreekschools.org/site/default.aspx?pagetype=15&SiteID=9&DirectoryType=6&SectionMax=40'
		# 'https://www.senecafallscsd.org/site/Default.aspx?PageType=15&SiteID=8&SectionMax=15&DirectoryType=6',
		# 'https://www.senecafallscsd.org/site/default.aspx?pagetype=15&SiteID=140&DirectoryType=6&SectionMax=15',
		# 'https://www.senecafallscsd.org/site/default.aspx?pagetype=15&SiteID=205&DirectoryType=6&SectionMax=15',
		# 'https://www.senecafallscsd.org/site/default.aspx?pagetype=15&SiteID=244&DirectoryType=6&SectionMax=15',
		# 'https://www.senecafallscsd.org/site/default.aspx?pagetype=15&SiteID=286&DirectoryType=6&SectionMax=15'
		# 'https://www.shorelineschools.org/site/Default.aspx?PageType=15&SiteID=4&SectionMax=15&DirectoryType=6',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=8&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=9&DirectoryType=6&SectionMax=15'
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=21&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=10&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=22&DirectoryType=6&SectionMax=15'
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=17&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=11&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=23&DirectoryType=6&SectionMax=15'
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=18&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=12&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=13&DirectoryType=6&SectionMax=15'
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=14&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=15&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=19&DirectoryType=6&SectionMax=15'
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=20&DirectoryType=6&SectionMax=15',
		# 'https://www.shorelineschools.org/site/default.aspx?pagetype=15&SiteID=16&DirectoryType=6&SectionMax=15'
	]
	mainfolder = all_sites[0].split('.')[1]
	main_folder = Path(f'../f_web_interface/static/files/{mainfolder}')
	main_folder.mkdir(parents=True, exist_ok=True)
	wb = xlwt.Workbook()

	for site in all_sites:
		page_counter = 0
		issue_pages_counter = 0
		issue_pages_links = ''
		image_counter = 0
		issue_images = ''
		doc_counter = 0
		issue_docs = ''

		URL = site
		splitter = URL.split('/')
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')
		sitemap = soup.find(id='sw-sitemap')
		list_items = sitemap.select('li.sw-sitemap-channel-item')
		school = soup.find(id='sw-sitemap-sitelist').find('option', selected='selected').get_text()

		if len(school) > 30:
			ws = wb.add_sheet(f'{school[:30]}')
		else:
			ws = wb.add_sheet(f'{school}')

		i = 0
		ws.write(i, 0, 'Link to page')
		ws.write(i, 1, 'Tier 1')
		ws.write(i, 2, 'Tier 2')
		ws.write(i, 3, 'Tier 3')
		ws.write(i, 4, 'Tier 4')
		ws.write(i, 5, 'Column Count')
		ws.write(i, 6, 'Column 1')
		ws.write(i, 7, 'Column 2')
		ws.write(i, 8, 'Meta title')
		ws.write(i, 9, 'Meta keywords')
		ws.write(i, 10, 'Meta description')
		ws.write(i, 11, 'form')
		i += 1

		filepath = Path(f'../f_web_interface/static/files/{mainfolder}/{school}/images')
		filepath.mkdir(parents=True, exist_ok=True)
		filepath = Path(f'../f_web_interface/static/files/{mainfolder}/{school}/docs')
		filepath.mkdir(parents=True, exist_ok=True)

		for item in list_items[1:]:
			group_links = item.find_all('a')

			for link in group_links:
				page_counter += 1

				if link.get('href')[0] == '/' and link.get('href')[1] == '/':
					ws.write(i, 0, splitter[0] + link.get('href'))
				elif link.get('href')[0] == '/':
					ws.write(i, 0, splitter[0] + '//' + splitter[2] + link.get('href'))
				else:
					ws.write(i, 0, link.get('href'))

				ws.write(i, 1, group_links[0].get_text())

				if group_links[0].get_text() != link.get_text():
					ws.write(i, 2, link.get_text())

				col1, col2, col3, col4, col_num, nav_sec, forms, meta_title, meta_keywords, meta_desc, content_i, content_ii, content_d, content_id, content_ipc, content_ipl = get_content(link.get('href'), splitter, mainfolder, school)
				image_counter += content_i
				issue_images += content_ii
				doc_counter += content_d
				issue_docs += content_id
				issue_pages_counter += content_ipc
				issue_pages_links += content_ipl
				ws.write(i, 5, col_num)
				ws.write(i, 6, col1)
				ws.write(i, 7, col2)

				if len(meta_title) > 50000 or len(meta_keywords) > 50000 or len(meta_desc) > 50000:
					ws.write(i, 8, 'Too much meta content on this page')

				else:
					ws.write(i, 8, meta_title)
					ws.write(i, 9, meta_keywords)
					ws.write(i, 10, meta_desc)

				ws.write(i, 11, forms)

				if nav_sec != None and nav_sec != '' and nav_sec != []:
					for nav_link in nav_sec:
						page_counter += 1
						i += 1
						nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, forms, meta_title, meta_keywords, meta_desc, content_i, content_ii, content_d, content_id, content_ipc, content_ipl = get_content(nav_link.get('href'), splitter, mainfolder, school)
						image_counter += content_i
						issue_images += content_ii
						doc_counter += content_d
						issue_docs += content_id
						issue_pages_counter += content_ipc
						issue_pages_links += content_ipl

						if nav_link.get('href')[0] == '/' and nav_link.get('href')[1] == '/':
							ws.write(i, 0, splitter[0] + nav_link.get('href'))
						elif nav_link.get('href')[0] == '/':
							ws.write(i, 0, splitter[0] + '//' + splitter[2] + nav_link.get('href'))
						else:
							ws.write(i, 0, nav_link.get('href'))

						ws.write(i, 1, group_links[0].get_text())
						ws.write(i, 2, link.get_text())
						ws.write(i, 3, nav_link.get_text())
						ws.write(i, 5, nav_col_num)
						ws.write(i, 6, nav_col1)
						ws.write(i, 7, nav_col2)

						if len(meta_title) > 50000 or len(meta_keywords) > 50000 or len(meta_desc) > 50000:
							ws.write(i, 8, 'Too much meta content on this page')

						else:
							ws.write(i, 8, meta_title)
							ws.write(i, 9, meta_keywords)
							ws.write(i, 10, meta_desc)

						ws.write(i, 11, forms)

				i += 1

		i += 1
		ws.write(i, 0, 'Pages scraped')
		ws.write(i, 1, page_counter)
		i += 1

		ws.write(i, 0, 'Issues')
		ws.write(i, 1, issue_pages_counter)
		ws.write(i, 2, issue_pages_links)
		i += 1

		ws.write(i, 0, 'Images downloaded')
		ws.write(i, 1, image_counter)
		ws.write(i, 2, issue_images)
		i += 1

		ws.write(i, 0, 'Docs downloaded')
		ws.write(i, 1, doc_counter)
		ws.write(i, 2, issue_docs)
		i += 1

		print('Finished:', site)

	wb.save(mainfolder + '/blackboard.xls')
	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
