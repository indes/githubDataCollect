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


class repository_list_item(scrapy.Item):
    name = scrapy.Field()
    describe = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()

    def item2dic(self):
        return {
            "name": self["name"],
            "category": self["category"],
            "describe": self["describe"],
            "link": self["link"]
        }


class repository_detail_item(scrapy.Item):
    readme = scrapy.Field()
    tags = scrapy.Field()
    project = scrapy.Field()
    watch_num = scrapy.Field(),
    star_num = scrapy.Field(),
    fork_num = scrapy.Field(),
    lang_list = scrapy.Field()

    def item2dic(self):
        return {
            "readme": self["readme"],
            "tags": self["tags"],
            "project": self["project"],
            "watch_num": self["watch_num"],
            "star_num": self["star_num"],
            "fork_num": self["fork_num"],
            "lang_list": self["lang_list"]
        }
