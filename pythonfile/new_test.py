import multiprocessing
import time
import threading

def do_fun(i,j):
    time.sleep(1)
    print i,j

def aaa(i):
    print 'Process %s' % (i)
    for a in range(2):
        for b in range(3):
            print '@@@@@@@@@@@ %s' % (i)
            t = threading.Thread(target=do_fun, args=(a,b,))
            t.start()
            print '########### %s' % (i)









def multi_fun_cpu(fun_name,fun_argvslist,num_of_processes):
    pool = multiprocessing.Pool(processes=num_of_processes)
    result = []
    for argv in fun_argvslist:
        result.append(pool.apply_async(fun_name,argv))
    pool.close()
    pool.join()
    print '###################'
    # for res in result:
    #     print res.get()
    # print "Sub-process(es) done."


if __name__ == "__main__":
    multi_fun_cpu(aaa,[(1,),(2,),(3,),(4,)],2)