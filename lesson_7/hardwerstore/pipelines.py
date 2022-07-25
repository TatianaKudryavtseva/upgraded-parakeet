# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import scrapy
from scrapy.utils.python import to_bytes
from pymongo import MongoClient, errors
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class HardwerstorePipeline:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        self.mongo_base = client.store2507

    def process_item(self, item, spider):
        item['_id'] = item['_id']
        item['name'] = item['name']
        item['price'] = item['price']
        item['url'] = item['url']
        item['photos'] = self.process_photos_list_url(item['photos'])

        collection = self.mongo_base[spider.name]

        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            collection.replace_one({'_id': item['_id']}, item)
        return item

    @staticmethod
    def process_photos_list_url(photos):
        lst_photo = []
        for photo in photos:
            lst_photo.append(photo['path'])
        return lst_photo

    @staticmethod
    def process_spec(spec_key, spec_value):
        spec = dict(zip(spec_key, spec_value))
        return spec


class HardwerstorePhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["name"]}/{image_guid}.jpg'
