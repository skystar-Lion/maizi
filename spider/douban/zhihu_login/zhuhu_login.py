#-*- coding=utf-8 -*-

import urllib
from urllib import request
from urllib import error
from html.parser import HTMLParser
from http import cookiejar

class zhihu_client():
    def __init__(self):
        super(zhihu_client, self).__init__()
    
    def login(self, phone_num, password):
        url = 'https://www.zhihu.com/#signin'
        res = request.urlopen(url)
        if res.getcode() == 200:
            content = res.read().decode('utf-8')
        (xsrf, captcha_type) = get_sign_info(content)
        print("xsrf: %s, captcha_type: %s" % (xsrf, captcha_type))
        
        header = {
            'Host':'www.zhihu.com',
            'Origin':'https://www.zhihu.com',
            'Referer':'https://www.zhihu.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            }
        post_data = {
            '_xsrf':xsrf,
            'password':password,
            'captcha_type':captcha_type,
            'phone_num':phone_num
            }
        
        url = 'https://www.zhihu.com/login/phone_num'
        
        cj = cookiejar.CookieJar()
        pro = request.HTTPCookieProcessor(cj)
        opener = request.build_opener(pro)
        request.install_opener(opener)

        
        data = urllib.parse.urlencode(post_data).encode(encoding='utf_8')
        res = request.Request(url, data=data, headers = header)
        res = request.urlopen(res)
        if res.getcode() == 200:
            print("recode:%s,reinfo:%s" % (res.getcode(),res.info()))
            return res.read().decode('utf-8')
        
    def get_info(self):
        url = 'https://www.zhihu.com/people/skystar-69/activities'
        res = request.urlopen(url)
        if res.getcode() == 200:
            content = res.read().decode('utf-8')
        position = get_position(content)
        print("position:%s" % (position))

def _get_attr(attrs,name):
    for key,value in attrs:
        if key == name:
            return value
    return None
    
def get_position(content):
    class position_info(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.position = ''
            self.flag = False
        
        def handle_starttag(self, tag, attrs):
            if tag == 'span' and _get_attr(attrs, 'class') == 'RichText ProfileHeader-headline':
                self.flag = True
        def handle_data(self, data):
            if self.flag:
                self.position = data
                self.flag = False
    p = position_info()
    p.feed(content)
    return p.position
    

def get_sign_info(content):
    class sign_info(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self._xsrf = ''
            self.captcha_type =''
        

        
        def handle_starttag(self, tag, attrs):
            if tag == 'input' and _get_attr(attrs, 'type') == 'hidden' and _get_attr(attrs, 'name') == '_xsrf':
                self._xsrf = _get_attr(attrs, 'value')
            if tag == 'input' and _get_attr(attrs, 'type') == 'hidden' and _get_attr(attrs, 'name') == 'captcha_type':
                self.captcha_type = _get_attr(attrs, 'value')
    p = sign_info()
    p.feed(content)
    print(p._xsrf, p.captcha_type)
    return p._xsrf, p.captcha_type
            

if __name__ == "__main__":
    c = zhihu_client()
    c.login('18516995767', 'zhihu3@py')
    c.get_info()