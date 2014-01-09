#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 01:14:52
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-10 01:31:46
# @Email: lisnb.h@gmail.com

"""
# @comment here:

"""
import urllib2
import urllib
import threading
import Queue

import sys
sys.path.append('..')
import config


class Spider(threading.Thread):
	"""docstring for Spider"""
	def __init__(self,thread_name,visit_dict,unvisit_queue,v_lock,u_lock):
		super(Spider, self).__init__(name=thread_name)
		self.v_lock=v_lock
		self.u_lock=u_lock
		self.visit_dict=visit_dict
		self.unvisit_queue=unvisit_queue

	def run(self):
		self.u_lock.acquire()
		current_url=self.unvisit_queue.get(True,timeout=5)
		self.u_lock.release()
		

		





if __name__ == '__main__':
	pass






