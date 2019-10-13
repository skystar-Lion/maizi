# -*- coding=utf-8 -*-

from scrapy.dupefilters import RFPDupeFilter

class myfilter(RFPDupeFilter):
    """request_fingerprint 默认会对url进行校验对比，这里只是通过url来判断重复"""
    def request_fingerprint(self, request):
        return request.url

