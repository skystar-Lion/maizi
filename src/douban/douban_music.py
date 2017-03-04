#-*- encoding=utf-8
'''
Created on 2017年3月2日

@author: Lion
'''
from urllib import request
from html.parser import HTMLParser


def get_attr_value(attrs, name):
    for key,value in attrs:
        if key == name:
            return value
    return None

def get_new_music(content):
    class new_music(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.musics_list = []
            self.music = {}
            self.nametag = False
            self.authertag = False
            self.scoretag = False
        
        def handle_starttag(self, tag, attrs):
            if tag == 'img' and get_attr_value(attrs, 'data-reactid') and get_attr_value(attrs, 'width') == '100%':
                self.music['img'] = get_attr_value(attrs, 'src')
            if tag == 'a' and get_attr_value(attrs, 'data-reactid') and get_attr_value(attrs, 'class') == 'album-title':
                self.nametag = True
            if tag == 'p' and get_attr_value(attrs, 'data-reactid'):
                self.authertag = True
            if tag == 'span' and get_attr_value(attrs, 'class') == 'score' and get_attr_value(attrs, 'data-reactid'):
                self.scoretag = True
        
        def handle_data(self, data):
            if self.nametag:
                self.music['name'] = data
            if self.authertag:
                self.music['author'] = data
            if self.scoretag:
                self.music['score'] = data
            self.musics_list.append(self.music)
            print(self.music)
    p = new_music()
    p.feed(content)
    return p.musics_list

                 
                                               
                
        

class music():
    def __init__(self):
        self.music_list=[]
    
    def get_info(self):
        url = 'https://music.douban.com/'
        res = request.urlopen(url)
        if res.getcode() ==200:
            content = res.read().decode('utf-8')
        f = open('music.txt', 'w', encoding = 'utf-8')
        f.write(content)
        f.close()
        get_new_music(content)
        

if __name__ == '__main__':
    c = music()
    c.get_info()