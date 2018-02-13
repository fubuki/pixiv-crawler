# coding=utf-8

import scrapy
from scrapy.exceptions import *
from scrapy_splash import SplashRequest


class PixivSpider(scrapy.Spider):
    name = "pixiv"
    allowed_domains = ['pixiv.net']

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

        for url in image_list:
            print url
