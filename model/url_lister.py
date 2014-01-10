#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 15:01:51
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-10 16:12:31
# @Email: lisnb.h@gmail.com

"""
# @comment here:

"""

from sgmllib import SGMLParser
import urllib2
import sys
sys.path.append('..')
import config


class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.hrefs=[]

	def a_filter(self,href):
		for fiter in config.ignore_url_list:
			if fiter in href:
				return False
		return True

	def start_a(self,attrs):
		href = [v for k,v in attrs if k=='href' and 'ict' in v and self.a_filter(v)]
		self.hrefs.extend(href)



if __name__ == '__main__':
	pass







	