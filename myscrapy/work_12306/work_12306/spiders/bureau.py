# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from items import BureauItem

class BureauSpider(scrapy.Spider):
    name = "bureau"
    allowed_domains = ["12306.cn"]
    start_urls = ['http://www.12306.cn/mormhweb/kyyyz/']
    custom_settings = {
        'ITEM_PIPELINES' : {
            'work_12306.pipelines.BureauPipeline' : 300,
        },
        'JOBDIR' : 'stack/bureau',
    }

    def parse(self, response):
        base_url = 'http://www.12306.cn/mormhweb/kyyyz/'
        rail_bureau = response.xpath('//*[@id="secTable"]/tbody/tr/td/text()')
        rail_station = response.xpath('//a[@title="客运站数据(车站)"]/@href')
        rail_stopping_point = response.xpath('//a[@title="客运站数据(乘降所)"]/@href')
        #print(rail_bureau, rail_station, rail_stopping_point)
        for i in range(len(rail_bureau)):
            bureau_name = rail_bureau[i].extract()
            rail_station[i] = base_url + rail_station[i].extract().replace('./', '')
            rail_stopping_point[i] = base_url + rail_stopping_point[i].extract().replace('./', '')
            #print(bureau_name, rail_station[i], rail_stopping_point[i])
            
            for times in range(2):
                yield Request(url = rail_station[i], callback = self.station_info, meta = {'type': '0', 'train_bureau': bureau_name})
                yield Request(url = rail_stopping_point[i], callback = self.station_info, meta = {'type': '1', 'train_bureau': bureau_name})
            


    def station_info(self, response):
        res = response.xpath('//tbody/tr')
        for s in res[2:]:
            item = BureauItem()
            item['train_bureau'] = response.meta['train_bureau']
            item['station_type'] = response.meta['type']
            item['station_name'] = ''.join(s.xpath('td[1]/text()').extract()).strip().replace(' ','').replace('\t' ,'')
            item['station_address'] = ''.join(s.xpath('td[2]/text()').extract()).strip().replace(' ','').replace('\t' ,'')
            if ''.join(s.xpath('td[3]/text()').extract()).strip():
                item['passengers'] = ''.join(s.xpath('td[3]/text()').extract()).strip().replace(' ','').replace('\t' ,'')
            else:
                item['passengers'] = 'x'
            if ''.join(s.xpath('td[4]/text()').extract()).strip():
                item['luggage'] = ''.join(s.xpath('td[4]/text()').extract()).strip().replace(' ','').replace('\t' ,'')
            else:
                item['luggage'] = 'x'
                #桐城站（既有）    安徽省桐城市龙眠街道海峰东路1号    √   　   快运包裹,呵呵
            if ''.join(s.xpath('td[5]/text()').extract()).strip():
                item['package'] = ''.join(s.xpath('td[5]/text()').extract()).strip().replace(' ','').replace('\t' ,'')
            else:
                item['package'] = 'x'
            """ 
            item['station_address'] = s[1].text
            if s[2].text.strip():
                item['passengers'] = s[2].text.strip()
            else:
                item['passengers'] = 'x'
            if s[3].text.strip():
                item['luggage'] = s[3].text.strip()
            else:
                item['luggage'] = 'x'
            if s[4].text.strip():
                item['package'] = s[4].text.strip()
            else:
                item['package'] = 'x'
            """
            #print(item)
            yield item


