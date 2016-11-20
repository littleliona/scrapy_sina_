# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from imp import reload
import json
import codecs
import sys
reload(sys)
#sys.setdefaultencoding( "utf-8" )
class SinaPipeline(object):
    def process_item(self, item, spider):
        link_url = item['link_url']
        file_name = link_url[7:-6].replace('/','_')
        file_name += ".txt"
        if(item['content']):
            fp = open(item['path']+'/'+file_name, 'w+')
            fp.write(item['content'])
            fp.close()
        return item
