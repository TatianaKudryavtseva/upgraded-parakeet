from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from datetime import date


client = MongoClient('mongodb://localhost:27017')
db = client['user1607']
news_lenta = db.news_lenta

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/103.0.0.0 Safari/537.36'}

url = 'https://lenta.ru/'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//a[contains(@class, '_topnews')]")
for item in items:
    news = {}
    link = item.xpath("./@href")
    title = item.xpath(".//span/text() | .//h3/text()")
    source = url
    data_publication = item.xpath(".//time/text()")

    news['title'] = title[0]
    news['link'] = link[0]
    news['source'] = source
    news['data_publication'] = str(date.today()) + ' ' + str(data_publication[0])

    news_lenta.insert_one(news)

for item in news_lenta.find({}):
    pprint(item)

client.close()
