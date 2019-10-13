# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import Request
import json
import re
from items import TimeScheduleName,TrainInfoItem



class TimeScheduleSpider(scrapy.Spider):
    name = "time_schedule"
    allowed_domains = ["12306.cn"]
    custom_settings = {
        'ITEM_PIPELINES' : {
            'work_12306.pipelines.SchedulePipeline' : 300,
        },
        'JOBDIR' : 'stack/time_schedule',
    }


    def start_requests(self):
        base_url = 'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?date={}'
        t = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days = 3), "%Y-%m-%d")
        url = base_url.format(t)
        yield Request(url = url, callback = self.parse, meta = {'date': t})


    def parse(self, response):
        datas = json.loads(response.body.decode('utf-8'))
        if 'data' in datas:
            for train in datas['data']:
                item = TrainInfoItem()
                item['date'] = response.meta['date']
                item['train_code'] = train['station_train_code'].split('(')[0]
                item['train_num'] = train['train_no']
                item['start_station'] = re.split('\(|-|\)', train['station_train_code'])[1]
                item['to_station'] = re.split('\(|-|\)', train['station_train_code'])[2]
                #print(item)
                yield item
                url_format = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={}&from_station_telecode=XXX&to_station_telecode=XXX&depart_date={}'
                url = url_format.format(item['train_num'], item['date'])
                yield Request(url = url, callback = self.query_data, meta = {'date': item['date']})

    def query_data(self, response):
        datas = json.loads(response.body.decode('utf-8'))
        #print(datas)
        if 'data' in datas and 'data' in datas['data']:
            #print("in query_data...")
            for info in datas['data']['data']:
                item = TimeScheduleName()
                item['date'] = response.meta['date']
                if 'station_train_code' in info:
                    train_num = info['station_train_code']
                item['train_code'] = train_num
                item['station_no'] = info['station_no']
                item['station_name'] = info['station_name']
                item['start_time'] = info['start_time']
                item['arrive_time'] = info['arrive_time']
                item['stopover_time'] = info['stopover_time']
                #print(item)
                yield item


