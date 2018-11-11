# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from githubData.items import repository_detail_item
from scrapy import Request, log
from scrapy.selector import Selector
import pprint
import pymongo
import json
import time
import re


class repository_detail_spider(scrapy.Spider):
    name = 'repository_detail'

    def start_requests(self):
        client = pymongo.MongoClient(
            host="127.0.0.1", port=29197)

        a = 0
        client["github"].authenticate("github", "git332", "github")
        db = client["github"]
        pattern = re.compile(r'^https://github.com/(.*)/(.*)$')
        coll = db.repository_list
        query = {"link": {"$regex": "^https://github.com/"}}
        docs = coll.find(query)
        for doc in docs:
            a = a + 1

            print(doc['link'])
            user = doc['link'].split('/')[3]
            print('user: {}'.format(user))
            if(len(doc['link'].split('/')) > 4):
                project = doc['link'].split('/')[4].split('#')[0]
                request_link = "https://api.github.com/repos/{}/{}".format(
                    user, project)
                yield Request(request_link, meta={'link_raw': doc["link"], 'user': user, 'project': project}, callback=self.parse)
            else:
                continue

            # print('project: {}'.format(project))

        # print("a: {}".format(a))

    def parse(self, response):
        detail_json = response.xpath("//pre/text()").extract()[0]
        repository_detail = repository_detail_item()
        repository_detail["json_str"] = detail_json
        # print(repository_detail)
        yield repository_detail
        
