#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 15:01:51
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-10 22:50:34
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
		self.charset=''
		self.charsetget=False

	def a_filter(self,href):
		for fiter in config.ignore_url_list:
			if fiter in href:
				return False
		return True

	def start_a(self,attrs):
		href = [v for k,v in attrs if k=='href' and 'ict' in v and self.a_filter(v)]
		self.hrefs.extend(href)


	def start_meta(self,attrs):
		if not self.charsetget:
			for k,v in attrs:
				if k=='charset':
					self.charset=v
					self.charsetget=True
					break
				if k=='content' and 'charset' in v:
					vs=[x.strip() for x in v.replace(' ','').split(';') if x.startswith('charset')]
					if len(vs) is 0:
						break
					else:
						self.charset=vs[0][8:]
						self.charsetget=True





if __name__ == '__main__':
	pass







	