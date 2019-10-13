# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from douban_mivie.items import DoubanMivieItem
from scrapy.http import Request
from scrapy.selector import Selector

class DoubanMovieSpider(scrapy.Spider):
    name = "douban_movie"
    allowed_domains = ["douban.com"]
    start_urls = ['https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0']

    def parse(self, response):

        #这里通过selenium模拟浏览器加载网页js代码
        driver = webdriver.Firefox()
        for url in self.start_urls:
            driver.get(url)
            #获取到加载js后的源代码
            res = driver.page_source
            #分别获取影片的名称，评分，海报图片和电影详细页面链接
            info_lists = Selector(text=res).xpath('//div[@class="list-wp"]/div[@class="list"]')
            for info_list in info_lists.xpath('a'): 
            #这里生成item所需要的字段，之后保存在item中
                items = DoubanMivieItem()       
                items['img'] = info_list.xpath('div/img/@src').extract()
                items['name'] = "".join(info_list.xpath('p/text()').extract()).strip().replace('\n', '')
                items['score'] = info_list.xpath('p/strong/text()').extract()
                info_url = "".join(info_list.xpath('@href').extract())
                #print(items)
                #开始从电影详细页面链接获取导演，类型等详细信息
                yield Request(url = info_url, meta =  {'items' : items}, callback = self.get_detail)

    def get_detail(self, response):
        items = response.meta['items']
        movie_info = response.xpath('//div[@id="info"]')
        #print(movie_info.xpath('span[3]/span[2]/a/text()').extract())
        items['director'] = movie_info.xpath('span[1]/span[2]/a/text()').extract()
        items['scriptwriter'] = "/".join(movie_info.xpath('span[2]/span[2]/a/text()').extract())
        items['lead_actor'] = movie_info.xpath('span[3]/span[2]/a/text()').extract()
        items['type'] = movie_info.xpath('span[@property="v:genre"]/text()').extract()
        items['offcialSite'] = movie_info.xpath('a[1]/@href').extract()
        items['initialReleaseDate'] = movie_info.xpath('span[@property="v:initialReleaseDate"]/text()').extract()
        items['runtime'] = movie_info.xpath('span[@property="v:runtime"]/text()').extract()
        #aliasName,language,productAddress都是text标签，没有被html标签包裹，比较恶心。先从了列表中将空元素和'/'元素删除，只“按照顺序”保留制片地区/语言/别名
        text_list = movie_info.xpath('text()').extract()
        for i in range(len(text_list)):
            text_list[i] = text_list[i].strip().replace('\n', '')
        while "" in text_list:
            text_list.remove("")
        while "/" in text_list:
            text_list.remove("/")
        #print(text_list)
        
        #这里也有特殊情况，比如：
        #“无处为家”只有['美国', '英语']两个字段；
        #“血战钢锯岭”多了一个字段['美国 / 澳大利亚', '英语', '/ 140分钟(美国)', '钢锯岭 / 钢铁英雄(台) / The Conscientious Objector']
        items['productAddress'] = text_list[0]
        items['language'] = text_list[1]
        if len(text_list) > 2:
            items['aliasName'] = text_list[-1]
        else:
            items['aliasName'] = ''
        
        items['IMDBAddress'] = movie_info.xpath('a[last()]/@href').extract()
        items['brief_info'] = "".join(response.xpath('//span[@property="v:summary"]/text()').extract()).strip().replace('\n', '')
        #print(items)
        yield items



