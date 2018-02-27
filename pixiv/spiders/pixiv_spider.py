# coding=utf-8

import scrapy
from scrapy.exceptions import *
from scrapy_splash import SplashRequest
from pixiv.items import PixivDataItem
import datetime
import time
import itertools

class PixivSpider(scrapy.Spider):
    name = "pixiv"
    allowed_domains = ['pixiv.net']
    start_urls = ["http://pixiv.net/"]

    def start_requests(self):
        return [scrapy.Request(url='https://accounts.pixiv.net/login', callback=self.after_login)]

    def after_login(self, response):
        post_key = response.css('#old-login input[name=post_key]::attr(value)').extract_first()

        setting = self.settings
        if not setting['PIXIV_USER_NAME'] or not setting['PIXIV_USER_PASS']:
            raise CloseSpider('username or password not set !')

        return scrapy.FormRequest(url='https://accounts.pixiv.net/login',
                                  formdata={
                                      'pixiv_id': setting['PIXIV_USER_NAME'],
                                      'password': setting['PIXIV_USER_PASS'],
                                      'post_key': post_key,
                                      'skip': '1',
                                      'mode': 'login'
                                  },
                                  callback=self.logged_in)

    def logged_in(self, response):
        if response.url == 'https://accounts.pixiv.net/login':
            raise CloseSpider('username or password error !')

        yield SplashRequest(self.generate_search_url(), self.parse)

    def generate_search_url(self, page=1):
        url = 'https://www.pixiv.net/search.php?s_mode=s_tag&p={page}&word=Fate%2FGrandOrder'
        return url.format(page=page)

    def parse(self, response):
        image_list = response \
            .xpath('//section[@id="js-react-search-mid"]//div[@class="_7IVJuWZ"]//a//div') \
            .xpath("@style") \
            .re('url\((.+)\)')

        illust_list = response \
            .xpath('//section[@id="js-react-search-mid"]//div[@class="_7IVJuWZ"]//figcaption//li/a') \
            .xpath('@href') \
            .re('illust_id=(\d+)')

        member_list = response \
            .xpath('//section[@id="js-react-search-mid"]//div[@class="_7IVJuWZ"]//figcaption//ul/li[2]/a') \
            .xpath('@href') \
            .re("id=(\d+)")

        for member_id, illust_id, url in itertools.izip(member_list, illust_list, image_list):
            item = PixivDataItem()
            item['member_id'] = member_id
            item['illust_id'] = illust_id
            item['image_urls'] = [url]
            item['bookmark'] = 0
            item['created_at'] = int(time.time())
            yield item

