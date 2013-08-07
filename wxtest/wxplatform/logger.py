# -*- coding:utf-8 -*-

"""
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-03 14:21:51
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""
# -*- coding:utf-8 -*-

"""日志处理
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-01 16:58:09
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""

import sys
import inspect

isBAE = True

try:
	from bae.api import logging as logging
except Exception, e:
	import logging
	isBAE = False

class BAElogger(object):

	def __init__(self):
		self.sm_logger = logging.getLogger("simple_debug")

	def get_cur_info(self):
		try:
			raise Exception
		except:
			f =  sys._getframe( 2 )

		moduleName = f.f_code.co_filename
		funcName = f.f_code.co_name
		lineNo = f.f_lineno #行号

		return ("[%s.%s-%s]" % (moduleName,funcName,lineNo))

	def debug(self,msg):
		self.sm_logger.debug("%s:%s" % (self.get_cur_info(),msg))

if isBAE:
	sm_logger = BAElogger()
else:
	sm_logger = logging.getLogger("simple_debug")
	sm_logger.setLevel(logging.DEBUG)

	ch = logging.StreamHandler()
	formatter = logging.Formatter('[%(asctime)s - %(module)s.%(funcName)s-%(lineno)d](%(levelname)s): %(message)s')
	ch.setFormatter(formatter)

	sm_logger.addHandler(ch)
