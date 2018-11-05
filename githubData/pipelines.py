# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import project_category_item
import pymongo
import json


class GithubdataPipeline(object):
    def process_item(self, item, spider):
        return item


class github_awesome_pipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host="192.168.0.165", port=27017)

        self.db = self.client["github"]

    def process_item(self, item, spider):
        if isinstance(item, project_category_item):
            coll = self.db.category
            id = coll.insert_one({
                "name": item["name"],
                "link": item["link"]
            }).inserted_id
            print(item.item2dic())
            print(id)
