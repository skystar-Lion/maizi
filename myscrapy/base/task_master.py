#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import queue,random,time
from multiprocessing.managers import BaseManager

#生成存放数据的队列
task_queue = queue.Queue()
#存放获取数据的队列
result_queue = queue.Queue()

#从BaseManager继承QueueManager
class QueueManager(BaseManager):
    pass

#将数据队列注册到网络上,并关联队列
QueueManager.register('get_task', callable = lambda : task_queue)
QueueManager.register('get_result', callable = lambda : result_queue)

#绑定端口和校验码
manager = QueueManager(address=('127.0.0.1', 5555), authkey = b'abc')
#启动queue
manager.start()

#获取通过网络访问的queue对象
task = manager.get_task()
result = manager.get_result()

#写数据
for i in range(10):
	n = random.randint(0,1000)
	print("put task %d ..." % n)
	task.put(n)
#读取数据
print("try get result")
for i in range(10):
	r = result.get()
	print("get result is %s..." % r)

manager.shutdown()
print("master exit...")
