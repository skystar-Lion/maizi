# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Maizi12306Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    agency_name = scrapy.Field()
    address = scrapy.Field()
    start_time = scrapy.Field()
    stop_time = scrapy.Field()
    windows_quantity = scrapy.Field()
