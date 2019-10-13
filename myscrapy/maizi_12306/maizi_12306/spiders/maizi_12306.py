# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from maizi_12306.items import Maizi12306Item


class A12306Spider(scrapy.Spider):
    name = "12306"
    allowed_domains = ["12306.cn"]
    start_urls = ['https://kyfw.12306.cn/otn/userCommon/allProvince']

    def parse(self, response):
        #print(response.body)
        datas = json.loads(response.body)
        if 'data' in datas:
            for province in datas['data']:
                #print(province['chineseName'])
                url = 'https://kyfw.12306.cn/otn/queryAgencySellTicket/query?province={}&city=&county='.format(province['chineseName'])
                #print(url)
                yield Request(url = url, callback = self.agency)


    def agency(self, response):
        #print(response.body)
        infos = json.loads(response.body)
        item = Maizi12306Item()
        #print(infos['data']['datas'])
        if 'data' in infos and 'datas' in infos['data']:
            for info in infos['data']['datas']:
                item = {}
                item['province'] = info['province'].strip()
                item['city'] = info['city'].strip()
                item['country'] = info['county'].strip()
                item['agency_name'] = info['agency_name'].strip()
                item['address'] = info['address'].strip()
                item['start_time'] = info['start_time_am'].strip()
                item['stop_time'] = info['stop_time_pm'].strip()
                item['windows_quantity'] = info['windows_quantity'].strip()
                
                yield item



