# -*- coding:utf-8 -*-

"""微信WEB在百度BAE平台的WEB应用
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-01 15:23:54
@Copyright: asiainfo-linkage 2013
@version: $Revision$

本系统同时支持tornado和百度的BAE。当前文件是支持BAE的WEB应用。

1.B{百度BAE配置}
	- 配置文件

		>>> app.conf
		
	- 在配置文件中添加一个WEB应用
		
	如下例所示，在handlers:下添加:

		>>> 
		- url : /Test
		script: index.py

	注意：此处添加的url必须与下面web应用配置的url映射地址一致。


2.B{web应用配置}

	- 配置文件

		>>> config/web.cfg

	- 在配置文件中添加一个WEB应用

		如下例所示，在[url-patterns]下添加:

		>>> classes.web.TestHandler.TestHandler = /Test

		“=”号前面是类的地址路径。“=”号后面是类的URL映射地址。

		web应用编写方法参考：http://sebug.net/paper/books/tornado/#_4

	3. B{添加一个模板}

	- 如下例所示，在[templates]下添加:

		>>> MainHandler = templates/index.html

		“=”号前面是程序内引用模板的名称。“=”号后面是模板位置。

	- 程序内引用模板示例:

		>>> self.render(TEMPLATES['MainHandler'], title="电信微信服务平台")

		模板编写方法参考：http://sebug.net/paper/books/tornado/#_5
"""

import tornado.wsgi

from wxplatform.global_settings import *
from wxplatform.logger import sm_logger
from wxplatform.WebConfigParser import WebConfigParser


sm_logger.debug("**start**")
webConfig = WebConfigParser(WEB_CONFIG_FILE)
urlPatterns = webConfig.urlPatterns()
webConfig.templates()

# 默认支持百度BAE
app = tornado.wsgi.WSGIApplication(urlPatterns)
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
