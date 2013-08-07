# -*- coding:utf-8 -*-

"""微信接口应用
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-02 09:13:12
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""

import sys
import time
import hashlib

import tornado.wsgi

from ..logger import sm_logger
from ..MessageManage import PushMsg,MessageManage
from ..global_settings import *

class WXInterfaceHandler(tornado.web.RequestHandler):
	
	responseString = ""

	def get(self):
		"""接受get请求，提供微信服务器校验本接口地址"""
		sm_logger.debug("****")
		self.valid()
		self.write(self.responseString)

	def post(self):
		"""接受post请求，与微信用户进行消息交互"""
		sm_logger.debug("****")

		self.messageManage = MessageManage()
		self.responseMsg()
		self.write(self.responseString)

	# 微信接口地址校验
	def valid(self):
		"""接受微信服务器发来的校验码，校验成功后返回微信提供的校验码
		@return: 返回微信提供的随机字符串

		 echostr: 微信HTTP发来的随机字符串
		
		"""
		sm_logger.debug("****")
		echostr = self.get_argument('echostr','')
		if self._checkSignature():
			sm_logger.debug("echostr:%s" % echostr)
			self.responseString = echostr;

	def _checkSignature(self):
		"""接受微信服务器发来的校验信息，并进行校验
			@return: True-校验成功；Flase-校验失败

			HTTPRequst signature: 微信发来的微信加密签名

			HTTPRequst timestamp: 微信发来的时间戳

			HTTPRequst nonce: 微信发来的随机数

		"""
		sm_logger.debug("****")
		signature = self.get_argument('signature','')
		timestamp = self.get_argument('timestamp','')
		nonce = self.get_argument('nonce','')

		token = TOKEN
		tmpArr = [token, timestamp, nonce] 
		tmpArr.sort() 
		tmpStr = "".join(tmpArr)
		tmpStr = hashlib.sha1(tmpStr).hexdigest()
		sm_logger.debug("tmpStr:%s; signature:%s" % (tmpStr, signature))
		if tmpStr == signature :
			sm_logger.debug("return True!")
			return True
		else:
			sm_logger.debug("return False!")

		return False

	def responseMsg(self):
		"""解析微信用户推送的消息，并回复微信用户"""
		sm_logger.debug("****")
		postStr = self.request.body
		
		if postStr: # 解析微信推送的消息
			self.messageManage.handle(postStr);
			replyMsg = self.messageManage.getReplyMsg()
			self.responseString = replyMsg
		else:
			self.responseString = ""
