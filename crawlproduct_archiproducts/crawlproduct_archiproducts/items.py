# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlproductArchiproductsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    vendor = scrapy.Field()
    type1 = scrapy.Field()
    type2 = scrapy.Field()
    type3 = scrapy.Field()
    published = scrapy.Field()
    url=scrapy.Field()
    dimension=scrapy.Field()
    pass
