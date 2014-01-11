#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-11 15:02:25
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-11 15:35:33
# @Email: lisnb.h@gmail.com

"""
# @comment here:

"""
import Queue
import sys
sys.path.append('..')
import config
from threading import RLock

class Pipe(object):
	"""docstring for Pipe"""
	def __init__(self, seed):
		super(Pipe, self).__init__()
		self.seed = seed
		self.u_lock=RLock()
		self.v_lock=RLock()
		self.u_queue = Queue.Queue()
		self.u_dict={}
		self.v_dict={}
		self.init()

	def init(self):
		self.u_lock.acquire()
		self.u_queue.put(self.seed)
		self.u_lock.release()

	def put(self,obj):
		self.u_lock.acquire()
		if not self.u_dict.get(obj,False):
			self.u_dict[obj]=True
			self.u_queue.put(obj)
		self.u_lock.release()


	def get(self,timeout=config.queue_timeout):
		obj=None

		self.u_lock.acquire()
		while not obj:
			try:
				obj=self.u_queue.get(True,timeout)
			except Queue.Empty,e:
				print e 
				continue
			except Exception, e:
				print e 
				continue
		self.u_lock.release()

		self.v_lock.acquire()
		self.v_dict[obj]=True
		self.v_lock.release()

		return obj


	def getstatistics(self):
		sta={}
		self.v_lock.acquire()
		self.u_lock.acquire()
		sta['visited']=len(self.v_dict)
		sta['unvisited']=len(self.u_dict)-sta['visited']
		self.u_lock.release()
		self.v_lock.release()
		return sta,'visited: %s unvisited: %s'%(sta['visited'],sta['unvisited'])


if __name__ == '__main__':
	pass







	