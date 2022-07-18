from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client['user1607']
news_yandex = db.news_yandex

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/103.0.0.0 Safari/537.36'}

url = 'https://yandex.ru/news/'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

news_list = []

link = dom.xpath("//section[@aria-labelledby='top-heading']//h2/a/@href")
title = dom.xpath("//section[@aria-labelledby='top-heading']//h2/a/text()")
title = [a.replace(u'\xa0', u' ') for a in title]
source = dom.xpath("//section[@aria-labelledby='top-heading']//span[@class='mg-card-source__source']//a/text()")
time_publication = dom.xpath("//section[@aria-labelledby='top-heading']//span[@class='mg-card-source__time']/text()")

for i in range(len(title)):
    news = {}
    news['title'] = title[i]
    news['link'] = link[i]
    news['source'] = source[i]
    news['time_publication'] = time_publication[i]

    news_list.append(news)

news_yandex.insert_many(news_list)

for item in news_yandex.find({}):
    pprint(item)

client.close()
