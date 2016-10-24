# -*- coding: utf-8 -*-
import scrapy


class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["yelp.com"]

    def start_requests(self):
        biz_path = getattr(self, 'biz_json', 'data/biz.json')
        biz = bz.data(biz_path)
        biz = bz.compute(biz)
        for b in biz:
            yield scrapy.Request(url=b['url'], callback=self.parse, meta=b)

    def parse(self, response):
        pass
