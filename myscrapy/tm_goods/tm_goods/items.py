# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmGoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    good_name = scrapy.Field()
    good_price = scrapy.Field()
    good_assess_num = scrapy.Field()
    shop_name = scrapy.Field()
    shop_tel = scrapy.Field()
    shop_site = scrapy.Field()
    #download image
    image_urls = scrapy.Field()
    images = scrapy.Field()
