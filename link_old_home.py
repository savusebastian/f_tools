import csv

from bs4 import BeautifulSoup
import requests


def check_news(web_page):
	try:
		web_link = requests.get(web_page)
		web_soup = BeautifulSoup(web_link.content, 'html.parser')
		news = web_soup.find(class_='fsNews')

		return news != None

	except:
		pass


if __name__ == '__main__':
	def check_by_class(web_page):
		try:
			web_link = requests.get(web_page)
			print(web_page)
			web_soup = BeautifulSoup(web_link.content, 'html.parser')
			links = web_soup.find('main').find_all('a')
			o = []

			for link in links:
				if link.get('href') != None and len(link.get('href')) > 19 and (link.get('href')[:25] == 'https://www.skschools.org' or link.get('href')[:24] == 'http://www.skschools.org' or link.get('href')[:21] == 'https://skschools.org' or link.get('href')[:20] == 'http://skschools.org'):
					o.append(link.get_text())

			return o

		except:
			pass
			# print('Page not working:', web_page)


	url = 'https://skschoolsorg.finalsite.com/fs/pages/sitemap.xml'
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	urls = soup.find_all('loc')
	links = []
	counter = 0

	for link in urls:
		if link.get_text()[0] != 'h':
			d = check_by_class('https:' + link.get_text())
		else:
			d = check_by_class(link.get_text())

		if d != []:
			print('>', link)
			print(d)
