# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from python_recruit.items import PythonRecruitItem
from selenium import webdriver
from scrapy.selector import Selector
import time

class JdBookSpider(scrapy.Spider):
    name = "jd_book"
    allowed_domains = ["jd.com"]
    custom_settings = {
        'ITEM_PIPELINES' : {
            'python_recruit.pipelines.PythonRecruitPipeline' : 300,
        }
    }

    def start_requests(self):
        url_format = 'https://search.jd.com/Search?keyword={}&enc=utf-8&page={}'
        keyword = 'python 数据挖掘'
        for page in range(1, 3):
            num = int(2 * page - 1)
            url = url_format.format(keyword, num)
            yield Request(url = url, callback = self.parse)

    def parse(self, response):
        #print(response.body.decode('utf-8'))
        #with open('jd-1.html', 'w', encoding = 'utf-8') as f:
        #    f.write(response.body.decode('utf-8'))
        
        #方法一：直接加载网页源代码，缺陷，有部分js的动态加载信息会丢失
        #contents = response.xpath('//div[@id="J_goodsList"]/ul/li')

        #方法二：通过selenium加载js代码生成完整的商品信息
        
        #print(response.url)
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        #document.body.scrollHeight获取当前内容的滚动高度
        js1 = 'return document.body.scrollHeight'
        #滚动到指定的位置
        js2 = 'window.scrollTo(0, document.body.scrollHeight)'
        old_scroll_height = 0
        #如果当前内容的滚动位置>上次内容的滚动位置，则继续滚动
        while(driver.execute_script(js1) > old_scroll_height):
            #print("current_height:{}---old_height:{}".format(driver.execute_script(js1), old_scroll_height))
            old_scroll_height = driver.execute_script(js1)
            driver.execute_script(js2)
            time.sleep(1)
        res = driver.page_source
        contents = Selector(text = res).xpath('//div[@id="J_goodsList"]/ul/li')
        
        #print("length:", len(contents))
        
        for index, info in enumerate(contents, 1):
            
            item = PythonRecruitItem()
            #这尼玛这种情况都能出现，什么鬼？应该是selenium加载结束遗留的问题
            #data-lazy-img="done" src="//img11.360buyimg.com/n1/s200x200_jfs/t3103/294/341326706/157850/6b62b40e/57b26a04Nc33c4a20.png">
            #goods_img = info.xpath('div/div[@class="p-img"]/a/img/@src | div/div[@class="p-img"]/a/img/@data-lazy-img')
            if info.xpath('div/div[@class="p-img"]/a/img/@src'):
                goods_img = info.xpath('div/div[@class="p-img"]/a/img/@src')
            else:
                goods_img = info.xpath('div/div[@class="p-img"]/a/img/@data-lazy-img')
            goods_price = info.xpath('div/div[@class="p-price"]/strong/i/text()')
            goods_name = info.xpath('div/div[@class="p-name"]/a/em')
            goods_info = info.xpath('div/div[@class="p-name"]/a/@href')
            goods_commits = info.xpath('div/div[@class="p-commit"]/strong/a/text()')
            if goods_img:
                item['goods_img'] = 'http:' + goods_img.extract()[0]
            if goods_price:
                item['goods_price'] = goods_price.extract()[0]
            if goods_name:
                item['goods_name'] = goods_name.xpath('string(.)').extract()[0].strip('区域').strip('包邮').replace(' ','').replace(':', '_').replace('：', '')
            if goods_info:           
                item['goods_info'] = 'http:' + goods_info.extract()[0]
            if goods_commits:
                item['goods_commits'] =  goods_commits.extract()[0]
            #这里需要分情况（京东自营/其他书店经营），京东店铺有介绍，其他需要在店铺详情查看
            bookdetails = info.xpath('div/div[@class="p-bookdetails"]')
            if bookdetails:
                book_authors = bookdetails.xpath('span[1]/a/text()')
                publishing_com = bookdetails.xpath('span[2]/a/text()')
                publishing_date = bookdetails.xpath('span[3]/text()')
                shop_name = info.xpath('div/div[@class="p-shopnum"]/span/text()')
                if book_authors:                 
                    item['book_authors'] =  bookdetails.xpath('span[1]/a/text()').extract()
                if publishing_com:
                    item['publishing_com'] = bookdetails.xpath('span[2]/a/text()').extract()[0]
                if publishing_date:
                    item['publishing_date'] = bookdetails.xpath('span[3]/text()').extract()[0]
                if shop_name:
                    item['shop_name'] = info.xpath('div/div[@class="p-shopnum"]/span/text()').extract()[0]
                item['shop_url'] = ''
            else:
                item = Request(url = item['goods_info'], callback = self.book_info, meta = {'item': item})
            #print(item)
            yield item
        

    def book_info(self, response):
        contents = response.xpath('//ul[@id="parameter2"]')
        item = response.meta['item']
        if contents:
            shop_name = contents.xpath('li[1]/a/text()')
            shop_url = contents.xpath('li[1]/a/@href')
            publishing_company =  contents.xpath('li[2]/a/text()')
            if shop_name: 
                item['shop_name'] = contents.xpath('li[1]/a/text()').extract()[0]
            if shop_url:
                item['shop_url'] = 'http:' + contents.xpath('li[1]/a/@href').extract()[0]
            #非京东自营的图书找不到作者信息
            item['book_authors'] = ''
            #出版社信息一般在商品介绍里面，一般顺序为“店铺：.*出版社：.*...
            
            if publishing_company:
                item['publishing_com'] = publishing_company.extract()[0]
            else:
                item['publishing_com'] = ''
            #出版时间有的是在出版信息里面，有的在页面的其他相信信息里面，所以这里是通过全文body信息正则匹配的
            publishing_date = contents.xpath('.').re(r'出版时间：.*([0-9]{4}.[0-9]{0,2}.[0-9]{0,2}).*')
            if publishing_date:
                item['publishing_date'] = publishing_date[0]
            else:
                item['publishing_date'] = ''

            return item
        
