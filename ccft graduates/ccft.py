import os
import time
import re
import csv

from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from selenium import webdriver


base_dir = os.path.abspath(os.path.dirname(__file__))
Base = declarative_base()

class CCFTDetail(Base):
    __tablename__ = 'ccft'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    university = Column(String)
    company = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    webpage = Column(String)
	
    def __repr__(self):
        return "<CCFTDetail(person_name={})>".format(self.name)

db_uri = 'sqlite:///' + os.path.join(base_dir, 'ccft.db')
engine = create_engine(db_uri)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class CCFT():
    def __init__(self):
        self.base_url = "https://shop.utvetce.com/ccft-graduates"
        self.driver = webdriver.Chrome('/usr/bin/chromedriver')
        self.states_url = []
        self.session = Session()

    def usa_states(self):
        self.driver.get(self.base_url)
        #time.sleep(10)
        result = self.driver.find_elements_by_xpath("//*[@id='rt-mainbody']//*[@class='side-navigation']//*[@id='narrow-by-list']//*[@class='odd collapsed']//ol/li")
        for r in result:
            state_link = r.find_element_by_tag_name('a').get_attribute('href')
            self.states_url.append(state_link)
        #print(self.states_url)
    
    def save_csv(self, data):
        with open('cctf.csv', 'a') as csv_file:
            fieldnames = ['name', 'university', 'company', 'address', 'phone', 'email', 'webpage']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(data)
    
    def get_or_create(self, session, model, **kwargs):
	    instance = session.query(model).filter_by(**kwargs).first()
	    if not instance:
		    instance = model(**kwargs)
		    session.add(instance)
		    session.commit()
	    return instance

    def information(self, content):
        lines = re.split(r'\n', content)
        name = None
        university = None
        company = None
        address = None
        phone = None
        email = None
        webpage = None
        print(lines)
        if lines != [" "]:
            name = lines[0]
            university = lines[1]
            for l in lines[2:]:
                company_match = re.match("^[A-Z][a-z0-9]+\s+\-\S", l)
                if company_match:
                    company = company_match.group()
                
                address_match = re.match("[A-Z][a-z]+,\s[A-Z]{2}?\s\d{5}", l)
                if address_match:
                    address = address_match.group()
                
                phone_match = re.match("^\d{3}-\d{3}-\d{4}", l)
                if phone_match:
                    phone = phone_match.group()

                # email_match = re.match("[a-z0-9]+@[a-z]+.\S+", l)
                # if email_match:
                #     print(email_match.group())

                if "Email: " in l:
                    email = l.split("Email: ")[1]
                
                if 'www' or 'WWW' in l:
                    webpage = l

            data = {
                'name': name,
                'university': university,
                'company': company if company != None else '',
                'address': address if address != None else '',
                'phone': phone if phone != None else '',
                'email': email if email != None else '',
                'webpage': webpage if webpage != None else ''
            }
            # print(data)
            # self.save_csv(data)
            self.get_or_create(self.session, CCFTDetail, **data)
    
    def extract_information(self):
        self.usa_states()
        for url in self.states_url:
            print(url)
            self.driver.get(url)
            # self.driver.get("https://shop.utvetce.com/ccft-oregon")
            # time.sleep(10)
            data = self.driver.find_elements_by_xpath("//*[@id='rt-mainbody']//*[@class='layout layout-2-cols']//*[@role='main']//*[@class='std']//*[@class='states-table']//tbody//tr/td//p")
            
            print(len(data))
            if len(data) > 0:
                for d in data:
                    print(d)
                    if d.text == "":
                        table_data = self.driver.find_elements_by_xpath("//*[@id='rt-mainbody']//*[@class='layout layout-2-cols']//*[@role='main']//*[@class='std']//*[@class='states-table']//tbody//tr/td")
                        # print(table_data)
                        if len(table_data) > 0:
                            for td in table_data:
                                # print(td)
                                content = td.text
                                # print(content)
                                if content != '':
                                    self.information(content)
                                else:
                                    print("empty text in table data also")
                        print("empty text in paragraph of table data")
                    else:
                        content = d.text
                        self.information(content)
            break


c = CCFT()
c.extract_information()