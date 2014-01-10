#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 15:37:27
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-10 16:29:07
# @Email: lisnb.h@gmail.com

"""
# @comment here:

"""
import os
import config
import threading
import Queue
import time
from model import spider_thread


def run():
	if not os.path.isdir(config.http_repo_path):
		print 'Directory: %s not found, make it ...'%config.http_repo_path
		os.makedirs(config.http_repo_path)
	threadpool=[]
	v_lock=threading.RLock()
	u_lock=threading.RLock()
	visit_dict={}
	unvisit_queue=Queue.Queue()
	unvisit_queue.put(r'http://www.ict.ac.cn')
	spider=spider_thread.Spider('spider',visit_dict,unvisit_queue,v_lock,u_lock)
	spider.start()
	threadpool.append(spider)
	time.sleep(5)
	for i in range(10):
		sp=spider_thread.Spider('spider_%s'%i,visit_dict,unvisit_queue,v_lock,u_lock)
		sp.start()
		threadpool.append(sp)
	for t in threadpool:
		t.join()




if __name__ == '__main__':
	run()







	