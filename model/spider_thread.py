#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 01:14:52
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-11 15:01:15
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
import chardet
import re
from util import utils

import sys
sys.path.append('..')
import config


class Spider(threading.Thread):
	"""docstring for Spider"""
	def __init__(self,thread_name,visit_list,unvisit_queue,unvisit_list,v_lock,u_lock):
		super(Spider, self).__init__(name=thread_name)
		self.v_lock=v_lock
		self.u_lock=u_lock
		self.unvisit_list=unvisit_list
		self.visit_list=visit_list
		self.unvisit_queue=unvisit_queue

	def run(self):
		while 1:
			try:
				self.u_lock.acquire()
				current_url=self.unvisit_queue.get(True,timeout=5)
				print '%s, Queue size: %s, Handling %s '%(self.name,self.unvisit_queue.qsize(),current_url)
				self.u_lock.release()
				
				self.v_lock.acquire()
				self.visit_list.append(current_url)
				self.v_lock.release()

				request = urllib2.Request(current_url)
				request.add_header('User-Agent',config.user_agent)
				urlopener=urllib2.urlopen(request,timeout=2)
				html=urlopener.read()
				html=re.sub(r'<!--.*-->','',html)
				urlopener.close()

				urllister=url_lister.URLLister()
				urllister.feed(html)

				charset=urllister.charset if urllister.charset else chardet.detect(html)['encoding']
				print 'charset: %s'%charset
				if not ('utf' in charset and '8' in charset):
					try:
						html=html.decode(charset).encode('utf-8')
					except Exception, e:
						print 'decode error... '
				filename= config.http_repo_path+current_url.translate(utils.filename_table)[4:]+'.html'
				with open(filename,'w') as f:
					f.write(html)

				
				self.v_lock.acquire()
				for href in urllister.hrefs:
					whole_href=urlparse.urljoin(current_url,href)
					if whole_href not in self.visit_list and whole_href not in self.unvisit_list:
						self.u_lock.acquire()	
						self.unvisit_queue.put(whole_href)
						self.unvisit_list.append(whole_href)
						self.u_lock.release()
				self.v_lock.release()
				# print 'Done, Queue Size : %s'%self.unvisit_queue.qsize()
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






