# coding=utf-8

import scrapy
from scrapy.exceptions import *
from scrapy_splash import SplashRequest
from pixiv.items import PixivDataItem
from pixiv.items import InsidePageItem
import time
import itertools

class PixivSpider(scrapy.Spider):
    name = "pixiv"
    allowed_domains = ['pixiv.net']
    start_urls = ["http://pixiv.net/"]

    def start_requests(self):
        setting = self.settings
        page = setting['CRAWL_PAGE']
        tags = setting['TAGS']
        for tag in tags:
            for p in range(1, page + 1):
                yield SplashRequest(self.generate_search_url(page=p, tag=tag), self.parse)
        #return [scrapy.Request(url='https://accounts.pixiv.net/login', callback=self.after_login)]

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

    def generate_search_url(self, page=1, tag=None):
        url = 'https://www.pixiv.net/search.php?s_mode=s_tag&p={page}&word={tag}&order=date_d'
        return url.format(page=page, tag=tag)

    def parse(self, response):

        illust_list = response \
            .xpath('//section[@id="js-react-search-mid"]//div//figcaption//li/a') \
            .xpath('@href') \
            .re('illust_id=(\d+)')

        member_list = response \
            .xpath('//section[@id="js-react-search-mid"]//div//figcaption//ul/li[2]/a') \
            .xpath('@href') \
            .re("id=(\d+)")

        print illust_list
        for member_id, illust_id in itertools.izip(member_list, illust_list):
            illust_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id={illust_id}'
            yield SplashRequest(
                url=illust_url.format(illust_id=illust_id),
                callback=self.parse_inside_page,
                meta={'illust_id': illust_id, 'member_id': member_id}
            )

    def parse_inside_page(self, response):
        tag_list = response.xpath('//span[@class="tags-container"]//li[@class="tag"]//a[2]/text()').extract()
        image_url = response.xpath('//div[@class="img-container"]//img').xpath('@src').extract()
        bookmark = response.xpath('//section[@class="score"]//li[2]//span[2]/text()').extract_first()

        print tag_list
        print image_url
        print bookmark
        for tag in tag_list:
            inside = InsidePageItem()
            inside['illust_id'] = response.meta['illust_id']
            inside['tag'] = tag
            yield inside

        item = PixivDataItem()
        item['member_id'] = response.meta['member_id']
        item['illust_id'] = response.meta['illust_id']
        item['image_urls'] = image_url
        item['bookmark'] = bookmark
        item['created_at'] = int(time.time())
        yield item