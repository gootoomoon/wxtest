# -*- coding:utf-8 -*-

"""微信WEB服务平台
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-01 15:23:54
@Copyright: asiainfo-linkage 2013
@version: $Revision$

本系统同时支持tornado和百度的BAE。当前文件是使用tornado建立的WEB服务平台

	1. B{运行WEB服务平台命令}
	
	>>> python mainServer

	2. B{web应用配置}
	
		- B{配置文件}

		>>> config/web.cfg

		- B{添加一个WEB应用}

			如下例所示，在[url-patterns]下添加::

			>>> classes.web.TestHandler.TestHandler = /Test

			“=”号前面是类的地址路径。“=”号后面是类的URL映射地址。

			web应用编写方法参考：U{http://sebug.net/paper/books/tornado/#_4}


		- B{添加一个模板}

			如下例所示，在[templates]下添加::

			>>> MainHandler = templates/index.html

			“=”号前面是程序内引用模板的名称。“=”号后面是模板位置。

			程序内引用模板示例::
		
			>>> self.render(TEMPLATES['MainHandler'], title="电信微信服务平台")

			模板编写方法参考：U{http://sebug.net/paper/books/tornado/#_5}

"""

import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from wxplatform.global_settings import *
from wxplatform.WebConfigParser import WebConfigParser
from wxplatform.logger import sm_logger

define("port", default=8888, help="微信平台", type=int)

reload(sys) 
sys.setdefaultencoding('utf8') 

def main():
	"""主函数"""
	sm_logger.debug("**start server**")
	webConfig = WebConfigParser(WEB_CONFIG_FILE)
	urlPatterns = webConfig.urlPatterns()
	webConfig.templates()
	settings = {"static_path": os.path.join(os.path.dirname(__file__), "static"),
				'debug' : True} # 设置static静态目录
	tornado.options.parse_command_line()
	urlPatterns.append((r"/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])))
	application = tornado.web.Application(urlPatterns, **settings)
	http_server = tornado.httpserver.HTTPServer(application)

	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
	
