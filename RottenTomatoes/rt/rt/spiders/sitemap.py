# -*- coding: utf-8 -*-
import scrapy


class SitemapSpider(scrapy.Spider):
    name = 'sitemap'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ['http://rottentomatoes.com/sitemap.xml']

    def parse(self, response):
        print("Hello")
        pass
