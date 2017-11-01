# -*-coding: utf-8 -*-
import sys, os
from imp import reload
reload(sys)
#sys.setdefaultencoding("utf-8")
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import TutorialItem
file_name ="/Users/aria/Desktop/data_t/" #存放文件分类的目录
ent_class = "sina15-channel-wrap"
auto_class = "sub-nav"
auto = "articleContent"
tech_class = "select"
tech_class_1 = "box"
class SinaSpider(Spider):
    name= "sina"
    allowed_domains= ["sina.com.cn"]
    start_urls= ["http://tech.sina.com.cn/"]#起始urls列表

    def parse(self, response):
        items= []
        sel= Selector(response)
        second_urls=sel.xpath('//div[@class=\"select\"]/ul/li/a/@href').extract()#大类的url
        second_titles=sel.xpath('//div[@class=\"select\"]/ul/li/a/text()').extract()
        #print(second_titles)
        #print(second_urls)
        for j in range(0,len(second_urls)):
            item = TutorialItem()
            item['second_url'] = second_urls[j]
            item['second_title'] = second_titles[j]
            item['path'] = file_name
            items.append(item)
        for item in items:
            yield Request(url=item['second_url'],meta={'item_1': item},callback=self.second_parse)

    def second_parse(self, response):
        sel= Selector(response)
        item_1= response.meta['item_1']
        items= []
        bigUrls= sel.xpath('//a/@href').extract()
        for i in range(0,len(bigUrls)):
            #if_belong = bigUrls[i]
            #if(if_belong):
            item = TutorialItem()
            item['second_url'] =item_1['second_url']
            item['second_title'] =item_1['second_title']
            item['path'] = item_1['path']
            item['link_url'] = bigUrls[i]
            items.append(item)
        for item in items:
            yield Request(url=response.urljoin(item['link_url']), meta={'item_2':item},callback=self.detail_parse)
                                                                        #对于返回的小类的url，再进行递归请求
    def detail_parse(self, response):
        sel= Selector(response)
        item= response.meta['item_2']
        content= ""
        head=sel.xpath('//h1[@id=\"artibodyTitle\"]/text()').extract()
        content_list=sel.xpath('//div[@id=\"artibody\"]/p/text()').extract()
        for content_one in content_list:
            content += content_one
        item['head']= head
        item['content']= content
        yield item




