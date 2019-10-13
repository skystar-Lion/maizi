# -*- coding=utf-8 -*-

import scrapy
import time
from spiders.agency import AgencySpider
from spiders.bureau import BureauSpider
from spiders.ticket import TicketSpider
from spiders.time_schedule import TimeScheduleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

settings = get_project_settings()
process = CrawlerProcess(settings)


#@defer.inlineCallbacks 通过链接(chaining) deferred来线性运行spider,如果不添加会运行不通过
@defer.inlineCallbacks
def myrun():
    #print("myrun 16")
    
    first_tag = True
    #print("myrun day:",day)
    while True:
        day = int(time.time() / 86400)
    
        if first_tag or day % 10 == 0:
            print("begin run agency...")
            yield process.crawl(AgencySpider) 
            print("begin run bureau...")
            yield process.crawl(BureauSpider)
        
        if day % 3 == 0 or first_tag:
            print("begin run ticket...")
            yield process.crawl(TimeScheduleSpider)
            print("begin run time_schedule...")
            yield process.crawl(TicketSpider)
        first_tag = False
        time.sleep(86400)

        

if __name__ == '__main__':
    myrun()
    process.start()


