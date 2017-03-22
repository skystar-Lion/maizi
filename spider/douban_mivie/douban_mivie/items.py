# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMivieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    director = scrapy.Field()
    scriptwriter = scrapy.Field()
    lead_actor = scrapy.Field()
    type = scrapy.Field()
    offcialSite = scrapy.Field()
    productAddress = scrapy.Field()
    language = scrapy.Field()
    initialReleaseDate = scrapy.Field()
    runtime = scrapy.Field()
    aliasName = scrapy.Field()
    IMDBAddress = scrapy.Field()
    brief_info = scrapy.Field()
