# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["12306.cn"]
    start_urls = ['https://kyfw.12306.cn/otn/leftTicket/init']

    def parse(self, response):

        yield Request(url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-03-17&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=XAY&purpose_codes=ADULT', callback = self.myparse)
        yield Request(url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-03-17&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=ZAF&purpose_codes=ADULT', callback = self.myparse)
        yield Request(url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-03-17&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=XAY&purpose_codes=ADULT', callback = self.myparse)
        yield Request(url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-03-17&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=ZAF&purpose_codes=ADULT', callback = self.myparse)



    def myparse(self, response):
        print("in myparse:--------------------------------------------------------------", response.url)
        #yield Request(url = response.url, callback = self.myparse)
