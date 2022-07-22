from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from pprint import pprint


client = MongoClient('mongodb://localhost:27017')
db = client['user1807']
goods_mvideo = db.goods_mvideo

options = Options()
options.add_argument("start-maximized")

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)

driver.get('https://www.mvideo.ru/')
driver.implicitly_wait(10)

place = driver.find_element(By.TAG_NAME, 'mvid-shelf-group')
place = place.location_once_scrolled_into_view

button = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]")
button.click()

name = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[contains(@class,'name')]")
price = driver.find_elements(By.XPATH,
                             "//mvid-shelf-group//mvid-product-cards-group//div[contains(@class,'price')]"
                             "//span[@class='price__main-value']")

for i in range(len(name)):
    goods = {}
    goods['name'] = name[i].text
    goods['price'] = price[i].text

    goods_mvideo.insert_one(goods)

for item in goods_mvideo.find({}):
    pprint(item)

client.close()
