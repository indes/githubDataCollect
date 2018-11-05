# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubdataItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    pass

# 大类别 小类别 项目名字 项目链接 项目描述


class crawlItem(scrapy.Item):
    cate = scrapy.Field()
    subcate = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    pass


class project_category_item(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()

    def item2dic(self):
        return {
            "name": self["name"],
            "link": self["link"]
        }
