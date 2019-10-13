#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import time,sys,queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
	pass

QueueManager.register('get_task')
QueueManager.register('get_result')

server_addr = '127.0.0.1'
print("connect to the server %s..." % server_addr)

s = QueueManager(address = (server_addr, 5555), authkey = b'abc')
s.connect()

task = s.get_task()
result = s.get_result()

for i in range(10):
	try:
		n = task.get()
		print("run task %d * %d ..." % (n, n))
		r = "%d * %d = %d" % (n, n, n*n)
		result.put(r)
	except Queue.Empty:
		print("task queue is empty")

print("work over...")

