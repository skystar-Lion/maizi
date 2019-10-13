# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiciSiteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    ip_port = scrapy.Field()
    ip_address = scrapy.Field()
    ip_type = scrapy.Field()
    ip_speed = scrapy.Field()
    ip_alive_time = scrapy.Field()
    ip_ttm = scrapy.Field()
    ip_valid_time = scrapy.Field()


