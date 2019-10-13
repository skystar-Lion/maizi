# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request

class DoubanMiviePipeline(object):
    def process_item(self, item, spider):
        """ test the pipeline functuon
        print("in pipelines:")
        print(item['img'])
        """
        if item['name']:
            filepath = 'movies/' + item['name']
            if not os.path.exists(filepath):
                os.makedirs(filepath)

        if filepath:
            self.create_readme(item, filepath)
            self.download_image(item['img'], filepath)
            return item
        else:
            raise DropItem("write file isn't exists...")


    def download_image(self, img_url, filepath):
        url = "".join(img_url)
        print(url)
        img_filename = filepath + '/' + url.split('/')[-1]
        with open(img_filename, 'wb') as f:
            f.write(request.urlopen(url).read())
        

    def create_readme(self, item, filepath):
        filename = filepath + '/' + 'Readme.txt'
        with open(filename, 'w', encoding = 'utf-8') as f:
            f.write("电影名称：%s\n" % item['name'])
            f.write("评分：%s\n" % item['score'])
            f.write("导演：%s\n" % item['director'])
            f.write("编剧: %s\n" % item['scriptwriter'])
            f.write("主演: %s\n" % item['lead_actor'])
            f.write("类型: %s\n" % item['type'])
            f.write("官方网站: %s" % item['offcialSite'])
            f.write("制片国家/地区: %s\n" % item['productAddress'])
            f.write("语言: %s\n" % item['language'])
            f.write("上映日期: %s\n" % item['initialReleaseDate'])
            f.write("片长: %s\n" % item['runtime'])
            f.write("别名: %s\n" % item['aliasName'])
            f.write("IMDb链接: %s\n" % item['IMDBAddress'])
            f.write("简介: %s\n" % item['brief_info'])