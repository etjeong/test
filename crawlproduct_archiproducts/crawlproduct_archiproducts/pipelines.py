# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import unicode_literals
import datetime
import logging
import scrapy
import pymysql.cursors

class CrawlproductArchiproductsPipeline(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='scrapy_db', charset='utf8mb4')
            self.cursor = self.conn.cursor()
        except pymysql.Error as e:
            print("Error %d: %s"%(e.args[0], e.args[1]))

    def process_item(self, item, spider):
        try:
            sql = "insert into archiproducts_product(title, description, vendor, type1, type2, type3, url, dimension) " \
                  "values (%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update title=%s,description=%s,vendor=%s,type1=%s,type2=%s,type3=%s,url=%s,dimension=%s"
            self.cursor.execute(sql, (
            item['title'], item['description'], item['vendor'], item['type1'], item['type2'], item['type3'],item['url'],item['dimension'],
            item['title'], item['description'], item['vendor'], item['type1'], item['type2'], item['type3'],item['url'],item['dimension']))
            self.conn.commit()
        except pymysql.Error as e:
            print("Error %d: %s"%(e.args[0], e.args[1]))
            return item

