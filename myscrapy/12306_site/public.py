# -*- coding=utf-8 -*-

from urllib import request
from time import sleep
import ssl

def https_get(url):
    sleep(3)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    context = ssl._create_unverified_context()
    res = request.Request(url, headers = headers)
    res = request.urlopen(res, context = context)
    if res.getcode() == 200:
        return res.read().decode('utf-8')
    else:
        print('url request error:%s', res.getcode())
        exit(1)

def http_get(url):
    sleep(3)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}   
    res = request.Request(url, headers = headers)
    res = request.urlopen(res)
    if res.getcode() == 200:
        response = res.read().decode('utf-8')
        return response
    else:
        print('url request error:%s',res.getcode())
        exit(1)

def chinese_str(text, width, align = "left"):
    con = str(text)
    cn_count = 0
    cjk_list = ['\u3002','\uFF1F','\uFF01','\uFF0C','\u3001','\uFF1B','\uFF1A','\u300C','\u300D',
    '\u300E','\u300F','\u2018','\u2019','\u201C','\u201D','\uFF08','\uFF09','\u3014','\u3015','\u3010',
    '\u3011','\u2014','\u2026','\u2013','\uFF0E','\u300A','\u300B','\u3008','\u3009']
    #参见blog: http://blog.csdn.net/yuan892173701/article/details/8731490
    for uchar in con:
        if (uchar >= u'\u4E00' and uchar <= u'\u9FA5') or uchar in cjk_list:
            #如果是等款中文字符[4e00-9fa5],中文标点符号cjk_list，字符宽度是2个英文字符宽度
            cn_count += 2 
        else:
            cn_count += 1
    if align == 'left':
        return text + " " * (width - cn_count)
    elif align == 'right':
        return " " * (width - cn_count) + text
    else:
        return text

"""
print("str: {}|".format(chinese_str("中国", 20, 'right')))
print("str: {}|".format(chinese_str("abcdegf", 20, 'right')))
print("str: {}|".format(chinese_str("中《华》、（）", 20, 'right')))
"""



