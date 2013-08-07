wxtest
======

微信公众账号测试平台。本系统同时支持tornado和百度的BAE。

使用tornado建立的WEB服务平台
=========================

1. 运行WEB服务平台命令
------------------

		python mainServer

2. web应用配置
------------
* 配置文件

		config/web.cfg

* 添加一个WEB应用

	如下例所示，在[url-patterns]下添加:

		classes.web.TestHandler.TestHandler = /Test
		
	“=”号前面是类的地址路径。“=”号后面是类的URL映射地址。

	web应用编写方法参考：http://sebug.net/paper/books/tornado/#_4

* 添加一个模板

	如下例所示，在[templates]下添加:

		MainHandler = templates/index.html

	“=”号前面是程序内引用模板的名称。“=”号后面是模板位置。

* 程序内引用模板示例

		self.render(TEMPLATES['MainHandler'], title="电信微信服务平台")	

	模板编写方法参考：http://sebug.net/paper/books/tornado/#_5

使用BAE建立的WEB服务平台
=====================

1. 百度BAE配置
-------------
* 配置文件

		app.conf
		
* 在配置文件中添加一个WEB应用
		
	如下例所示，在handlers:下添加:

		- url : /Test
		script: index.py

	注意：此处添加的url必须与下面web应用配置的url映射地址一致。


2. web应用配置
-------------

* 配置文件

		config/web.cfg

* 在配置文件中添加一个WEB应用

	如下例所示，在[url-patterns]下添加:

		classes.web.TestHandler.TestHandler = /Test

		“=”号前面是类的地址路径。“=”号后面是类的URL映射地址。

	web应用编写方法参考：http://sebug.net/paper/books/tornado/#_4

3. 添加一个模板
-------------

* 如下例所示，在[templates]下添加:

		MainHandler = templates/index.html

	“=”号前面是程序内引用模板的名称。“=”号后面是模板位置。

* 程序内引用模板示例:

		self.render(TEMPLATES['MainHandler'], title="电信微信服务平台")

	模板编写方法参考：http://sebug.net/paper/books/tornado/#_5


