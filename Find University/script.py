import sys
import time
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.headless = True


class FindUniversity:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver_linux64/chromedriver", options=chrome_options)
        self.url = "https://www.finduniversity.ph/search.aspx?sch=1&region=national-capital-region"
        self.csv_headers = []
        self.append_header = False
    
    def extract_data(self):
        self.driver.get(self.url)
        time.sleep(10)
        try:
            dissmiss_button = self.driver.find_element_by_id('dismiss-button')
        except:
            dissmiss_button = None
        if dissmiss_button:
            dissmiss_button.submit()
        time.sleep(10)
        detaildiv = self.driver.find_elements_by_xpath("//div[@class='shell']//div[@class='section__group-main']//div[@class='search-result']//div[@class='box-inner-top']")
        for dv in detaildiv:
            try:
                name = dv.find_element_by_tag_name('h3').text
            except:
                name = None
            try:
                location = dv.find_element_by_xpath("//ul[@class='details']//li[@class='location']").text
            except:
                location = None
            try:
                application_url = dv.find_element_by_xpath("//ul[@class='details']//li[@class='application']").get_attribute('href')
            except:
                application_url = None
            tuitions = dv.find_elements_by_xpath("//ul[@class='details']//li[@class='tuition']")
            try:
                bachelor_tuition = tuitions[0].text.strip()
            except:
                bachelor_tuition = None
            try:
                masters_tuition = tuitions[1].text.strip()
            except:
                masters_tuition = None
            try:
                doctorate_tuition = tuitions[2].text.strip()
            except:
                doctorate_tuition = None
            review = dv.find_element_by_xpath("//div[@class='search-item__review']//p").text.strip()
            reviewer = dv.find_element_by_xpath("//div[@class='search-item__review']//p[@class='reviewer']").text.strip()
            data = {
                "name": name,
                "location": location,
                "bachelor_tuition": bachelor_tuition,
                "masters_tuition": masters_tuition,
                "doctorate_tuition": doctorate_tuition,
                "application_url": application_url,
                "review": review,
                "reviewer": reviewer
            }
            self.write_csv(data)
        try:
            next = self.driver.find_element_by_id('cphBody_cphMain_ucBusinessList_ucPagerBottom_hlNext')
        except:
            next = None
        if next:
            self.url = next.get_attribute('href')
            self.extract_data()
        sys.exit()
    
    def write_csv(self, data):
        if not self.csv_headers:
            for key, value in data.items():
                self.csv_headers.append(key)
        with open('university.csv', 'a+', encoding='utf8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.csv_headers)
            if not self.append_header:
                writer.writeheader()
                self.append_header = True
            writer.writerow(data)

if __name__ == "__main__":
    fu = FindUniversity()
    fu.extract_data()