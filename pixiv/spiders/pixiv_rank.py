# -*- coding: utf-8 -*-
import scrapy
import json
from pixiv.items import PixivDataItem
from pixiv.items import InsidePageItem
import time


class PixivRankSpider(scrapy.Spider):
    name = 'pixiv_rank'
    allowed_domains = ['pixiv']
    start_urls = ['http://pixiv/']

    def start_requests(self):
        setting = self.settings
        rank_url = 'https://www.pixiv.net/ranking.php?format=json'
        page = 1

        for p in range(1, page + 1):
            yield scrapy.Request(url=rank_url, callback=self.parse)

    def parse(self, response):
        decode = json.loads(response.body)
        illust_list = decode['contents']
        for illust in illust_list:
            tag_list = illust['tags']
            illust_id = illust['illust_id']
            user_id = illust['user_id']
            image_url = illust['url']
            bookmark = illust['rating_count']
            for tag in tag_list:
                inside = InsidePageItem()
                inside['illust_id'] = illust_id
                inside['tag'] = tag
                yield inside

            item = PixivDataItem()
            item['member_id'] = user_id
            item['illust_id'] = illust_id
            item['image_urls'] = [image_url]
            item['bookmark'] = bookmark
            item['created_at'] = int(time.time())

            yield item