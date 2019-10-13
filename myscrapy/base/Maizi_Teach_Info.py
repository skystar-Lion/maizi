#!/usr/bin/env python3
"""
get the teacher infomation by  access maizi sits 
"""
# -*- encoding=utf-8 -*-

import re
import socket
from urllib import request
from urllib import error

#setting the socket response timeout
timeout = 10
socket.setdefaulttimeout(timeout)

def http_curl(url, page):
    """
       wrap the urllib.request.urlopen
    """
    try:
       res = request.urlopen(url)
    except error.HTTPError as e:
       print('the server can\'t fulfill the request')
       print('Error code', e.code, 'Error reason:', e.reason)
    except error.URLError as e:
       print('can\'t reach the server')
       print('Error reason', e.reason)
    else:
       return res.read().decode('utf-8')


def re_pattern(pattern, content):
    """
        wrap the re regex pattern
    """
    regex_pattern = re.compile(pattern)
    str = re.findall(regex_pattern, content)
    return str

    
if __name__ == "__main__":
    url_format = "http://www.maiziedu.com/course/teachers/?page={0}"
    pattern = (r"class=\"t3out\".*?title=\"([\w|_| ]+?)\".*?class=\"color66\""
            "span.*?\/span(.*?)\/p.*?\/li")
    fd = open('teacher_info.txt', 'w')
    for i in range(1, 27):
        url = url_format.format(i)
        curl_str = http_curl(url, i)
        #print(curl_str)
        teacher_info = re_pattern(pattern, curl_str.replace("<", "")\
        .replace(">", "").replace("\n", ""))
        #teacher_info = curl_str.replace("<", "").replace(">", "").replace("\n", "")
        #print(teacher_info)
        for i in teacher_info:
            #print(i[0], i[1])
            file_format = "姓名：{0}，简介：{1}\n".format(i[0].strip(), i[1].strip())
            fd.write(file_format)
            fd.write("\n")
    fd.close()


