# -*- coding=utf-8 -*-
'''
Created on 2017年3月3日

@author: Lion
'''

from urllib import request
from html.parser import HTMLParser
import os
import threading
import random
import time
import datetime



img_list = []
task_list = []
Glock = threading.Condition()
total_tasks_num = 0
c_processed_num = 0
p_processed_num = 0
p_error_num = 0
p_error_task = []
c_error_task = []

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
        print('url request error...')
        return None



def release_task(url):
    global total_tasks_num
    global task_list
    
    class info_parser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.info = {}
            self.tag = False
            
        def handle_starttag(self, tag, attrs):
            #获取贴吧发言人的个人信息页面
            if (tag == 'a' and get_attrs(attrs, 'class') == 'frs-author-name j_user_card ' and 
                get_attrs(attrs, 'target')):
                self.info['url'] = 'http://tieba.baidu.com' + get_attrs(attrs, 'href')
                self.tag = True
                
        def handle_data(self, data):
            if self.tag:
                self.info['name'] = data
                #获取python吧 发言人的名称，如果是多次发言，只记录一次信息
                if self.info not in task_list:
                    task_list.append(self.info)
                    #print(self.info)
                    #这里清空self.info字典是因为，如果不清空，infos列表内存实际记录的是字典info的key地址，最后会导致信息多次重复
                    self.info = {}                    
        
        def handle_endtag(self, tag):
            if tag == 'a':
                self.tag = False    
    
    content = http_curl(url)
    if content:
        text = content.decode('utf-8')                
        p = info_parser()
        p.feed(text)
        total_tasks_num = len(task_list)
        
        print(task_list)
        print('manager release %s tasks totally...' % total_tasks_num)
        return task_list


def create_img_url(task):
    global p_error_task
    
    class img_parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.atag = False
            self.url_list = {}
            
        def handle_starttag(self, tag, attrs):
            if tag == 'a' and get_attrs(attrs, 'class') == 'userinfo_head':
                self.atag = True
            if tag == 'img' and self.atag:
                self.url_list['url'] = get_attrs(attrs, 'src')
                self.url_list['name'] = task['name']
                
        def handle_endtag(self, tag):
            if tag == 'a':
                self.atag = False
    
    url = task['url']
    str = http_curl(url)
    try:
        text = str.decode('utf-8')
    except UnicodeDecodeError as e:
        err_str = 'url: %s request  error: %s' % (url, e)
        p_error_task.append(err_str)
        # return -1 代表吧主的页面url不存在，访问出错
        return -1
    
    p = img_parser()
    p.feed(text)
    img_list.append(p.url_list)
    p.url_list = {}
    return 0           
                    
class productor(threading.Thread):
    #task_list parameter represents all task,it's a list consist of dict(task['name'] and task['url'])
    def __init__(self):
        super().__init__()
    
    def run(self):
        global img_list
        global Glock
        global p_processed_task
        global p_error_task
        global p_error_num
        global p_processed_num
        global task_list
        
        
        #只要生产者生产的数量没有达到总量，就继续执行
        while (p_processed_num + p_error_num) < total_tasks_num:
            time.sleep(random.randint(1,3))            
            Glock.acquire()
            #print("processed: %s,error: %s, total: %s" % (p_processed_num, p_error_num, total_tasks_num))
            #print('task_list:%s' % len(task_list))
            
            if len(task_list) > 0:
                task = task_list.pop()
                # create_img_url() 负责将原始的url_list信息提取然后添加到img_list
                status = create_img_url(task)
                if status:
                    p_error_num += 1
                else:
                    p_processed_num += 1
                
                if len(img_list) > 0 and len(img_list) <= total_tasks_num/3:
                    print('product_thread_id: %s,current tasks: %s' % (threading.current_thread(), len(img_list)))
                    Glock.notify_all()
                elif len(img_list) >= total_tasks_num/3:
                    print('product_thread_id: %s,have create enough tasks: %s' % (threading.current_thread(), len(img_list)))
                    Glock.wait()           
            Glock.release()
            
        print('%s tasks have been done by productor and there are %s task error...' % (p_processed_num, p_error_num))
        #print('productor task num:%s,len img_list num:%s' % (p_processed_num, len(img_list)))
        if p_error_num:
            print('error info:%s' % p_error_task)
        #print('work status as follow: %s,totally: %s' % (img_list, len(img_list)))
        
        


class consumer(threading.Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        global img_list
        global Glock
        global c_processed_task
        global c_processed_num
        global total_tasks_num
        global p_error_num
        
        #如果当前已经处理的任务数和生产的总任务数相等，说明消费者消费完毕，就退出线程，负责继续
        while True:
            Glock.acquire()
            #如果当前确定还有待处理任务数，则等待处理
            if c_processed_num < (total_tasks_num - p_error_num):
                left_task = len(img_list)
                if left_task == 0:
                    print('consumer_thread_id: %s waiting,current tasks: %s' % (threading.current_thread(), len(img_list)))
                    Glock.wait()
                elif left_task < total_tasks_num/2:                                                      
                    task = img_list.pop()
                    print('consumer_thread_id: %s,current tasks not enough,left: %s' % (threading.current_thread(), len(img_list)))  
                    c_processed_num += 1
                    Glock.notify_all()
                    #开始下载图片
                    download_img(task['url'], task['name'])   

            else:
                Glock.release()
                break
            Glock.release()
            time.sleep(random.randint(1,2))
        print('current %s tasks have been done,consumer_thread_id: %s will quit' % (p_processed_num, threading.current_thread()))

            
def download_img(url, filename):     
    
    if not os.path.exists('image'):
        os.mkdir('image')
    filename = 'image/' + filename + '.jpg'
    page_content = http_curl(url)
    if page_content:
        content = page_content
        f = open(filename, 'wb')
        f.write(content)
        f.close()

"""                 
class test(threading.Thread):
    def run(self):
        for i in range(2):
            Glock.acquire()
            print('2---%s' % threading.current_thread())
            Glock.release()
"""

if __name__ == "__main__":
    #begin = datetime.datetime.now()
    url = 'http://tieba.baidu.com/f?kw=python&fr=ala0&tpl=5'
    tasks = release_task(url)
    for i in range(2):
        #test().start()
        p = productor()   
        p.start()

    for i in range(4):
        c = consumer()
        c.start()
    #统计时间代码有问题，因为主线程不能等待任何一个线程结束，会死锁
    #end = datetime.datetime.now()
    #print('program run time:%s' % (end-begin))
