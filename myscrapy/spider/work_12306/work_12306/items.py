# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AgencyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    agency_name = scrapy.Field()
    address = scrapy.Field()
    start_time_am = scrapy.Field()
    stop_time_pm = scrapy.Field()
    windows_quantity = scrapy.Field()


class BureauItem(scrapy.Item):
    """docstring for BureauItem"""
    train_bureau = scrapy.Field()
    station_type = scrapy.Field()
    station_name = scrapy.Field()
    station_address = scrapy.Field()
    passengers = scrapy.Field()
    luggage = scrapy.Field()
    package = scrapy.Field()

class TimeScheduleName(scrapy.Item):
    """docstring for ClassName"""
    date = scrapy.Field()
    train_code = scrapy.Field()
    station_no = scrapy.Field()
    station_name = scrapy.Field()
    start_time = scrapy.Field()
    arrive_time = scrapy.Field()
    stopover_time = scrapy.Field()

class TrainInfoItem(scrapy.Item):
    """docstring for ClassName"""
    date = scrapy.Field()
    train_code = scrapy.Field()
    train_num = scrapy.Field()
    start_station = scrapy.Field()
    to_station = scrapy.Field()

class StationCodeItem(scrapy.Item):
    """docstring for station_code"""
    station_name = scrapy.Field()
    station_code = scrapy.Field()

class TicketItem(scrapy.Item):
    """docstring for TicketItem"""
    train_code = scrapy.Field()
    start_station = scrapy.Field()
    to_station = scrapy.Field()
    swz_num = scrapy.Field()
    tz_num = scrapy.Field()
    zy_num = scrapy.Field()
    ze_num = scrapy.Field()
    gr_num = scrapy.Field()
    rw_num = scrapy.Field()
    yw_num = scrapy.Field()
    rz_num = scrapy.Field()
    yz_num = scrapy.Field()
    wz_num = scrapy.Field()
    qt_num = scrapy.Field()


        

            

        
        
        
