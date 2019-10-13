# -*- coding=utf-8 -*-
'''
Created on 2017��3��1��

@author: Lion
'''
import urllib
from urllib import request
from urllib import error
from html.parser import HTMLParser
from pip._vendor.distlib.compat import raw_input
from http import cookiejar




class douban_client(object):
    def __init__(self):
        super(douban_client, self).__init__()
        
        
    def login(self, user_email, password):
        #先通过抓取原始页面的html获取需要登录的post表单数据
        url = 'https://accounts.douban.com/login'
        res = request.urlopen(url)
        if res.getcode() == 200:
            content = res.read().decode('utf-8')
        #print(get_captcha(content))
        (string_code, captcha_id) = get_captcha(content)
            
        headers = {        
        'Host':'accounts.douban.com',
        'Origin':'https://accounts.douban.com',
        'Referer':'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
          
        post_data = {
        'source':'index_nav',
        'redir':'https://www.douban.com/',
        'form_email':user_email,
        'form_password':password,
        'captcha-solution':string_code,
        'captcha-id':captcha_id,
        'login':'登录'
        }
        """
        这段代码至关重要啊，负责登录coockie信息的传递，没有他，后续的页面相当于是没有登录的情况下操作的，fuck
        cj = cookiejar.CookieJar()
        pro = request.HTTPCookieProcessor(cj)
        opener = request.build_opener(pro)
        request.install_opener(opener)
        """
        cj = cookiejar.CookieJar()
        pro = request.HTTPCookieProcessor(cj)
        opener = request.build_opener(pro)
        request.install_opener(opener)
        
        datas = urllib.parse.urlencode(post_data)
        datas = datas.encode(encoding='utf_8')
        url = "https://accounts.douban.com/login"
        try:
            res = request.Request(url , data = datas, headers = headers)
            res = request.urlopen(res)  
        except error.HTTPError as e:
            print('the server can\'t fulfill the request')
            print('Error code', e.code, 'Error reason:', e.reason)
        except error.URLError as e:
            print('can\'t reach the server')
            print('Error reason', e.reason)
        else:
            print("recode:",res.getcode())
            #print("reinfo:",res.info())
            return res.read()
        
        
    def edit_signature(self, sig):
        url = "https://www.douban.com/people/158479867/"
        res = request.urlopen(url)
        if res.getcode() == 200:
            #print(res.getcode())
            content = res.read().decode('utf-8')
            f = open("douban.txt", 'w')
            f.write(content)
            f.close()
            print("write done")
            #print(content)
        

        ck = get_ck(content)
        
        
        headers = {
        'Host':'www.douban.com',
        'Origin':'https://www.douban.com',
        'Referer':'https://www.douban.com/people/158479867/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
            }
        post_data = {
            'ck':ck,
            'signature':sig
            }
        print("in edit:%s" % post_data) 

        
        datas = urllib.parse.urlencode(post_data)
        datas = datas.encode(encoding='utf_8')
        url = "https://www.douban.com/j/people/158479867/edit_signature"
        try:
            res = request.Request(url , data = datas, headers = headers)
            res = request.urlopen(res)
        except error.HTTPError as e:
            print('the server can\'t fulfill the request')
            print('Error code', e.code, 'Error reason:', e.reason)
        except error.URLError as e:
            print('can\'t reach the server')
            print('Error reason', e.reason)
        else:
            print("recode:",res.getcode())
            #print("reinfo:",res.info())
            return res.read()


def get_attr_value(attr, name):
    for key,value in attr:
        if key == name:
            return value
    return None


def get_captcha(content):
#获取登录的图片码    
    class get_captcha(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.captcha_code = ""
            self.captcha_id =""
            
        def handle_starttag(self, tag, attrs):
            if tag == "img" and get_attr_value(attrs, 'id') == 'captcha_image' and get_attr_value(attrs, 'class') == 'captcha_image':
                print("验证码图片地址:%s" % (get_attr_value(attrs, 'src')))
                self.captcha_code = raw_input("")
                
            if tag == "input" and get_attr_value(attrs, 'type') == 'hidden' and get_attr_value(attrs, 'name') == 'captcha-id':
                self.captcha_id = get_attr_value(attrs, 'value')

    p = get_captcha()
    p.feed(content)
    return p.captcha_code,p.captcha_id


def get_ck(content):
    class get_ck(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck =""
            self.sig = ""
            
        def handle_starttag(self, tag, attrs):
            if tag == "input" and get_attr_value(attrs, 'type') == 'hidden' and get_attr_value(attrs, 'name') == 'ck':
                self.ck = get_attr_value(attrs, 'value')
                print("ck:%s" % self.ck)
            if tag == "input" and get_attr_value(attrs, 'name') == 'signature' and get_attr_value(attrs, 'type') == 'text' and get_attr_value(attrs, 'maxlength') == '30':
                self.sig = get_attr_value(attrs, 'value')
                print("sig:%s" % self.sig)

    p = get_ck()
    p.feed(content)
    return p.ck



    

if __name__ == '__main__':

    c = douban_client()
    c.login("xxx", "xxx")
    sig = "huangzi"
    c.edit_signature(sig)
    
