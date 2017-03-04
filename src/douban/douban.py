#-*- coding=utf-8 -*-
'''
Created on 2017年2月28日

@author: Lion
'''

import socket
from html.parser import HTMLParser
from urllib  import request
from urllib import error




timeout = 10
socket.setdefaulttimeout(timeout)

def http_curl(url):
    try:
        res = request.urlopen(url)
    except error.HTTPError as e:
        print("the server can't fulfill the request")
        print("ERROR code",e.code,"ERROR reason",e.reason)
    except error.URLError as e:
        print("can't reach the server")
        print("ERROR reason",e.reason)
    else:
        return res.read().decode('utf-8')
    
class nowplay(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies=[]
        
    def handle_starttag(self, tag, attrs):
        def get_val(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]            
            return None            

        if tag == "li" and get_val(attrs, "data-category") == "nowplaying" and get_val(attrs, "data-title"):
 
            movie = {}
            movie["name"] = get_val(attrs, "data-title")
            movie["score"] = get_val(attrs, "data-score")
            movie["star"] = get_val(attrs, "data-star")
            movie["time"] = get_val(attrs, "data-duration")
            movie["director"] = get_val(attrs, "data-director")
            movie["actor"] = get_val(attrs, "data-actors")
            self.movies.append(movie)
            print("{0:#<30} {1:#<5} {2:#<5} {3:#<20} {4:#<30} {5:#<50}".format(movie["name"], movie["score"], movie["star"], movie["time"],movie["director"], movie["actor"]))
            #print("%s %s %s %s %s %s" % (movie["name"], movie["score"], movie["star"], movie["time"],movie["director"], movie["actor"]))

class upcoming(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.movice = {}
        self.flag = False
        
    def handle_starttag(self, tag, attrs):
        def get_val(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]            
            return None
        if tag == "li" and get_val(attrs, "data-category") == "upcoming":
            self.movice["name"] = get_val(attrs, "data-title")
            self.movice["time"] = get_val(attrs, "data-duration")
            self.movice["director"] = get_val(attrs, "data-director")
            self.movice["actor"] = get_val(attrs, "data-actors")
            print("%-20s %-20s %-30s %-50s" % (self.movice["name"], self.movice["time"], self.movice["director"], self.movice["actor"]),end="")
        if tag == "li" and get_val(attrs, "class") == "release-date":
            self.flag = True
                
            
    def handle_data(self, data):
        if self.flag:
            self.movice["uptime"] = str(data).strip().replace("\r\n", "")
            print("%s" % (self.movice["uptime"]))
        self.flag = False
    
               
            


 
            
if __name__ == '__main__':
    url = "https://movie.douban.com/nowplaying/beijing/"
    text = http_curl(url)
    #print(text)
    """<li
                        id="25765735"
                        class="list-item"
                        data-title="金刚狼3：殊死一战"
                        data-wish="23736"
                        data-duration="123分钟(中国大陆)"
                        data-region="美国"
                        data-director="詹姆斯·曼高德"
                        data-actors="休·杰克曼 / 帕特里克·斯图尔特 / 达芙妮·基恩"
                        data-category="upcoming"
                        data-enough="false"
                        data-subject="25765735">  
                        <ul class="">
                            <li class="poster">
                                    <a class="ticket-btn"
                                        href="https://movie.douban.com/subject/25765735/?from=playing_poster"
                                        target="_blank"
                                        data-psource="poster">
                                        <img src="https://img3.doubanio.com/view/movie_poster_cover/mpst/public/p2431980130.jpg" alt="金刚狼3：殊死一战" rel="nofollow" class="" />
                                    </a>
                            </li>
                            <li class="stitle">
                                    <a class="ticket-btn" href="https://movie.douban.com/subject/25765735/?from=playing_poster" target="_blank" title="金刚狼3：殊死一战" data-psource="title">
                                        金刚狼3：殊死...
                                    </a>
                            </li>
                            <li class="release-date">
                                03月03日上映
                            </li>
                                <li class="sbtn">
                                    <a class="ticket-btn"
                                        href="https://movie.douban.com/subject/25765735/cinema/beijing/?from=playing_btn"
                                        target="_blank"
                                        data-subject="25765735"
                                        data-title="金刚狼3：殊死一战"
                                        data-psource="btn">
                                            选座购票
                                    </a>
                                </li>
                        </ul>
                    </li>"""
    #parser = nowplay()
    parser = upcoming()
    parser.feed(text)
    parser.close()
    
    
    