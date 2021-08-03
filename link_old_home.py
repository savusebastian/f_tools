import csv

from bs4 import BeautifulSoup
import requests


def check_by_class(web_page):
	# try:
		web_link = requests.get(web_page)
		web_soup = BeautifulSoup(web_link.content, 'html.parser')
		links = web_soup.find('main').find_all('a')
		o = []

		for link in links:
			if link.get('href') != None and len(link.get('href')) > 19 and (link.get('href')[:25] == 'https://www.skschools.org' or link.get('href')[:24] == 'http://www.skschools.org' or link.get('href')[:21] == 'https://skschools.org' or link.get('href')[:20] == 'http://skschools.org'):
				o.append(link.get_text())

		return o

	# except Exception:
	# 	pass
		# print('Page not working:', web_page)


if __name__ == '__main__':
	all_schools = [
		'https://skschoolsorg.finalsite.com/site-map',
		'https://skschoolsorg-23-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-42-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-49-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-47-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-48-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-50-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-51-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-52-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-53-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-54-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-56-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-55-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-57-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-58-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-59-us-west1-01.preview.finalsitecdn.com/site-map',
		'https://skschoolsorg-60-us-west1-01.preview.finalsitecdn.com/site-map',
	]

	for url in all_schools:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		urls = soup.find('main').find_all('a')
		counter = 0

		for link in urls:
			if link.get_text()[0] != 'h':
				d = check_by_class('https:' + link.get_text())
			else:
				d = check_by_class(link.get_text())

			if d != []:
				print('Link:', link.get_text())
				print('Text of links:', d)

		print()
		print()
		print()
		print('Next school')
