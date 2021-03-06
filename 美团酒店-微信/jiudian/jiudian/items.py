# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JiudianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    addr = scrapy.Field()
    lowestPrice = scrapy.Field()
    quyu = scrapy.Field()
    phone = scrapy.Field()
    poiid = scrapy.Field()
    cityName = scrapy.Field()
