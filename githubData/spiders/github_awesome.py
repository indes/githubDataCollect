# -*- coding: utf-8 -*-
import scrapy
import csv
from githubData.items import project_category_item
from scrapy import Request, log
from scrapy.selector import Selector
import pprint
import json


class github_awesome_spider(scrapy.Spider):
    name = 'github_awesome'

    start_urls = [
        'https://github.com/sindresorhus/awesome/blob/master/readme.md']

    def parse(self, response):

        # print(response.body)
        categories = response.xpath('//h2/text()').extract()[1:-1]
        for category_1 in categories:
            # 一级分类
            print("-----------" + category_1+"-----------")

            categories_2 = response.xpath(
                "//h2[text()='{}']/following-sibling::ul[1]/li".format(category_1)).extract()

            for category_2 in categories_2:
                # 二级分类
                category_item = project_category_item()

                name = Selector(text=category_2).xpath(
                    "//li/a/text()").extract()[0]
                category_item["name"] = "{}/{}".format(category_1, name)
                # print(category_name)
                category_item["link"] = Selector(text=category_2).css(
                    "a::attr(href)").extract()

                yield category_item

            print("\n\n")
