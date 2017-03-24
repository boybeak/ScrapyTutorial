# -*- coding: utf-8 -*-
import scrapy


class DownloadLink(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()