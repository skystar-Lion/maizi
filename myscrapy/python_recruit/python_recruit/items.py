# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PythonRecruitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #goods_img ：商品图片
    #goods_price：商品价格
    #goods_name：商品名称
    #book_authors：图书作者
    #publishing_com：出版社
    #publishing_date：出版日期
    #goods_commits：商品评论数
    #shop_name：店铺名称
    #shop_url：店铺链接
    goods_img = scrapy.Field()              
    goods_price = scrapy.Field()
    goods_name = scrapy.Field()
    goods_info = scrapy.Field()
    goods_commits = scrapy.Field()
    book_authors = scrapy.Field()
    publishing_com = scrapy.Field()
    publishing_date = scrapy.Field()
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
