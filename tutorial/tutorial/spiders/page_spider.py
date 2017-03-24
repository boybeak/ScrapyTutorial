# -*- coding: utf-8 -*-
import scrapy
import logging


class PageSpider(scrapy.Spider):

    name = "page_spider"

    start_urls = [
        'http://www.6vhao.net/dy2/2017-02-11/31273.html'
    ]

    def parse(self, response):
        content_info = response.css('div.contentinfo')
        symbol1 = u'【'
        symbol2 = u'】'

        rex = r'%s(.*)%s' % (symbol1, symbol2)
        logging.log(logging.INFO, "rex=" + rex)
        title = content_info.css('h1 a::text').re_first(rex)
        logging.log(logging.INFO, title)
