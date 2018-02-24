# pixiv-crawler

抓取 pixiv 圖片和資料做處理
抓出我想要的圖片後下載，之後會對圖片做處理，讓程式可以學習我想要抓哪些圖片。
另外順便做圖片識別，找出風格相似的圖片。

1. 照時間排序後抓取圖片
2. 取出人氣 作者 然後儲存起來
3. 圖片和資料要怎麼存放
4. 根據圖片內容找出下載者的愛好
5. 透過訓練好的模型找出沒有人氣但是下載者喜歡的圖片
6. 搜尋 by 圖片

## Getting Started


### Prerequisites

splash

	docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash

mongodb 

see [install-mongodb-on-ubuntu]

[install-mongodb-on-ubuntu]:https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/


### Installing

	git clone git@github.com:fubuki/pixiv-crawler.git
	cd pixiv-crawler
	pip install -r requirements.txt
	scrapy crawl pixiv


