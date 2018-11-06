# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from githubData.items import repository_list_item
from scrapy import Request, log
from scrapy.selector import Selector
import pprint
import pymongo
import json
import time


class github_repository_list_spider(scrapy.Spider):
    name = 'repository_list'

    def start_requests(self):
        client = pymongo.MongoClient(
            host="127.0.0.1", port=29197)
            
        client["github"].authenticate("github", "git332", "github")
        db = client["github"]
        coll = db.category
        # query = {"name": {"$regex": "^Databases"}}
        docs = coll.find()
        for doc in docs:
            for link in doc["link"]:
                yield Request(link, meta={'category': doc["name"]}, callback=self.parse)

    def parse(self, response):
        # print(response.body)
        print(response.url)
        # 获取github仓库列表
        repositories = response.xpath(
            "//*/article/*/li/a[starts-with(@href,'https://github.com')]/..")
        for repository in repositories:
            # 生成item
            # print(repository.extract())
            print("爬取{}".format(response.meta["category"]))
            repository_item = repository_list_item()
            # print(repository.xpath("a/text()").extract())
            # print(repository.xpath("a/@href").extract())
            # print(repository.xpath("text()").extract(
            # )[0] if len(repository.xpath("text()").extract()) > 0 else None)

            repository_item["category"] = response.meta["category"]
            repository_item["name"] = repository.xpath("a/text()").extract()[0]
            repository_item["link"] = repository.xpath("a/@href").extract()[0]
            repository_item["describe"] = (
                repository.xpath("text()").extract()[0]
                if len(repository.xpath("text()").extract()) > 0
                else None
            )
            yield repository_item
