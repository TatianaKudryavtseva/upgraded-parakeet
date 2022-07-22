# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient, errors


class BooksPipeline:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        self.mongo_base = client.books2207

    def process_item(self, item, spider):
        item['_id'] = self.process_id(item['_id'])
        item['name'] = self.process_name(item['name'], item['authors'])
        item['authors'] = self.process_author(item['authors'])
        item['price_discount'] = self.process_price(item['price'])[1]
        item['price'] = self.process_price(item['price'])[0]

        collection = self.mongo_base[spider.name]

        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            collection.replace_one({'_id': item['_id']}, item)

        return item

    @staticmethod
    def process_id(book_id):
        book_id = book_id.split(': ')[1]
        return book_id

    @staticmethod
    def process_name(name, authors):
        if len(authors) != 0:
            name = name.split(': ')[1]
        else:
            name = name
        return name

    @staticmethod
    def process_author(authors):
        return ', '.join(authors)

    @staticmethod
    def process_price(price):
        if len(price) > 1:
            price_discount = int(price[1])
            price = int(price[0])
        elif len(price) == 1:
            price = int(price[0])
            price_discount = ''
        else:
            price = 'Нет в продаже'
            price_discount = ''
        return [price, price_discount]
