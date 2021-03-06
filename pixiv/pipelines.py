# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import imagehash
import pymongo
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from PIL import Image

class PixivImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        refer_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={id}'
        if 'image_urls' in item:
            for image_url in item['image_urls']:
                yield scrapy.Request(
                    image_url, meta={'m_id': item['member_id'], 'i_id': item['illust_id']},
                    headers={
                        'Referer': refer_url.format(id=item['illust_id']),
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
                    })

    def file_path(self, request, response=None, info=None):
        m_id = request.meta['m_id']
        i_id = request.meta['i_id']
        return 'full/%s/%s.jpg' % (m_id, i_id)

    def item_completed(self, results, item, info):
        if 'tag' in item:
            return item

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class MongoPipeline(object):

    collection_name = 'illust'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        table = self.collection_name

        if 'image_urls' in item:
            del item['image_urls']
            full_image_path = spider.settings['IMAGES_STORE'] + '/' + item['image_paths'][0]
            item['image_hash'] = str(imagehash.phash(Image.open(full_image_path)))
        else:
            table = 'illust_tags'

        self.db[table].update({'illust_id': item['illust_id']}, dict(item), upsert=True)
        return item