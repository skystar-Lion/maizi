# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BytedanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()
    job_category = scrapy.Field()
    job_summary = scrapy.Field()
    job_city = scrapy.Field()
    pub_time = scrapy.Field()
    job_qualification = scrapy.Field()
    job_description = scrapy.Field()
    job_required = scrapy.Field()
