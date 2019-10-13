# -*- coding=utf-8 -*-

from scrapy.dupefilters import RFPDupeFilter

class myfilter(RFPDupeFilter):
    """request_fingerprint 默认会对url进行校验对比，这里只是通过url来判断重复"""
    def request_fingerprint(self, request):
        return request.url

"""
    def request_seen(self, request):
        #重写request_seen 方法，只要返回时True就会被过滤掉
        if "ZAF" in request.url:
            print(request.url)
            return True

"""



