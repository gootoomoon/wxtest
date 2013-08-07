# -*- coding:utf-8 -*-

"""
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-02 09:12:52
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""

import sys
import time
import tornado.wsgi

from xml.etree import ElementTree as ET
from tornado.util import import_object

from logger import sm_logger
from MessageConfigParser import MessageConfigParser
from global_settings import *

class PushMsg(object):
	"""消息推送对象"""
	fromUsername = ""
	"""微信用户"""
	toUsername = ""
	"""公众账号"""
	createTime =  ""
	"""消息创建时间"""
	msgType = ""
	"""消息类型"""
	content = ""
	"""消息文本内容"""
	msgId = ""
	"""消息ID"""
	location_X = ""
	"""地理位置纬度"""
	location_Y = ""
	"""地理位置经度"""
	scale = ""
	"""地图缩放大小"""
	label = ""
	"""地理位置信息"""
	title = ""
	"""消息标题"""
	description = ""
	"""消息描述"""
	url = ""
	"""消息链接"""
	event = ""
	"""事件类型，subscribe(订阅)、unsubscribe(取消订阅)、CLICK(自定义菜单点击事件)"""
	eventKey = ""
	"""事件KEY值，与自定义菜单接口中KEY值对应"""
	
class ReplyMsg(object):
	"""回复消息对象"""
	toUserName = ""
	"""接收方帐号（收到的OpenID）"""
	fromUserName = ""
	"""开发者微信号"""
	createTime = ""
	"""消息创建时间"""
	msgType = ""
	"""消息类型"""
	content = ""
	"""回复的消息内容,长度不超过2048字节"""
	musicUrl = ""
	"""音乐链接"""
	hQMusicUrl = ""
	"""高质量音乐链接，WIFI环境优先使用该链接播放音乐"""
	articleCount = ""
	"""图文消息个数，限制为10条以内"""
	articles = list()
	"""多条图文消息信息(NewsArticle)，默认第一个NewsArticle为大图"""
	articles 
	"""article(object) list"""

class NewsArticle(object):
	"""图文消息"""
	title = ""
	"""图文消息标题"""
	description = ""
	"""图文消息描述"""
	picUrl = ""
	"""图片链接，支持JPG、PNG格式，较好的效果为大图640*320，小图80*80。"""
	url = ""
	"""点击图文消息跳转链接"""

class MessageManage(object):
	"""消息处理

	message.cfg是回复消息的配置文件。以[root]配置为例:

	>>> 
	[root]
	command = 0
	class = wxplatform.MessageManage.TextMessage
	welcome = 欢迎参加电信营销与服务微信平台测试！发送指令“0”，返回主菜单。发送其他数字进入其他菜单。当前菜单如下：
		输入“1”，进入客户服务
		输入“2”，进入优惠信息查询
		输入“3”，进入营业厅服务

	1）command和class是必须配置项。

	2）command是接受的消息命令

	3）class是处理消息的类。处理消息类的结构是:

		>>> 
		class className(object):
			def msgHandle(self,pushMsg,config): # 是处理提交过来的消息。
												# pushMsg是提交过来的消息对象。
												# config是message的配置
				...
			return replyMsg 					# 回复微信的消息对象

	"""

	pushMsg = None
	"""微信提交过来的消息对象。"""

	replyMsg = None
	"""返回微信的消息对象。"""

	def __init__(self):
		sm_logger.debug("****")
		messageConfig = MessageConfigParser()
		self.config = messageConfig.config()
		self.replyMsg = ReplyMsg()

	def handle(self, postStr):
		"""处理提交过来的消息内容
		@param postStr: 提交过来的消息内容。消息内容应该是微信规定XML格式。
		"""
		sm_logger.debug("****")
		sm_logger.debug("postStr:" + postStr)
		self.pushMsg = self._pushMsgParser(postStr)
		if self.pushMsg:
			self._pushMsgHandle()

	def _pushMsgHandle(self):
		"""处理提交过来的消息对象"""
		sm_logger.debug("****")
		if self.pushMsg.msgType == PUSH_MSG_TYPE['text']: #如果是文本类型
			command = self.pushMsg.content.strip()
			if command:
				configSection = self._getConfigSection(command)

			if configSection: #如果消息配置项存在
				self._redirect(configSection)
			else:
				error_msg = self.config.get('exception','error')
				self.replyMsg = self._makeExceptionReplyMsg(error_msg)
	
	def _getConfigSection(self,command):
		"""根据命令从消息配置文件中查找配置项
		@param command: 用户从微信发送的命令 
		"""
		sm_logger.debug("****")
		section = None
		options = None
		configSection = None
		sections = self.config.sections()
		num = len(sections)
		for x in range(num):
			section = sections[x]
			config_command = ""
			try:
				config_command = self.config.get(section,'command')
			except Exception, e:
				sm_logger.debug("Exception:%s" % e)

			try:
				self.config.get(section,'class')
			except Exception, e:
				sm_logger.debug("Exception:%s" % e)

			if command == config_command:
				options = self.config.options(sections[x])
				break

		if options:
			configSection  = dict()
			num = len(options)
			for x in range(num):
				configSection[options[x]] = self.config.get(section, options[x])

		sm_logger.debug("return:%s" % configSection)
		return configSection

	def _redirect(self, configSection):
		"""转发到回复消息配置的类处理
		@param configSection: 回复消息配置
		"""
		sm_logger.debug("****")

		if configSection['class']:
			handler = configSection['class']
			try:
				handler = import_object(handler)
				handler = handler()
				self.replyMsg = handler.msgHandle(self.pushMsg, configSection)
			except Exception, e:
				sm_logger.debug("Exception:%s" % e)
				error_msg = (self.config.get('exception','missing') % configSection['command'])
				self.replyMsg = self._makeExceptionReplyMsg(error_msg)
				

	def getReplyMsg(self):
		"""返回回复微信的文本消息
		@return: 符合微信规范要求的xml文本格式。或是返回空 
		"""
		sm_logger.debug("****")
		replyMsgStr = ""

		if self.replyMsg:
			if self.replyMsg.msgType == REPLY_MSG_TYPE['text']:
				replyMsgStr = self._makeTextReplyMsg()
			# elif self.replyMsg.msgType == REPLY_MSG_TYPE['music']:
			# 	replyMsgStr = self._makeMusicReplyMsg()
			elif self.replyMsg.msgType == REPLY_MSG_TYPE['news']:
				replyMsgStr = self._makeNewsReplyMsg()
			else:
				sm_logger.debug("未知类型：%s" % self.replyMsg.msgType)
		else:
			error_msg = (self.config.get('exception','missing') % self.pushMsg.content)
			self.replyMsg = self._makeExceptionReplyMsg(error_msg)
			replyMsgStr = self._makeTextReplyMsg()

		sm_logger.debug("replyMsgStr:%s" % replyMsgStr)
		return replyMsgStr

	def _pushMsgParser(self,postStr):
		"""将微信推送的消息解析成对象
		@param postStr: 微信发来的POST请求文本内容
		@return: 解析后的微信消息对象
		"""
		sm_logger.debug("postStr:%s" % postStr)

		postObj = ET.fromstring(postStr)
		pushMsg = None
		try:
			pushMsg = PushMsg()
			fromUsername = postObj.find("FromUserName").text
			pushMsg.fromUsername = fromUsername

			toUsername = postObj.find("ToUserName").text
			pushMsg.toUsername = toUsername

			createTime = postObj.find("CreateTime").text
			pushMsg.createTime = createTime

			msgType = postObj.find("MsgType").text
			pushMsg.msgType = msgType

			msgId = postObj.find("MsgId").text
			pushMsg.msgId = msgId

			if msgType == PUSH_MSG_TYPE['text']: #文本消息
				content = postObj.find("Content").text
				content = content.encode('utf-8')
				pushMsg.content = content

			elif msgType == PUSH_MSG_TYPE['image']: #图片消息
				picUrl = postObj.find("PicUrl").text
				pushMsg.content = content

			elif msgType == PUSH_MSG_TYPE['location']: #地理位置消息
				location_X = postObj.find("Location_X").text
				location_Y = postObj.find("Location_Y").text
				scale = postObj.find("Scale").text
				label = postObj.find("Label").text
				pushMsg.location_X = location_X
				pushMsg.location_Y = location_Y
				pushMsg.scale = scale
				pushMsg.label = label

			elif msgType == PUSH_MSG_TYPE['link']: #链接消息
				title = postObj.find("Title").text
				description = postObj.find("Description").text
				url = postObj.find("Url").text
				pushMsg.title = title
				pushMsg.description = description
				pushMsg.url = url

			elif msgType == PUSH_MSG_TYPE['event']: #事件推送
				event = postObj.find("Event").text
				eventKey = postObj.find("EventKey").text
				pushMsg.event = event
				pushMsg.eventKey = eventKey

			else:
				sm_logger.debug("未知类型：%s"%msgType)
		except Exception, e:
			sm_logger.debug("Exception:%s" % e)

		sm_logger.debug("return:%s" % pushMsg.__dict__)
		return pushMsg
		
	def _makeTextReplyMsg(self):
		sm_logger.debug("****")
		
		textTpl = "<xml>\n\
					<ToUserName><![CDATA[%s]]></ToUserName>\n\
					<FromUserName><![CDATA[%s]]></FromUserName>\n\
					<CreateTime>%s</CreateTime>\n\
					<MsgType><![CDATA[%s]]></MsgType>\n\
					<Content><![CDATA[%s]]></Content>\n\
					<FuncFlag>0</FuncFlag>\n\
					</xml>"
		resultStr = textTpl % (self.replyMsg.toUsername, 
								self.replyMsg.fromUsername, 
								self.replyMsg.createTime, 
								self.replyMsg.msgType, 
								self.replyMsg.content)

		sm_logger.debug("resultStr:%s" % resultStr)
		return resultStr

	def _makeNewsReplyMsg(self):
		sm_logger.debug("****")
		
		articleCount = len(self.replyMsg.articles)
		if articleCount > 0:

			itemTpl = "\
					<item>\n\
						<Title><![CDATA[%s]]></Title>\n\
						<Description><![CDATA[%s]]></Description>\n\
						<PicUrl><![CDATA[%s]]></PicUrl>\n\
						<Url><![CDATA[%s]]></Url>\n\
					</item>"

			articlesContent = ""
			for x in range(articleCount):
				itemStr = itemTpl % (self.replyMsg.articles[x].title,
										self.replyMsg.articles[x].description,
										self.replyMsg.articles[x].picUrl,
										self.replyMsg.articles[x].url)
				articlesContent = articlesContent + itemStr

			textTpl = "<xml>\n\
						<ToUserName><![CDATA[%s]]></ToUserName>\n\
						<FromUserName><![CDATA[%s]]></FromUserName>\n\
						<CreateTime>%s</CreateTime>\n\
						<MsgType><![CDATA[%s]]></MsgType>\n\
						<ArticleCount>%s</ArticleCount>\n\
						<Articles>\n%s\n</Articles>\n\
						</xml>"
			resultStr = textTpl % (self.replyMsg.toUsername, 
									self.replyMsg.fromUsername, 
									self.replyMsg.createTime, 
									self.replyMsg.msgType,
									articleCount, 
									articlesContent)
		else:
			error_msg = (self.config.get('exception','missing') % self.pushMsg.content)
			self.replyMsg = self._makeExceptionReplyMsg(error_msg)
			resultStr = self._makeTextReplyMsg()

		sm_logger.debug("resultStr:%s" % resultStr)
		return resultStr

	def _makeExceptionReplyMsg(self,exception_msg):
		replyMsg = ReplyMsg()
		replyMsg.toUsername = self.pushMsg.fromUsername
		replyMsg.fromUsername = self.pushMsg.toUsername
		replyMsg.createTime = str(int(time.time()))
		replyMsg.msgType = REPLY_MSG_TYPE['text']
		replyMsg.content = exception_msg
		return replyMsg

class TextMessage():
	"""文本回复消息对象"""
	msgType = ""
	
	def msgHandle(self, pushMsg, configSection):
		"""处理文本信息
		@param pushMsg: 回复消息对象
		@param configSection: 消息配置项
		"""
		sm_logger.debug("pushMsg:%s" % pushMsg.__dict__)
		sm_logger.debug("configSection:%s" % configSection)
		replyMsg = None

		if pushMsg and configSection:
			replyMsg = ReplyMsg()
			replyMsg.toUsername = pushMsg.fromUsername
			replyMsg.fromUsername = pushMsg.toUsername
			replyMsg.createTime = str(int(time.time()))
			replyMsg.msgType = REPLY_MSG_TYPE['text']

			try:
				content = configSection['welcome']
			except Exception, e:
				sm_logger.debug("Exception:%s" % e)
				replyMsg = None

			replyMsg.content = content

		sm_logger.debug("replyMsg:%s" % replyMsg.__dict__)
		return replyMsg

class NewsMessage():
	"""图文回复消息对象
		1. 消息配置文件设置

			>>> articles = wxplatform.query.ProductInfo.ProductInfo 

		2. 实现类的接口

			>>> 
			from ..MessageManage import NewsArticle
			class ProductInfo(object):	
				def queryArticles(self, pushMsg, configSection): #返回NewsArticle的list
	"""
	msgType = ""
	
	def msgHandle(self, pushMsg, configSection):
		"""处理文本信息
		@param pushMsg: 回复消息对象
		@param configSection: 消息配置项
		"""
		sm_logger.debug("pushMsg:%s" % pushMsg.__dict__)
		sm_logger.debug("configSection:%s" % configSection)
		replyMsg = None

		if pushMsg and configSection:
			replyMsg = ReplyMsg()
			replyMsg.toUsername = pushMsg.fromUsername
			replyMsg.fromUsername = pushMsg.toUsername
			replyMsg.createTime = str(int(time.time()))
			replyMsg.msgType = REPLY_MSG_TYPE['news']

			try:
				articlesHandler = configSection['articles']
				articlesHandler = import_object(articlesHandler)
				articlesHandler = articlesHandler()
				replyMsg.articles = articlesHandler.queryArticles(pushMsg, configSection)
			except Exception, e:
				sm_logger.debug("Exception:%s" % e)
				replyMsg = None

		sm_logger.debug("replyMsg:%s" % replyMsg.__dict__)
		return replyMsg