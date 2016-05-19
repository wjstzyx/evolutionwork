import threading
from time import ctime,sleep






def music(name1,name2):
    for i in range(2):
        print "I was listening to %s %s. %s" %(name1,name2,ctime())
        sleep(2)


def main_fun():
	threads = []
	name1='dhdh'
	arges=range(1,3)
	for i in range(1,3):
		threads.append(threading.Thread(target=music,args=(name1,i)))


	print "### %s" %ctime()
	print threads


	for t in threads:
	    t.setDaemon(True)
	    t.start()
	t.join()
	print "all over %s" %ctime()

main_fun()