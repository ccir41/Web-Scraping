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
        self.csv_headers = ["name", "location", "application_url", "Bachelor's", "Master's", "Doctorate", "Certificate", "review", "reviewer"]
    
    def extract_data(self):
        self.driver.get(self.url)
        time.sleep(5)
        try:
            dissmiss_button = self.driver.find_element_by_id('dismiss-button')
        except:
            dissmiss_button = None
        if dissmiss_button:
            dissmiss_button.submit()
        time.sleep(5)
        detaildiv = self.driver.find_elements_by_xpath("//div[@class='shell']//div[@class='section__group-main']//div[@class='search-result']//div[@class='box-inner-top']")
        for dv in detaildiv:
            data = {}
            name = dv.find_element_by_tag_name('h3').text.strip()
            data["name"] = name
            details = dv.find_elements_by_tag_name('li')
            for detail in details:
                class_attr = detail.get_attribute('class').strip()
                if class_attr == "location":
                    data["location"] = detail.text.strip()
                elif class_attr == "application":
                    data["application_url"] = detail.find_element_by_tag_name('a').get_attribute('href')
                elif class_attr == "tuition":
                    degreespan = detail.find_elements_by_tag_name('span')
                    try:
                        degree = degreespan[0].text.strip()
                        data[f"{degree}"] = degreespan[1].text.strip()
                    except:
                        pass
            #rev = dv.find_elements_by_class_name("search-item__review")
            #reviews = dv.find_elements_by_tag_name('p')
            #data["review"] = reviews[0].text.strip()
            #data["reviewer"] = reviews[1].text.strip()
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
        with open('university.csv', 'a+', encoding='utf8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.csv_headers)
            writer.writerow(data)

if __name__ == "__main__":
    fu = FindUniversity()
    fu.extract_data()