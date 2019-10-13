# -*- coding=utf-8 -*-
'''
Created on 2017��3��3��

@author: Lion
'''

import threading
import time
import random


def work_fun():
    print('work threading %s is started' % threading.current_thread())
    time.sleep(random.random())
    print('work threading %s is stoped' % threading.current_thread())
    
def main_thread_demo():
    """
    for i in range(10):
        threading.Thread(target=work_fun_lock, args = [semp]).start()
    """
    for i in range(2):
        productor().start()
    for j in  range(10):
        consumer().start()

def work_fun_lock(lock):
    lock.acquire()
    work_fun()
    lock.release()
    
    
class productor(threading.Thread):    
    def run(self):
        global money
        global gcondition
        money = 0
        
        while money < 500000:
            gcondition.acquire()
            put_money = random.randint(10000,20000)
            money += put_money
            print("money add: %s, totally: %s" % (put_money,money))
            gcondition.notify_all()
            gcondition.release()
        print("current money add up %s:!" % money)
       
    
class consumer(threading.Thread):
    def run(self):
        global money
        global gcondition
        gcondition.acquire()
        get_money = random.randint(500,5000)
        while money < get_money:
            gcondition.wait()
            print("current money not enough: %s,left: %s" % (get_money,money))
        money -= get_money
        print("money reduce: %s,total: %s" % (get_money,money))
        gcondition.release()


        
        
gcondition = threading.Condition()
money = 0
if __name__ == '__main__':
    #glock = threading.Lock()
    #semp = threading.Semaphore(3)
    #main_thread_demo(semp)
    
    main_thread_demo()