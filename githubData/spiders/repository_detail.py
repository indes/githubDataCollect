# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from githubData.items import repository_detail_item
from scrapy import Request
import logging
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
        # yield Request("https://github.com/golang/go", meta={'link_raw': "https://github.com/golang/go", 'user': "golang", 'project': "go"}, callback=self.parse)
        for doc in docs:
            # continue
            a = a + 1
            print("[{}] {}".format(a, doc['link']))
            user = doc['link'].split('/')[3]
            if(len(doc['link'].split('/')) > 4):
                project = doc['link'].split('/')[4].split('#')[0]
                request_link = "https://github.com/{}/{}".format(
                    user, project)
                logging.info("crawl {}".format(request_link))
                yield Request(
                    request_link, 
                    meta={'link_raw': doc["link"], 'user': user, 'project': project}, 
                    callback=self.parse)
            else:
                continue

            # print('project: {}'.format(project))

        # print("a: {}".format(a))

    def parse(self, response):
        logging.info("parsing {}".format(response.url))
        tags = []
        tags_raw = response.xpath(
            "//*[contains(@class,'list-topics-container')]/a/text()").extract()
        if(tags_raw):
            for tag_raw in tags_raw:
                tags.append(tag_raw.split(" ")[8].split("\n")[0])

        logging.info(
            "project: {}/{}, tags: {}".format(response.meta["user"], response.meta["project"], tags))
        readme_link = "https://raw.githubusercontent.com/{}/{}/master/README.md".format(
            response.meta["user"], response.meta["project"])
        yield Request(readme_link, meta={"link_raw": response.meta["link_raw"], "user": response.meta["user"], "project": response.meta["project"], "tags": tags, "page": "README.md"}, callback=self.readme_parse)

    def readme_parse(self, response):
        # pprint.pprint(response.xpath("//pre/text()").extract()[0])
        logging.info("parsing {}".format(response.url))

        if(response.meta["page"] == "README.md"):
            try:
                readme = response.xpath("//pre/text()").extract()[0]
            except:
                readme_link = "https://raw.githubusercontent.com/{}/{}/master/readme.md".format(
                    response.meta["user"], response.meta["project"])
                yield Request(
                    readme_link,
                    meta={
                        "link_raw": response.meta["link_raw"],
                        "user": response.meta["user"],
                        "project": response.meta["project"],
                        "tags": response.meta["tags"],
                        "page": "readme.md"
                    },
                    callback=self.readme_parse
                )

        elif(response.meta["page"] == "readme.md"):
            try:
                readme = response.xpath("//pre/text()").extract()[0]
            except:
                readme = ""
        
        

        item = repository_detail_item()
        item["tags"] = response.meta["tags"]
        item["readme"] = readme
        item["project"] = "{}/{}".format(response.meta["user"],
                                         response.meta["project"])

        yield item
