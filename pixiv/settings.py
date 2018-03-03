# -*- coding: utf-8 -*-

BOT_NAME = 'pixiv'

SPIDER_MODULES = ['pixiv.spiders']
NEWSPIDER_MODULE = 'pixiv.spiders'

PIXIV_USER_NAME = 'username'
PIXIV_USER_PASS = 'password'

COOKIES_ENABLED = True

SPLASH_URL = 'http://127.0.0.1:8050'

CRAWL_PAGE = 1

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

ITEM_PIPELINES = {
    'pixiv.pipelines.PixivImagesPipeline': 1,
    'pixiv.pipelines.MongoPipeline': 2
}
IMAGES_STORE = '/path/file/'

MONGO_URI = '127.0.0.1'
MONGO_DATABASE = 'pixiv'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1