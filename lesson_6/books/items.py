# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    authors = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
    rate = scrapy.Field()
    price_discount = scrapy.Field()
