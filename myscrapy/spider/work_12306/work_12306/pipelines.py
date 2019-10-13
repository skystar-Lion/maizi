# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from work_12306.items import TimeScheduleName, TrainInfoItem, StationCodeItem, TicketItem

class AgencyPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = '12306_site', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        self.sql = """INSERT station_agency(province, city, county, agency_name, agency_address, start_time_am, stop_time_pm, windows_quantity)
        VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""


    def process_item(self, item, spider):
        sql_data = (item['province'], item['city'], item['county'], item['agency_name'],
                    item['address'], item['start_time_am'], item['stop_time_pm'], item['windows_quantity'])

        try:
            self.cursor.execute(self.sql % (sql_data))
            self.db.commit()
            spider.logger.info("table station_agency insert record from {}".format(item['province']))
        except (Exception, pymysql.err.DataError, TypeError) as e:
            spider.logger.info(self.sql % (sql_data))
            spider.logger.error("insert record failed", e)
            self.db.rollback()

class BureauPipeline(object):
    """docstring for BureauPipeline ureauPipeline"""
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = '12306_site', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        self.sql = """INSERT station_info(train_bureau, station_type, station_name, station_address, passengers, luggage, package)
        VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")"""

    def process_item(self, item, spider):
        sql_data = (item['train_bureau'], item['station_type'], item['station_name'], item['station_address'], item['passengers'],
            item['luggage'], item['package'])
        try:
            self.cursor.execute(self.sql % (sql_data))
            self.db.commit()
            spider.logger.info("table station_info insert record from: %s" % (item['train_bureau']))
        except (Exception, pymysql.err.DataError, TypeError) as e:
            spider.logger.info(self.sql % (sql_data))
            spider.logger.error("insert record failed", e)
            self.db.rollback()

class SchedulePipeline(object):
    """docstring for SchedulePipeline"""
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = '12306_site', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        #写入指定日期的所有车次信息
        self.sql_a = """INSERT train_info(date, train_code, train_num, start_station, to_station) VALUES("%s", "%s", "%s", "%s", "%s")"""
        #写入指定日期的所有车次的途经站点信息
        self.sql_b = """INSERT station_time VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")"""


    def process_item(self, item, spider):
        if isinstance(item, TrainInfoItem):
            sql_data = (item['date'], item['train_code'], item['train_num'], item['start_station'], item['to_station'])
            try:
                self.cursor.execute(self.sql_a % sql_data)
                self.db.commit()
            except (Exception, pymysql.err.DataError, TypeError) as e:
                spider.logger.info(self.sql_a % (sql_data))
                spider.logger.error("insert record failed", e)
                self.db.rollback()
        elif isinstance(item, TimeScheduleName):
            sql_data = (item['date'], item['train_code'], item['station_no'], item['station_name'],
                item['start_time'], item['arrive_time'], item['stopover_time'])
            try:
                self.cursor.execute(self.sql_b % sql_data)
                self.db.commit()
            except (Exception, pymysql.err.DataError, TypeError) as e:
                spider.logger.info(self.sql_b % (sql_data))
                spider.logger.error("insert record failed", e)
                self.db.rollback()

class TicketPipeline(object):
    """docstring for TicketPipeline"""
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = '12306_site', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        #写入所有的车站对应的编号
        self.sql_code = """INSERT station_code(station_name, station_code) VALUES("%s", "%s")"""
        self.sql_ticket = """INSERT station_ticket VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""

    def process_item(self, item, spider):
        #print("in pipeline:")
        if isinstance(item, StationCodeItem):
            sql_data = (item['station_name'], item['station_code'])
            try:
                self.cursor.execute(self.sql_code % sql_data)
                #print("insert code table...")
                self.db.commit()
            except (Exception, pymysql.err.DataError, TypeError) as e:
                spider.logger.info(self.sql_code % (sql_data))
                spider.logger.error("insert record failed", e)
                self.db.rollback()
        elif isinstance(item, TicketItem):
            sql_data = (item['train_code'], item['start_station'], item['to_station'], item['swz_num'], item['tz_num'], 
                item['zy_num'], item['ze_num'], item['gr_num'], item['rw_num'], item['yw_num'], item['rz_num'], 
                item['yz_num'], item['wz_num'], item['qt_num'])
            try:
                self.cursor.execute(self.sql_ticket % sql_data)
                print("insert table station_ticket record...")
                self.db.commit()
            except (Exception, pymysql.err.DataError, TypeError) as e:
                spider.logger.info(self.sql_ticket % (sql_data))
                spider.logger.error("insert record failed", e)
                self.db.rollback()
            except pymysql.err.IntegrityError as e:
                spider.logger.info("Duplicate entry insert:",self.sql_ticket % (sql_data))
                spider.logger.error("insert record failed", e)
                self.db.rollback()

        


        
        
        

        
