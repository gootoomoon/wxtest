# -*- coding:utf-8 -*-

"""产品信息查询
@author: U{jinlei<mailto:jinlei3@asiainfo-linkage.com>}
@date: 2013-08-03 19:38:35
@Copyright: asiainfo-linkage 2013
@version: $Revision$
"""

from ..global_settings import *
from ..MessageManage import NewsArticle

class ProductInfo(object):
	"""docstring for ProductInfo"""
	
	def queryArticles(self, pushMsg, configSection):
		articles = list()

		article1 = NewsArticle()
		article1.title = "产品信息查询"
		article1.description = ""
		article1.picUrl = BAE_URL + "static/images/logo.png"
		article1.url = "http://telecomtest.duapp.com/static/html/productInfo.html"
		articles.append(article1)

		article2 = NewsArticle()
		article2.title = "基本信息"
		article2.description = "查询已经订购的产品信息"
		article2.picUrl = ""
		article2.url = "#"
		articles.append(article2)

		article3 = NewsArticle()
		article3.title = "商品信息"
		article3.description = "查询已经订购的套餐"
		article3.picUrl = ""
		article3.url = "#"
		articles.append(article3)

		return articles