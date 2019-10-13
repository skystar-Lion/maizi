#-*- coding=utf-8 -*-

import scrapy
from first_test.items import FirstTestItem

class first_test(scrapy.spiders.Spider):
	"""dong for first_test"""
	def __init__(self):
		super(first_test, self).__init__()

	name = 'xxx'
	allowed_domains = ['dmoz.org']
	start_urls = ['http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
				  'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
	]

	def parse(self, response):
		"""
		filename = response.url.split('/')[-2]
		with open(filename, 'w') as f:
			f.write(response.body.decode('utf-8'))
		"""
		for sel in response.xpath('//ul/li'):
			"""
			title = sel.xpath('a/text()').extract()
			link = sel.xpath('a/@href').extract()
			desc = sel.xpath('text()').extract()
			print(title, link, desc)
			"""
			item = FirstTestItem()
			item['title'] = sel.xpath('a/text()').extract()
			item['link'] = sel.xpath('a/@href').extract()
			item['desc'] = sel.xpath('text()').extract()
			yield item
			
		
