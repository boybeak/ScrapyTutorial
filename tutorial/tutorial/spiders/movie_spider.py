# -*- coding: utf-8 -*-
import scrapy
from tutorial.spiders.download_link import DownloadLink
from tutorial.spiders.movie import Movie
import logging


class MovieSpider(scrapy.Spider):

    name = "movie_spider"

    start_urls = [
        # "http://www.6vhao.net/dy1/",
        # "http://www.6vhao.net/dy2/",
        # "http://www.6vhao.net/dy3/",
        # "http://www.6vhao.net/dy5/",
        # "http://www.6vhao.net/dy6/",
        # "http://www.6vhao.net/zzp/",
        # "http://www.6vhao.net/jlp/",
        # "http://www.6vhao.net/jddy/",
        "http://www.6vhao.net/dy4/",
        # "http://www.6vhao.net/dlz/",
        # "http://www.6vhao.net/rj/",     # TimeOutException
        # "http://www.6vhao.net/mj/",
        # "http://www.6vhao.net/3d/",
        # "http://www.6vhao.net/zy/"
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1
    }

    # ,
    # 'ITEM_PIPELINES': {
    #     'tutorial.pipelines.TutorialPipeline'
    # }

    def parse(self, response):
        item = response.css('div.listBox ul li ')
        hrefs = item.css('div.listimg a::attr(href)').extract()
        # titles = item.css('div.listInfo h3 p::text').extract()
        # logging.log(logging.INFO, "parse " + len(hrefs))
        # 在分类下，对该页中的每个电影，进行跳入，再通过parse_movie爬取
        for href in hrefs:
            # logging.log(logging.INFO, "hrefs[" + index + "]=" + href)
            try:
                yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_movie)
            except Exception as e:
                continue

        # 指明该字符串编码
        next_page_str = u'下一页'
        rex = '//div[@class="pagebox"]/a[contains(text(), "%s")]/@href' % next_page_str
        next_page = response.xpath(rex).extract_first()
        # 如果发现了有下一页，则开始爬下一页，如果没有则说明该分类电影已经爬完了，跳到下个分类去爬
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_movie(self, response):
        content_info = response.css('div.contentinfo')
        movie = Movie()
        symbol1 = u'【'
        symbol2 = u'】'

        rex = r'%s(.*)%s' % (symbol1, symbol2)
        movie['title'] = content_info.css('h1 a::text').re_first(rex)

        # logging.log(logging.INFO, "parse_movie " + movie['title'])

        text = content_info.css('div#text')
        t_msg_font = text.css('div.t_msgfont')
        if len(t_msg_font) > 0:
            movie['cover'] = t_msg_font.css(' img::attr(src)').extract_first()
            movie['detail'] = self.parse_detail(t_msg_font.css('::text'))
        else:
            movie['cover'] = text.css(' p img::attr(src)').extract_first()
            movie['detail'] = self.parse_detail(text.css(' p::text'))
            thumbnails = text.css(' p img::attr(src)').extract()
            if movie['cover'] in thumbnails:
                thumbnails.remove(movie['cover'])
            movie['thumbnails'] = thumbnails
        download_links = text.css(' table tbody tr td a')
        download_links_array = []
        for link_item in download_links:
            download_link = DownloadLink()
            download_link['title'] = link_item.css('::text').extract_first()
            download_link['link'] = link_item.css('::attr(href)').extract_first();
            download_links_array.append(dict(download_link))
        movie['download_links'] = download_links_array
        return movie

    def parse_detail(self, selector):
        details = selector.extract()
        detail = ""
        for d in details:
            detail += d

        return detail

    # def parse_movie(self, response):
    #
    #     def extract_with_css_first(query):
    #         return response.css(query).extract_first().strip()
    #
    #     def extract_with_css_array(query):
    #         return response.css(query).extract()
    #
    #
    #     yield {
    #         'title': extract_with_css_first('div.contentinfo h1 a::text'),
    #         'cover': extract_with_css_first('div#text p img::attr(src)'),
    #         'detail': extract_with_css_array('div#text p::text'),
    #         'thumbnails': extract_with_css_array('div#text p img::attr(src)'),
    #         'source_links': extract_with_css_array('div#text table tbody tr td a::attr(href)')
    #     }