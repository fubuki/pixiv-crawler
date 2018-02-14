# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PixivDataItem(scrapy.Item):
    member_id = scrapy.Field()
    illust_id = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    bookmark = scrapy.Field()
    created_at = scrapy.Field()
