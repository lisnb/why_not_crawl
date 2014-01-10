#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: LiSnB
# @Date:   2014-01-10 19:15:52
# @Last Modified by:   LiSnB
# @Last Modified time: 2014-01-10 22:58:56
# @Email: lisnb.h@gmail.com

"""
# @comment here:

"""
import config
import chardet
import urllib2
import re
from model import url_lister

def transferencode():
	with open(config.http_repo_path+'---awtrc-ict-ac-cn-index-php-mact=News,cntnt01,detail,0&cntnt01articleid=217&cntnt01detailtemplate=custom_detail&cntnt01lang=zh_CN&cntnt01returnid=79.html') as f:
		html=f.read()
	print chardet.detect(html)
	html=html.encode('gb2312')
	with open('utf.html','w') as f:
		f.write(html)


def getinfo():
	urls=['http://www.baidu.com','http://www.ict.ac.cn','http://www.douban.com']
	for url in urls:
		opener=urllib2.urlopen(url)
		urllister=url_lister.URLLister()
		html=re.sub(r'<!--.*-->','',opener.read())
		urllister.feed(html)
		print urllister.charset
		print chardet.detect(html)



if __name__ == '__main__':
	# transferencode()
	getinfo()
# [('charset', 'gbk')]
# [('name', 'robots'), ('content', 'all')]
# [('name', 'author'), ('content', 'w3school.com.cn')]





	