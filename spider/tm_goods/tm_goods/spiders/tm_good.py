# -*- coding: utf-8 -*-
import scrapy
from tm_goods.items import TmGoodsItem
from scrapy.http import Request



class TmGoodSpider(scrapy.Spider):
    name = "tm_good"
    allowed_domains = ["suning.com"]
    start_urls = [
        #'https://list.tmall.com/search_product.htm?type=pc&totalPage=100&cat=50025135&sort=d&style=g&from=sn_1_cat-qp&active=1&jumpto=10#J_Filter',
        'http://list.suning.com/0-346873-0.html'
    ]

    def parse(self, response):
        
        all_goods_list = response.xpath('//ul[@class="clearfix"]')
        for good_list in all_goods_list.xpath('li'):
            #print(good_list)
            items = TmGoodsItem()
            items['good_price'] = good_list.xpath('div/div/div/div[2]/p[1]/em/text()').extract()
            items['good_name'] = good_list.xpath('div/div/div/div[2]/p[2]/a/text()').extract()
            #print(items['good_name'])
            items['good_assess_num'] = good_list.xpath('div/div/div/div[2]/p[3]/a[1]/text()').extract()
            items['image_urls'] = ["http:" + good_list.xpath('div/div/div/div[1]/div[1]/a/img/@src2').extract()[0]]
            #print(items['image_urls'])
            #获取店铺的页面连接
            link_url = good_list.xpath('div/div/div/div[2]/p[2]/a/@href').extract()
            #print(items)
            url = "".join(link_url)
            #print("url:%s" % url)
            yield Request(url = url, meta = {'item' : items}, callback = self.parse_detail)
            

    def parse_detail(self, response):
        items = response.meta['item']
        total_infos = response.xpath('//div[@class="si-intro"]')
        items['shop_name'] = total_infos.xpath('div[@class="si-intro-list"]/dl[1]/dd/strong/a/text()').extract()
        items['shop_tel'] = total_infos.xpath('div[@class="si-intro-list"]/dl[3]/dd/p/text()').extract()
        items['shop_site'] = total_infos.xpath('div[@class="si-intro-handle2"]/a[1]/@href').extract()
        #print(items)
        yield items




