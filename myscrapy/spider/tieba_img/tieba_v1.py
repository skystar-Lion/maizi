# -*- coding=utf-8 -*-
'''
Created on 2017年3月3日

@author: Lion
'''

from urllib import request
from html.parser import HTMLParser
import os

def get_attrs(attrs, name):
    for key, value in attrs:
        if key == name:
            return value
    return None


def http_curl(url):
    res = request.urlopen(url)
    if res.getcode() == 200:
        return res.read()
    else:
        return None


class tieba():
    def __init__(self):
        super().__init__()
        
    def get_author_info(self,content):
        class myhtml_parser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.infos = []
                self.info = {}
                self.tag = False
                
            def handle_starttag(self, tag, attrs):
                if (tag == 'a' and get_attrs(attrs, 'class') == 'frs-author-name j_user_card ' and 
                    get_attrs(attrs, 'target')):
                    self.info['url'] = 'http://tieba.baidu.com' + get_attrs(attrs, 'href')
                    self.tag = True
            def handle_data(self, data):
                if self.tag:
                    self.info['name'] = data
                    
                    if self.info not in self.infos:
                        self.infos.append(self.info)
                        #print(self.info)
                        self.info = {}
                        
            
            def handle_endtag(self, tag):
                if tag == 'a':
                    self.tag = False
        p_info = myhtml_parser()
        p_info.feed(content)
        print(p_info.infos)
        return p_info.infos
                
    def download_img(self, info_list):
        
        
        class myhtml_parser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.atag = False
                self.url = None
                
            def handle_starttag(self, tag, attrs):
                if tag == 'a' and get_attrs(attrs, 'class') == 'userinfo_head':
                    self.atag = True
                if tag == 'img' and self.atag:
                    self.url = get_attrs(attrs, 'src')
            def handle_endtag(self, tag):
                if tag == 'a':
                    self.atag = False
                    
        p = myhtml_parser()
        print('totally %s image.' % len(info_list))
        count = 0
        for img in info_list:
            if not os.path.exists('image'):
                os.mkdir('image')
            filename = 'image/' + img['name'] + '.jpg'
            
            count += 1
            try:
                page_content = http_curl(img['url']).decode('utf-8')
            except UnicodeDecodeError as e:
                print("count: %d, name: %s,jpg_url: %s, decode error: %s" % (count, img['name'], img['url'], e))

            
            p.feed(page_content)
            print("count: %d, filename: %s , url: %s" % (count, filename, p.url))
            url = p.url
            str = http_curl(url)
            f = open(filename, 'wb')
            f.write(str)
            f.close()
                  

if __name__ == "__main__":
    url = 'http://tieba.baidu.com/f?kw=python&fr=ala0&tpl=5'
    content = http_curl(url).decode('utf-8')
    c = tieba()
    user_list = c.get_author_info(content)
    c.download_img(user_list)