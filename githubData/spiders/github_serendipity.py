# -*- coding: utf-8 -*-
import scrapy
import csv
from githubData.items import crawlItem


class GithubSerendipitySpider(scrapy.Spider):
    name = 'github_serendipity'
    allowed_domains = ['scrapy-chs.readthedocs.io']
    start_urls = ['https://github-serendipity.github.io/repo/frenck___awesome-home-assistant']

    # father title is here but now ignore , use map to store

    def parse(self, response):
        # 得到所有h3,或者2
        cate = response.xpath('//h2/@id')
        with open('27home-assistant.csv', mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for sel in cate:
                # 子标题
                subcate = sel.extract()
                # 得到对应id的临近ul 和第一个子li
                subli = response.css('#' + subcate + '+ul li')
                for subli_single in subli:
                    # 得到所有a
                    subli_a = subli_single.css(' a')
                    # 得到所有链接
                    subli_link = subli_a.xpath("@href").extract()
                    # print(subli_link)
                    # 项目的详细介绍
                    subli_test = subli_single.xpath("text()").extract()
                    # print(subli_link)
                    # print(subli_test)
                    data = []
                    if len(subli_link)>0:
                        data.append("home-assistant")
                        data.append(str(subcate))
                        data.append(str(subli_link[0]))
                        if len(subli_test) == 0:
                            data.append("")
                        else:
                            data.append(str(subli_test[0]))
                        employee_writer.writerow(data)
                        # print("----" + str(len(subli_single)) + "-----------------")

         # yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):#后续工作，直接在爬取时对项目的代码readme进行分析
        detail = response.xpath('//div[@class="article-wrap"]')
        item = crawlItem()
        item['title'] = detail.xpath('h1/text()')[0].extract()
        item['link'] = response.url
        item['posttime'] = detail.xpath(
            'div[@class="article-author"]/span[@class="article-time"]/text()')[0].extract()
        print(item['title'], item['link'], item['posttime'])
        yield item
