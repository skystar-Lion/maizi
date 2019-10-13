# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
from bytedance.items import BytedanceItem
import json


class TtSpider(scrapy.Spider):
    name = "tt"
    allowed_domains = ["toutiao.com"]
    
    def start_requests(self):
        #summary 是研发
        #F1:一开始第一次抓取，方向错误
        #url_format = 'https://job.toutiao.com/society#position={page}'
        url_format = 'https://job.toutiao.com/recruitment/position/list/?type=1&summary_id=873&sequence=&city=%E5%8C%97%E4%BA%AC&name=&limit=10&offset={page}&position_type='
        for i in range(0, 180, 10):
            url = url_format.format(page = i)
            #print(url)
            yield Request(url, callback = self.parse)


    def parse(self, response):
        #print(response.url)
        """F1:
        #print(response.body.decode('utf-8'))
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        con = driver.page_source
        #print(con)
        #with open('tt.html', 'w', encoding = 'utf-8') as f:
        #    f.write(con)
        content = Selector(text = con).xpath('//tbody/tr')
        for p in content:
            item = BytedanceItem()
            item['job_name'] = p.xpath('td[1]/a/text()').extract()[0]
            item['job_url'] = 'https://job.toutiao.com' + p.xpath('td[1]/a/@href').extract()[0]
            item['job_type'] = p.xpath('td[2]/text()').extract()[0]
            item['job_city'] = p.xpath('td[3]/text()').extract()[0]
            item['pub_time'] = p.xpath('td[4]/text()').extract()[0]
            yield Request(url = item['job_url'], callback = self.job_detail, meta = {'meta':item})
        """
        content = json.loads(response.body.decode('utf-8'))
        #print(content)
        if 'positions' in content:
            #print(response.url, len(content['positions']))
            for datas in content['positions']:
                item = BytedanceItem()
                item['job_category'] = datas['category']
                item['job_name'] = datas['name']
                item['job_summary'] =datas['summary']
                item['job_city'] = datas['city']
                item['pub_time'] = datas['create_time']
                item['job_qualification'] = datas['qualification']
                item['job_description'] = datas['description'].replace('"', '')
                item['job_required'] = datas['requirement'].replace('"', '')
                
                yield item


    def job_detail(self, response):
        item = response.meta['meta']
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        con = driver.page_source
        content = Selector(text = con).xpath('//div[@class="job-content"]')
        item['job_description'] = content.xpath('div[1]/pre/text()').extract()[0]
        item['job_required'] = content.xpath('div[2]/pre/text()').extract()[0]
        yield item


