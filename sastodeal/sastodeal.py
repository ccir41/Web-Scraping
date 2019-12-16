import requests
from bs4 import BeautifulSoup
import csv


class SastoDeal():
	def __init__(self, url):
		self.url = url

	def crawl(self):
		page = requests.get(self.url)
		soup = BeautifulSoup(page.text, 'html.parser')
		container = soup.find('div', {'class': 'rightpanel'})
		panel = container.findAll('section', {'class': 'categorytDetailDiv'})

		for p in panel:
			detail = p.find('div', {'class': 'prod-detail'})
			title = detail.find('b', {'class': 'title'}).text.strip()
			price = detail.find('span', {'class': 'offer-price'}).text.strip()

			data = {
				'title': title,
				'price': price
			}
			self.save_csv(data)

	def save_csv(self, data):
		with open('sastodeal.csv', 'a') as csv_file:
			fieldnames = ['title', 'price']
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writerow(data)

sd = SastoDeal(url="https://www.sastodeal.com/sastodeal/cta-laptop-33")
sd.crawl()