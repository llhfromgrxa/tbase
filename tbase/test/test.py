
import os
import sys
import time
sys.path.append('../')
import myexceptions
from multiprocessing import Process
import common
import communicator
import random

def make_msg(strlist):
    strlist.append(common.random_str())

def testtask(oriqueue):
    while True:
        getdata = oriqueue.get()
        if getdata:
            with open(getdata.get("wpath"), "ab") as wfile:
                wfile.write(getdata.get("msg"))
            # time.sleep(4)
            print getdata.get("wpath")+ "write over !"

def test():
    orimap=[]
    for pid in range(0,10):
        oriqueue = communicator.OriQueue()
        sender = Process(target=testtask, name='send', args=([oriqueue]))
        sender.start()
        orimap.append(oriqueue)
    while True:
        msg = common.random_str(30)
        index = random.randint(0,9)
        content = {
            "msg": msg+'\n',
            "wpath": "file"+str(index)+".txt"
        }
        orimap[index].put(content)
        print "oriqueue %d put over !"%index
        time.sleep(3)

if __name__ =="__main__":
    test()