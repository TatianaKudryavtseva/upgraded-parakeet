from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient, errors
from dateutil.parser import parse


client = MongoClient('mongodb://localhost:27017')
db = client['user1607']
news_mail = db.news_mail

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        ' AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/103.0.0.0 Safari/537.36'}

url = 'https://news.mail.ru/'

session = requests.Session()
response = session.get(url, headers=header)

dom = html.fromstring(response.text)

link = dom.xpath("//div[contains(@class,'daynews')]//@href")
for el in link:
    news = {}
    response = requests.get(el)
    dom = html.fromstring(response.text)
    title = dom.xpath("//h1/text()")
    source = dom.xpath("//span[@class ='breadcrumbs__item']//a/span/text()")
    data = dom.xpath("//span[@class ='breadcrumbs__item']//span[contains(@class,'js-ago')]/@datetime")
    data_publication = parse(data[0]).date()
    time_publication = parse(data[0]).time()
    id_news = dom.xpath("//div[contains(@class,'article')]/@data-news-id")

    news['_id'] = id_news[0]
    news['title'] = title[0]
    news['link'] = el
    news['source'] = source[0]
    news['data_publication'] = str(data_publication) + ' ' + str(time_publication)

    try:
        news_mail.insert_one(news)
    except errors.DuplicateKeyError:
        news_mail.replace_one({'_id': news['_id']}, news)

for item in news_mail.find({}):
    pprint(item)

client.close()
