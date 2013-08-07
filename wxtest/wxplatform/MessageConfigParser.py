# -*- coding:utf-8 -*-

"""
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-02 09:12:45
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""

import sys
import ConfigParser

from global_settings import *
from logger import sm_logger

class MessageConfigParser:
	def __init__(self):
		configFile = MESSAGE_CONFIG_FILE
		self.configFile = configFile

	def config(self):
		sm_logger.debug("****")
		try:
			configData = open(self.configFile,"r");
		except Exception, e:
			sm_logger.debug("没有找到" + self.configFile + ":"+e);
			sys.exit();

		try:
			config = ConfigParser.ConfigParser();
			config.readfp(configData);
			configData.close();
		except ConfigParser.Error, e:
			sm_logger.debug("配置文件格式错误:" + e);
		return config;

