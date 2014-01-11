#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 15:37:27
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-11 15:34:47
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
from model import pipe


def run():
	if not os.path.isdir(config.http_repo_path):
		print 'Directory: %s not found, make it ...'%config.http_repo_path
		os.makedirs(config.http_repo_path)
	threadpool=[]
	localpipe= pipe.Pipe(config.seed)
	spider=spider_thread.Spider('spider',localpipe)
	spider.start()
	threadpool.append(spider)
	time.sleep(5)
	for i in range(10):
		sp=spider_thread.Spider('spider_%s'%i,localpipe)
		sp.start()
		threadpool.append(sp)
	for t in threadpool:
		t.join()




if __name__ == '__main__':
	run()







	