# -*- coding:utf-8 -*-

"""web配置文件解析
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-01 15:27:35
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""

import sys
import ConfigParser

from global_settings import *
from logger import sm_logger

class WebConfigParser:
	"""web配置文件解析"""

	def __init__(self, configFile):
		self.config = self.__getConfig(configFile)

	def __getConfig(self,configFile):
		try:
			configData = open(configFile,"r");
		except Exception, e:
			sm_logger.debug("没有找到" + configFile + "！")
			sys.exit()

		try:
			config = ConfigParser.ConfigParser();
			config.optionxform = str # 区别大小写
			config.readfp(configData);
			configData.close();
		except ConfigParser.Error, e:
			sm_logger.debug("配置文件格式错误:" , e)
			sys.exit()

		return config

	def urlPatterns(self):
		sm_logger.debug("****")

		section = "url-patterns"
		options = self.config.options(section)

		num = len(options)
		urlPatterns = list()
		for x in range(num):
			option = options[x]
			pattern = (self.config.get(section,option),option)
			urlPatterns.append(pattern)

		sm_logger.debug(urlPatterns)
		return urlPatterns

	def templates(self):
		sm_logger.debug("****")
		section = "templates"
		options = self.config.options(section)

		num = len(options)
		for x in range(num):
			option = options[x]
			TEMPLATES[option] = self.config.get(section,option)

		sm_logger.debug(TEMPLATES)
