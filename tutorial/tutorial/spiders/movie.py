# -*- coding: utf-8 -*-
import scrapy


class Movie(scrapy.Item):

    title = scrapy.Field()
    cover = scrapy.Field()
    detail = scrapy.Field()
    thumbnails = scrapy.Field()
    download_links = scrapy.Field()