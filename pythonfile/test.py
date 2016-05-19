#!/usr/bin/python
#create a daemon
import threading
import time
 
def worker():
    time.sleep(3)
    print "worker"
 
t=threading.Thread(target=worker)
t.setDaemon(True)
t.start()
print "haha11"
print "haha"