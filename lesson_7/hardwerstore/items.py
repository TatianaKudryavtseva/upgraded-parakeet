# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join, Identity


def process_price(value):
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        pass
    return value


class HardwerstoreItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field(input_processor=Join(), output_processor=TakeFirst())
