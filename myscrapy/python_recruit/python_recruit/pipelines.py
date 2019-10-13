# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from urllib import request

class PythonRecruitPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost', user = 'root', passwd = 'mims2', db = 'python_recruit', port = 3306, charset = 'utf8')
        self.cursor = self.db.cursor()
        self.sql = """INSERT jd_book VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")"""


    def process_item(self, item, spider):
        self.sql_data = (item['goods_img'], item['goods_price'], item['goods_name'], item['goods_info'],
        item['goods_commits'], item['book_authors'], item['publishing_com'], item['publishing_date'], item['shop_name'], item['shop_url'])
        #将图书的介绍图片抓取下来，并且以图书的名称作为文件名保存
        filename = 'pictures/' + item['goods_name'] + '.jpg' 
        try:
            f = open(filename, 'wb')
            f.write(request.urlopen(item['goods_img']).read())
            print('write done!', filename)
        except Exception as e:
            print("write error...",e)
        finally:
            f.close()

        #print(self.sql % self.sql_data)
        try:
            
            self.cursor.execute(self.sql % self.sql_data)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("sql rollback", e)
        

    def close_spider(self, spider):
        self.db.close()

