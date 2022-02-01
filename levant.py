from pathlib import Path
from time import time
import csv

from bs4 import BeautifulSoup
import requests

from util import get_column


# def download_file(url, mainfolder, school, folder, filename):
# 	try:
# 		response = requests.get(url, timeout=30)
#
# 		with open('../f_web_interface/static/files/' + mainfolder + '/' + school + folder + filename, 'wb') as f:
# 			f.write(response.content)
#
# 	except:
# 		ii += url + '\n'
# 		print('Failed:', url)


if __name__ == '__main__':
	start_time = time()
	all_sites = [
		'https://www.ccosa.org',
	]
	mainfolder = all_sites[0].split('.')[1]
	filepath = Path(f'../f_web_interface/static/files/{mainfolder}')
	filepath.mkdir(parents=True, exist_ok=True)

	with open('../f_web_interface/static/files/' + mainfolder + '/report.csv', 'w', encoding='utf-8') as csv_report:
		csv_report = csv.writer(csv_report)

		for site in all_sites:
			page_counter = 0
			issue_pages_counter = 0
			# issue_pages_links = ''
			# issue_images = ''
			# issue_docs = ''

			splitter = site.split('/')
			page = requests.get(site).content
			soup = BeautifulSoup(page, 'html.parser')
			sitemap = soup.find_all(class_='navbar-nav')
			list_items = sitemap[0].select('li')
			school = site.split('.')[1]

			if len(school) > 30:
				school_name = str(school[:30]).lower().replace(' ', '_').replace('.', '')
			else:
				school_name = str(school).lower().replace(' ', '_').replace('.', '')

			csv_report.writerow(['School name', school_name])
			# filepath = Path(f'../f_web_interface/static/files/{mainfolder}/{school_name}/images')
			# filepath.mkdir(parents=True, exist_ok=True)
			# filepath = Path(f'../f_web_interface/static/files/{mainfolder}/{school_name}/docs')
			# filepath.mkdir(parents=True, exist_ok=True)

			with open('../f_web_interface/static/files/' + mainfolder + '/' + school_name + '.csv', 'w', encoding='utf-8') as csv_main:
				csv_writer = csv.writer(csv_main)
				csv_writer.writerow(['Link to page', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 4', 'Column Count', 'Column 1', 'Column 2', 'Column 3', 'Column 4', 'Meta title', 'Meta keywords', 'Meta description'])

				for item in list_items[1:]:
					group_links = item.find_all('a')

					for link in group_links:
						external_link = False

						if link.get('href')[0] == '#':
							page_link = '#'
						elif len(link.get('href')) > 1 and link.get('href')[:2] == '//':
							page_link = splitter[0] + link.get('href')
						elif link.get('href')[0] == '/':
							page_link = splitter[0] + '//' + splitter[2] + link.get('href')
						elif link.get('href')[:4] == 'http':
							page_link = link.get('href')

							if link.get('href').find(splitter[2].split('.')[1]) == -1:
								external_link = True
						else:
							page_link = splitter[0] + '//' + splitter[2] + '/' + link.get('href')

						if not external_link:
							page_counter += 1
							# col1, col2, col3, col4, col_num, nav_sec, nav_sec2, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ii, content_id, content_ipc, content_ipl = get_content(page_link)
							col1, col2, col3, col4, col_num, nav_sec, nav_sec2, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link, splitter)
							# issue_images += content_ii
							# issue_docs += content_id
							issue_pages_counter += content_ipc
							# issue_pages_links += content_ipl

							if group_links[0].get_text() != link.get_text():
								csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), '', '', col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])
							else:
								csv_writer.writerow([str(page_link), str(group_links[0].get_text()), '', '', '', col_num, col1, col2, col3, col4, meta_title, meta_keywords, meta_desc])

							if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
								csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])

							if nav_sec != None and nav_sec != '' and nav_sec != []:
								for nav_link in nav_sec:
									external_link = False

									if nav_link.get('href')[0] == 'i':
										page_link = splitter[0] + '//' + splitter[2] + '/' + nav_link.get('href')
									elif len(nav_link.get('href')) > 1 and nav_link.get('href')[:2] == '//':
										page_link = splitter[0] + nav_link.get('href')
									elif nav_link.get('href')[0] == '/':
										page_link = splitter[0] + '//' + splitter[2] + nav_link.get('href')
									elif nav_link.get('href')[:4] == 'http':
										page_link = nav_link.get('href')

										if nav_link.get('href').find(splitter[2].split('.')[1]) == -1:
											external_link = True
									else:
										page_link = splitter[0] + '//' + splitter[2] + '/' + nav_link.get('href')

									if not external_link:
										page_counter += 1
										# nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ii, content_id, content_ipc, content_ipl = get_content(page_link)
										nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
										# issue_images += content_ii
										# issue_docs += content_id
										issue_pages_counter += content_ipc
										# issue_pages_links += content_ipl
										csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])

										if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
											csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])
									else:
										csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', '1', 'Linked page', '', '', '', '', '', ''])

							if nav_sec2 != None and nav_sec2 != '' and nav_sec2 != []:
								for nav_link in nav_sec2:
									external_link = False

									if nav_link.get('href')[0] == 'i':
										page_link = splitter[0] + '//' + splitter[2] + '/' + nav_link.get('href')
									elif len(nav_link.get('href')) > 1 and nav_link.get('href')[:2] == '//':
										page_link = splitter[0] + nav_link.get('href')
									elif nav_link.get('href')[0] == '/':
										page_link = splitter[0] + '//' + splitter[2] + nav_link.get('href')
									elif nav_link.get('href')[:4] == 'http':
										page_link = nav_link.get('href')

										if nav_link.get('href').find(splitter[2].split('.')[1]) == -1:
											external_link = True
									else:
										page_link = splitter[0] + '//' + splitter[2] + '/' + nav_link.get('href')

									if not external_link:
										page_counter += 1
										# nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ii, content_id, content_ipc, content_ipl = get_content(page_link)
										nav_col1, nav_col2, nav_col3, nav_col4, nav_col_num, _, _, meta_title, meta_keywords, meta_desc, form, embed, iframe, calendar, staff, news, content_ipc = get_content(page_link)
										# issue_images += content_ii
										# issue_docs += content_id
										issue_pages_counter += content_ipc
										# issue_pages_links += content_ipl
										csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', nav_col_num, nav_col1, nav_col2, nav_col3, nav_col4, meta_title, meta_keywords, meta_desc])

										if form != '' or embed != '' or iframe != '' or calendar != '' or staff != '' or news != '':
											csv_report.writerow([str(page_link), form, embed, iframe, calendar, staff, news])
									else:
										csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), str(nav_link.get_text()), '', '1', 'Linked page', '', '', '', '', '', ''])
						else:
							csv_writer.writerow([str(page_link), str(group_links[0].get_text()), str(link.get_text()), '', '', '1', 'Linked page', '', '', '', '', '', ''])
				csv_report.writerow([])
				csv_report.writerow(['Pages scraped', page_counter])
				csv_report.writerow(['Issues', issue_pages_counter])
				# image_counter = len(glob.glob(f'../f_web_interface/static/files/{mainfolder}/{school_name}/images/*'))
				# csv_report.writerow(['Images downloaded', image_counter, issue_images])
				# doc_counter = len(glob.glob(f'../f_web_interface/static/files/{mainfolder}/{school_name}/docs/*'))
				# csv_report.writerow(['Docs downloaded', doc_counter, issue_docs])
				csv_report.writerow([])
				csv_report.writerow([])
				csv_report.writerow([])

			print('Finished:', site)

	print('Finished:', round((time() - start_time) / 3600, 2), 'h')
