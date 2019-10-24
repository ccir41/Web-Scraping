from sqlalchemy import create_engine, Integer, String, Column, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import os
import re
from requests_html import HTMLSession

html_session = HTMLSession()

base_dir = os.path.abspath(os.path.dirname(__file__))
Base = declarative_base()


class UniversityDetail(Base):
	__tablename__ = 'university'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	email = Column(String)
	phone = Column(String)
	website = Column(String)
	address = Column(String)

	def __repr__(self):
		return "<UniversityDetail(university_name={})>".format(self.name)


db_uri = 'sqlite:///' + os.path.join(base_dir, 'university.db')

engine = create_engine(db_uri)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



class UniversityCrawler():
	def __init__(self, pageno):
		self.base_url = "https://edusanjal.com/"
		self.url = "https://edusanjal.com/university/?page={}".format(pageno)
	
	def crawl(self):
		r = html_session.get(self.url)
		r.html.render()

		phone_pattern = re.compile(".[0-9].+")
		email_pattern = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
		website_pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
		address_pattern = re.compile("[A-Z]+[a-z]+...+")

		root_div = r.html.find('#app', first=True)
		# print(root_div)

		require_div = root_div.find('.caption')
		
		for element_div in require_div:
			university_name = element_div.find('h3', first=True).text
			# print(university_name.text)
			caption_div = element_div.find('a')
			address_div = element_div.find('p')
			
			phone = []
			email = ''
			website = []
			address = []

			for e in caption_div:
				email_result = email_pattern.findall(e.text)
				if email_result != []:
					email = email_result[0]

				phone_result = phone_pattern.findall(e.text)
				if phone_result != []:
					phone.append(phone_result[0])

				phone_string = ''
				for p in phone:
					phone_string += str(p) + ', '

				website_result = website_pattern.findall(e.text)
				if website_result != []:
					website.append(website_result[0])

				website_string = ''
				for w in website:
					website_string += str(w) + ', '

			for a in address_div:
				address_result = address_pattern.search(a.text)
				if address_result:
					address.append(address_result)

			address_string = ''
			for a in address:
				address_string += str(a) + ', '


			data = {
				'name': university_name,
				'email': email,
				'phone': phone_string,
				'website': website_string,
				'address': address_string
			}
			# print(data)

			self.get_or_create(session, UniversityDetail, **data)

	def get_or_create(self, session, model, **kwargs):
		instance = session.query(model).filter_by(**kwargs).first()
		if not instance:
			instance = model(**kwargs)
			session.add(instance)
			session.commit()
		return instance


for i in range(4):
	pageno = i+1
	uc = UniversityCrawler(pageno)
	uc.crawl()
