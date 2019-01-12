# -*- coding: utf-8 -*-
import scrapy
import json
from pixiv.items import PixivDataItem
from pixiv.items import InsidePageItem
from scrapy_splash import SplashRequest
import time


class PixivRankSpider(scrapy.Spider):
    name = 'pixiv_rank'
    allowed_domains = ['pixiv.net']
    start_urls = ["http://pixiv.net/"]

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
            bookmark = illust['rating_count']
            for tag in tag_list:
                inside = InsidePageItem()
                inside['illust_id'] = illust_id
                inside['tag'] = tag
                yield inside

            item = PixivDataItem()
            item['member_id'] = user_id
            item['illust_id'] = illust_id
            item['bookmark'] = bookmark
            item['created_at'] = int(time.time())
            illust_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust_id}'
            yield SplashRequest(
                url=illust_url.format(illust_id=illust_id),
                callback=self.parse_inside_page,
                meta={'item': item}
            )

    def parse_inside_page(self, response):
        item = response.meta['item']
        image_url = response.xpath('//div[@class="img-container"]//img').xpath('@src').extract()
        if len(image_url) > 0:
            item['image_urls'] = image_url

        yield item