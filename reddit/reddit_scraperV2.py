import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://old.reddit.com/top/"
request = urllib.request.Request(url)
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html, 'html.parser')

main_table = soup.find("div", attrs={'id':'siteTable'})

comment_a_tags = main_table.find_all('a', attrs={'class':'bylink comments may-blank'})
#we have all the a tags with comment links

urls=[]
for a_tag in comment_a_tags:
    url = a_tag['href']
    if not url.startswith('http'):
        url = 'https://reddit.com' + url
    urls.append(url)

#print(urls)

#doenload the page content
request = urllib.request.Request('https://old.reddit.com/r/funny/comments/ae8p96/the_legendary_snow_gun/')
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html, 'html.parser')

#selecting the title
title = soup.find('a',attrs={'class':'title'}).text
#print(title)
# snv = soup.find_all('div',attrs={'class':'score unvoted'})
# print(snv)
upvotes = soup.find('div',attrs={'class':'score unvoted'}).text
#print(upvotes)

#selecting original poster
# l=len(soup.find_all('a',attrs={'class':'author'}))
# print(l)#210 not unique

#anothertry
main_post = soup.find('div',attrs={'id':'siteTable'})
#l=len(main_post.find_all('a',attrs={'class':'author'}))
#print(l)#only 1
title = main_post.find('a',attrs={'class':'title'}).text
upvotes = main_post.find('div',attrs={'class':'score unvoted'}).text
original_poster = main_post.find('a',attrs={'class':'author'}).text
comments_count = main_post.find('a',attrs={'class':'bylink comments may-blank'}).text
comment_area = soup.find('div',attrs={'class':'commentarea'})
comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})
c = len(comments)
print(c)#307 comments
print(comments_count)
print(title)
print(upvotes)
print(original_poster)


extracted_comments = []
for comment in comments:
    if comment.find('form'):
        commenter = comment.find('a',attrs={'class':'author'}).text
        comment_text = comment.find('div',attrs={'class':'md'}).text
        permalink = comment.find('a',attrs={'class':'bylink'})['href']
        extracted_comments.append({'commenter':commenter,'comment_text':comment_text,'permalink':permalink})

permalink = request.full_url
print(permalink)
print(extracted_comments)
