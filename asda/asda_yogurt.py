from selenium import webdriver
import time
import pandas as pd

class Scrapper():
	def __init__(self, pageNo):
		self.url = 'https://groceries.asda.com/search/yogurt?pageNo={}'.format(pageNo)
		self.driver = webdriver.Chrome('/usr/bin/chromedriver')

	def crawl(self):
		self.driver.get(self.url)
		# execute script to scroll down the page
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		# give time to load site
		time.sleep(30)
		# find elements by xpath
		results = self.driver.find_elements_by_xpath("//*[@class=' co-product-list__main-cntr']//*[@class=' co-item ']//*[@class='co-product']//*[@class='co-item__title-container']//*[@class='co-product__title']")
		# print(len(results))
		data = []
		for result in results:
			product_name = result.text
			link = result.find_element_by_tag_name('a')
			product_link = link.get_attribute('href')
			data.append({"product": product_name, "link": product_link})

		self.driver.quit()
		df = pd.DataFrame(data, columns=['product','link'])
		# print(df)
		# write to csv
		df.to_csv('data.csv', mode='a', header=False)

for i in range(12):
	i = i+1
	s = Scrapper(pageNo=i)
	s.crawl()

"""
# to speed up scraping use headless
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(firefox_options=options, executable_path = 'your/directory/of/choice')
"""