#-*- coding=utf-8 -*-

import scrapy
from xici_site.items import XiciSiteItem

class xici_spider(scrapy.Spider):
	""" xici_spider(scrapy.Spider) class xici_spider must inherite from scrapy.Spider, otherwise scrapy can't find the spider"""
	
	global count
	name = 'xici_web'
	#allowed_domains = ['dmoz.org']
	#start_urls = ['http://www.dmoz.org/Computers/Programming/Languages/Python/Books/']

	start_urls = []
	allowed_domains = ['xicidaili.com']
	for i in range(1,10):
		url = "http://www.xicidaili.com/nn/%s" % i
		start_urls.append(url)
	#start_urls = ['http://www.xicidaili.com/nn']
	
	def parse(self, response):
		"""
		print(response.url)  # 打印响应体的url，详见:http://scrapy-chs.readthedocs.io/zh_CN/master/topics/request-response.html
		print(response.headers) #打印响应体的头部信息
		print(response.status) #打印响应体的状态码
		"""
		ip_list = response.xpath('//table[@id="ip_list"]')
		#这里的tbody是通过firefix解析出来的，通过chrome浏览器没有这个标签,奇怪
		#ip = sel.xpath('tbody/tr[2]/td[2]/text()').extract()
		#print(ip)
			
		"""			
			item['ip'] = sel.xpath('tr[2]/td[2]/text()').extract()
			item['ip_port'] = sel.xpath('tr[2]/td[3]/text()').extract()
			item['ip_address'] = sel.xpath('tr[2]/td[4]/a/text()').extract()
			item['ip_type'] = sel.xpath('tr[2]/td[6]/text()').extract()
			item['ip_speed'] = sel.xpath('tr[2]/td[7]/div').re('\d+\.\d+')
			item['ip_alive_time'] = sel.xpath('tr[2]/td[8]/div').re('\d+\.\d+')
			item['ip_ttm'] = sel.xpath('tr[2]/td[9]/text()').extract()
			item['ip_valid_time'] = sel.xpath('tr[2]/td[10]/text()').extract()
			yield item
		"""
		#print(ip_list.xpath('tr')[0:2])
		#这里定义了count全局变量，导致这个函数不是线程安全的，即是不可重入函数
		global count
		count = 0
		#这里打印所有包含ip信息的tr列表,tr[0]是表头
		for sel in ip_list.xpath('tr')[1:]:
			item = XiciSiteItem()
			item['ip'] = sel.xpath('td[2]/text()').extract()
			item['ip_port'] = sel.xpath('td[3]/text()').extract()
			item['ip_address'] = sel.xpath('td[4]/a/text()').extract()
			item['ip_type'] = sel.xpath('td[6]/text()').extract()
			item['ip_speed'] = sel.xpath('td[7]/div').re('\d+\.\d+')
			item['ip_alive_time'] = sel.xpath('td[8]/div').re('\d+\.\d+')
			item['ip_ttm'] = sel.xpath('td[9]/text()').extract()
			item['ip_valid_time'] = sel.xpath('td[10]/text()').extract()
			count += 1
			print('total:%s' % count)
			yield item

			
		
