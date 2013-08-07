# -*- coding:utf-8 -*-

"""web根应用
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-01 16:29:57
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""

import sys
import tornado.wsgi

sys.path.append("../")

from ..global_settings import *
from ..logger import sm_logger

class MainHandler(tornado.web.RequestHandler):
	"""web根应用"""
	def get(self):
		"""web.cfg的MainHandler就是当前根应用的模板"""
		sm_logger.debug("****")
		self.render( TEMPLATES['MainHandler'], title="电信微信服务平台")
