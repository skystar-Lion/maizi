# -*- coding=utf-8 -*-
'''
Created on 2017��3��2��

@author: Lion
'''

import re
import json
from urllib import request
from html.parser import HTMLParser
from idlelib.iomenu import encoding






def http_curl(url):
    res = request.urlopen(url)
    if res.getcode() == 200:
        content = res.read().decode('utf-8', 'ignore')
        """
        print("content:%s", content)
        f = open('poem.txt', 'w', encoding = 'utf-8')
        f.write(content)
        f.close()
        """
    return content


def get_attr(attrs, name):
    for key, value in attrs:
        if key == name:
            return value
    return None


class get_poem_info(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.poem_list = []
        self.poems = {}
        self.typetag = False
        self.contag = False
        self.pattern = re.compile(r"""(\w+) # 诗词题目
                                    \((\w+)\) # 诗词作者""", re.X|re.S|re.M)
        
    
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and  get_attr(attrs, 'class') == 'guwencont2':
            #print("start_tag:%s" % tag)
            self.typetag = True
        if tag == 'a' and self.typetag:
            #print("start_tag:%s" % tag)
            self.contag = True
            self.poems['url'] = 'http://www.gushiwen.org' + get_attr(attrs, 'href')
            #print("url:%s" % self.poems['url'])
            
    def handle_data(self, data):
        #print("data :%s" % data)
        
        if self.contag and self.typetag:
            #print("data :%s" % data)
            #print("---")
            
            str = data
            m = self.pattern.search(str)
            if m:
                #print("m:%s" % m)
                self.poems['title'] = m.group(1)
                self.poems['author'] = m.group(2)
                print(self.poems)
                self.poem_list.append(self.poems)
                self.poems = {}
                
                """
                f = open('poem_list.txt', 'w+', encoding = 'utf-8')
                str = json.dumps(self.poem_list)
                f.write(str)
                f.close()
                """        
            
    def handle_endtag(self, tag):
        if tag == 'div':
            #print("end_tag: %s" % tag)
            self.typetag = False
        if tag == 'a':
            self.contag = False
            
class get_poem_content(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag = False
        self.text = ''
    
    
    def handle_starttag(self, tag, attrs):
        #1.有两首诗词没有匹配，《蜀道难》，原因:P标签没有center属性
        if tag == 'p' and get_attr(attrs, 'align') == 'center':
            self.tag = True
    
    def handle_data(self, data):
        if self.tag:
            self.text += data
            
    def handle_endtag(self, tag):
        if tag == 'p':
            self.tag = False
            


def poems_content(poem_list):
    for poem in poem_list:
        if poem['url']:
            print("title: %s author: %s url :%s" % (poem['title'], poem['author'], poem['url']))
            content = http_curl(poem['url'])
            c = get_poem_content()
            c.feed(content)
            print(c.text.replace('。', '。\n'))


def poem_re_content(poem_list):
    #燕歌行·并序 诗词内容标签是<p align="center">汉家烟尘在东北，汉将辞家破残贼。</p>类型，匹配失败
    #匹配到诗词前边的序，没有匹配到正文
    pattern = re.compile(r'<p.*?>(.*?)<\/p>')
    for poem in poem_list:
        if poem['url']: 
            str = http_curl(poem['url']) 
            m = pattern.search(str)
            #print(m)
            if m:
                print("title: %s author: %s url :%s" % (poem['title'], poem['author'], poem['url']))
                text = m.group(1).replace('<br />', '\n')
                print(text)

if __name__ == '__main__':
    url = 'http://www.gushiwen.org/gushi/tangshi.aspx'
    str = http_curl(url)
    c = get_poem_info()
    c.feed(str)
    print(c.poem_list)
    #1.第一种方法，通过htmlparse解析data
    #poems_content(c.poem_list)
    #2.第二种方法，通过re方式全文匹配
    poem_re_content(c.poem_list)