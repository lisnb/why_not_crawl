#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 01:14:52
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-10 16:28:24
# @Email: lisnb.h@gmail.com

"""
# @comment here:

"""
import urllib2
import urllib
import threading
import Queue
import url_lister
import urlparse
import socket
from util import utils

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
		while 1:
			try:
				self.u_lock.acquire()
				current_url=self.unvisit_queue.get(True,timeout=5)
				print '%s, Queue size: %s, Handling %s '%(self.name,self.unvisit_queue.qsize(),current_url)
				self.u_lock.release()
				
				urlopener=urllib2.urlopen(current_url,timeout=2)
				html=urlopener.read()
				urlopener.close()

				self.v_lock.acquire()
				self.visit_dict[current_url]=1
				self.v_lock.release()

				filename= config.http_repo_path+current_url.translate(utils.filename_table)[4:]+'.html'
				with open(filename,'w') as f:
					f.write(html)

				urllister=url_lister.URLLister()
				urllister.feed(html)
				print 'Contains href: %s'%len(urllister.hrefs)

				for href in urllister.hrefs:
					whole_href=urlparse.urljoin(current_url,href)
					self.u_lock.acquire()
					if not self.visit_dict.get(whole_href,0):	
						self.unvisit_queue.put(whole_href)
					self.u_lock.release()
				print 'Done, Queue Size : %s'%self.unvisit_queue.qsize()
			except (urllib2.URLError,urllib2.HTTPError),e:
				print e,1
				continue

			except Queue.Empty,e:
				print e,2
				break
			except socket.timeout, e:
				print e,4
				continue

			except Exception, e:
				print e,3
				continue
			
		
		
		


		





if __name__ == '__main__':
	pass






