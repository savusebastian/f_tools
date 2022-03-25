import csv

from bs4 import BeautifulSoup
import requests


def check_news(web_page):
	try:
		web_link = requests.get(web_page).content
		web_soup = BeautifulSoup(web_link, 'html.parser')
		news = web_soup.find(class_='fsNews')
		# news = web_soup.find(id='fsPageContent').find(class_='fsNews')

		return news != None

	except Exception:
		pass


if __name__ == '__main__':
	# with open('all_sites.csv') as csv_file, open('news_finder.csv', 'w', encoding='utf-8') as csv_main:
	# 	csv_reader = csv.reader(csv_file)
	# 	csv_writer = csv.writer(csv_main)
	# 	csv_writer.writerow(next(csv_reader))
	#
	# 	for row in csv_reader:
	# 		col_0 = row[0]
			col_0 = 'https://www.garlandisdschools.net/'
			# print(col_0)
			news_links = ''
			sitemap = requests.get(f'{col_0}fs/pages/sitemap.xml').content
			soup = BeautifulSoup(sitemap, 'html.parser')
			links = soup.find_all('loc')

			for link in links:
				text = link.get_text()

				if text[0] == '/':
					news = check_news(f'https:{text}')
				else:
					news = check_news(text)

				if news:
					news_links += f'{text}\n'

			if news_links == '':
				news_links = 'No news found'

			# csv_writer.writerow([col_0, news_links])
			print(news_links)
