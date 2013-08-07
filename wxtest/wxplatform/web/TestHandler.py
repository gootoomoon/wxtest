# -*- coding:utf-8 -*-

"""测试WEB应用
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-01 16:26:26
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""


import sys
import time
import tornado.wsgi

from ..logger import sm_logger

class TestHandler(tornado.web.RequestHandler):
	def get(self):
		"""接受HTTP Get请求"""
		sm_logger.debug("****")
		timeStr = str(int(time.time()))
		self.write("timeStr:%s"%timeStr)