# -*- coding: utf-8 -*-
import scrapy
import json
import pymysql
from scrapy.http import Request
from items import AgencyItem


class AgencySpider(scrapy.Spider):
    name = "agency"
    allowed_domains = ["12306.cn"]
    start_urls = ['https://kyfw.12306.cn/otn/userCommon/allProvince']
    custom_settings = {
        'ITEM_PIPELINES' : {
            'work_12306.pipelines.AgencyPipeline' : 300,
        },
        'JOBDIR' : 'stack/agency',
    }

    def parse(self, response):
        #print(response.body.decode('utf-8'))
        
        datas = json.loads(response.body.decode('utf-8'))
        province_list = []
        url_format = 'https://kyfw.12306.cn/otn/queryAgencySellTicket/query?province={}&city=&county='
        if 'data' in datas:
            for province in datas['data']:
                province_list.append(province['chineseName'])
                #print(province['chineseName'])
                url = url_format.format(province['chineseName'])
                yield Request(url = url, callback = self.get_agency_info)


    def get_agency_info(self, response):

        datas = json.loads(response.body.decode('utf-8'))
        if 'data' in datas and 'datas' in datas['data']:            
            for info in datas['data']['datas']:
                item = AgencyItem()               
                item['province'] = info['province'].replace(' ','')
                item['city'] = info['city'].replace(' ','')
                item['county'] = info['county'].replace(' ','').replace('\t', '')
                #还有这种事：
                #agency_name":"\"深圳市万顺达航空售票服务有限公司","address":"深圳市龙岗区横岗新亚洲广场商业街一楼南大门",
                #"agency_name":"\"五一\"商场客票代售点","address":"淮南市田家庵区淮舜北路254号"
                item['agency_name'] = info['agency_name'].replace(' ','').replace('"', '')
                item['address'] = info['address'].replace(' ','').replace('"', '')
                item['start_time_am'] = info['start_time_am'].replace(' ','')
                item['stop_time_pm'] = info['stop_time_pm'].replace(' ','')
                item['windows_quantity'] = info['windows_quantity'].replace(' ','')
                #print(item)
                yield item
        
