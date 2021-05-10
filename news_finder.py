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
	with open('all_sites.csv', 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		with open('news_finder.csv', 'w') as csv_main:
			csv_writer = csv.write(csv_main)
			csv_writer.writerow(csv_reader[0])

			for row in csv_reader[1:]:
				URL = row[0]
				print(URL)
				news_links = ''
				sitemap = requests.get(URL + 'fs/pages/sitemap.xml')
				soup = BeautifulSoup(sitemap.content, 'html.parser')
				urls = soup.find_all('loc')

				for link in urls:
					if link.get_text()[0] == '/':
						news = check_news('https:' + link.get_text())
					else:
						news = check_news(link.get_text())

					if news:
						news_links += link.get_text() + '\n'

				if news_links == '':
					news_links = 'None found'

				csv_writer.writerow([URL, news_links])