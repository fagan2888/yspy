# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpReviewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BizInfoItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    michelin_stars = scrapy.Field()
    yelp_stars = scrapy.Field()
    style = scrapy.Field()
    neighborhood = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    phone_number = scrapy.Field()


class ReviewItem(scrapy.Item):
    user_id = scrapy.Field()
    biz_id = scrapy.Field()
    yelp_stars = scrapy.Field()
    date = scrapy.Field()
    review = scrapy.Field()
    useful_count = scrapy.Field()
    funny_count = scrapy.Field()
    cool_count = scrapy.Field()

