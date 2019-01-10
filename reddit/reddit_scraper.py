#importing libraries we need
import urllib.request
from bs4 import BeautifulSoup
import json

#send request and download the html content of the url
url = "https://old.reddit.com/top/"

headers = {'user-agent':'Mozilla(Linux x86_64)'}
request = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(request).read()

#pass the html to BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

#get the html of the table called site Table where all the links are displayed
main_table = soup.find("div", attrs={'id':'siteTable'})

#now we go into main_table and get every element which has a class of "title"
links = main_table.find_all("a", class_="title")

#for each link extract the text of the link and link itself

extracted_records = []

for link in links:
    title = link.textT
    url = link['href']
    if not url.startswith('http'):
        url = "https://reddit.com"+url
    print("%s - %s"%(title, url))
    record = {
        'title': title,
        'url' : url
    }
    extracted_records.append(record)
#print(extracted_records)

#saving to json file
with open('data.json', 'w') as outfile:
    json.dump(extracted_records, outfile, indent=4)
