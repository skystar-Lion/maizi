# -*- coding: utf-8 -*-
import scrapy
import pymysql
import datetime
import json
from items import StationCodeItem, TicketItem
from scrapy.http import Request


class TicketSpider(scrapy.Spider):
    name = "ticket"
    allowed_domains = ["12306.cn"]
    start_urls = ['https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9001']
    custom_settings = {
        'ITEM_PIPELINES' : {
            'work_12306.pipelines.TicketPipeline' : 300,
        },
        'JOBDIR' : 'stack/ticket',
    }

    def parse(self, response):
        code = {}
        routes = {}
        
        for data in  response.body.decode('utf-8').split('@')[1:]:
            #print("%s %s " % (data.split('|')[1], data.split('|')[2]))
            item = StationCodeItem()
            item['station_name'] = data.split('|')[1]
            item['station_code'] = data.split('|')[2]
            code[item['station_name']] = item['station_code']
            #print(item)
            yield item
        
        routes = self.get_routes()
        base_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
        date = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days = 3), "%Y-%m-%d")
        for row in routes:
            #'九龙' 竟然没有编号？
            start_station_code = code[row[0]]
            to_station_code = code[row[1]]
            url = base_url.format(date, start_station_code, to_station_code)
            #print("in parse:", url)
            yield Request(url = url, callback = self.ticket_info)



    def get_routes(self):
        results = {}
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = '12306_site', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        self.sql = "select distinct start_station,to_station from train_info"
        try:
            self.cursor.execute(self.sql)
            results = self.cursor.fetchall()
        except Exception as e:
            print("error,get datas failed...",e)
        self.db.close()
        """
        for row in results:
            print("%s, %s" % (row[0],row[1]))
        """
        return results


    def ticket_info(self, response):
        datas = json.loads(response.body.decode('utf-8'))
        if 'data' in datas:
            for infos in datas['data']:
                #print(infos)
                if 'queryLeftNewDTO' in infos:
                    info = infos['queryLeftNewDTO']
                    #print(info)
                    
                    item = TicketItem()
                    item['train_code'] = info['station_train_code']
                    item['start_station'] = info['start_station_name']
                    item['to_station'] = info['end_station_name']
                    item['swz_num'] = info['swz_num']
                    item['tz_num'] = info['tz_num']
                    item['zy_num'] = info['zy_num']
                    item['ze_num'] = info['ze_num']
                    item['gr_num'] = info['gr_num']
                    item['rw_num'] = info['rw_num']
                    item['yw_num'] = info['yw_num']
                    item['rz_num'] = info['rz_num']
                    item['yz_num'] = info['yz_num']
                    item['wz_num'] = info['wz_num']
                    item['qt_num'] = info['qt_num']
                    #print(item)
                    yield item
                    


            
