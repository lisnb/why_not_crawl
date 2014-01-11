#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 01:14:52
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-11 15:37:35
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
	def __init__(self,thread_name,pipe):
		super(Spider, self).__init__(name=thread_name)
		self.pipe=pipe

	def run(self):
		while 1:
			try:
				current_url=self.pipe.get()
				sta=self.pipe.getstatistics()
				print '%s, current: %s'%(sta[1],current_url)

				request = urllib2.Request(current_url)
				request.add_header('User-Agent',config.user_agent)
				urlopener=urllib2.urlopen(request,timeout=2)
				html=urlopener.read()
				urlopener.close()

				html=re.sub(r'<!--.*-->','',html)
				urllister=url_lister.URLLister()
				urllister.feed(html)

				charset=urllister.charset if urllister.charset else chardet.detect(html)['encoding']
				print 'charset: %s'%charset
				if not ('utf' in charset and '8' in charset):
					try:
						html=html.decode(charset).encode('utf-8')
					except Exception, e:
						print 'decode error... '
				filename= config.http_repo_path+current_url.translate(utils.filename_table)[4:]+charset+'-.html'
				with open(filename,'w') as f:
					f.write(html)

				
				for href in urllister.hrefs:
					whole_href=urlparse.urljoin(current_url,href)
					self.pipe.put(whole_href)
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






