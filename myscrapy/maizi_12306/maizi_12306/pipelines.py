# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class Maizi12306Pipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = '12306_site', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        self.sql = """ INSERT  scrapy_agency(province, city, country, agency_name, address, start_time, end_time, windows_quality) 
        VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s") """
    def process_item(self, item, spider):
        self.sql_data = (item['province'], item['city'], item['country'], item['agency_name'],
            item['address'], item['start_time'], item['stop_time'], item['windows_quantity'])
        try:
            print(self.sql % self.sql_data)
            self.cursor.execute(self.sql % self.sql_data)
            self.db.commit()
            #print("inert sql record success...")
        except Exception as e:
            self.db.rollback()
            print("sql rollback ...", e) 
        

    def close_spider(spider):
        self.db.close()
