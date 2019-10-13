# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BytedancePipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = 'python_recruit', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        self.sql = """INSERT  byte_dance(job_name, job_category, job_summary, job_city, pub_time, job_qualification,  
        job_description, job_required) VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""


    def process_item(self, item, spider):
        if item['job_city'] != '北京' or item['job_summary'] != '研发':
            raise DropItem("recruitment conditions don\'t match.")
        else:
            try:

                data = (item['job_name'], item['job_category'], item['job_summary'], item['job_city'], item['pub_time'], 
                    item['job_qualification'], item['job_description'], item['job_required'])
                #print(self.sql % data)
                self.cursor.execute(self.sql % data)
                self.db.commit()
                print('db insert new record.')
            except Exception as e:
                self.db.rollback()
                print('db insert failed,already rollback', e)


    def close_spider(self, spider):
        self.db.close()

