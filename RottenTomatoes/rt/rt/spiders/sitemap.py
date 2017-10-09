# -*- coding: utf-8 -*-
import scrapy
from rt.items import *
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

class SitemapSpider(scrapy.Spider):
    name = 'sitemap'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ['http://www.rottentomatoes.com/sitemap.xml']

    def parse(self, response):
        if (response.url == self.start_urls[0]):
            urls = response.xpath("//*[name()='loc']/text()").extract()
            for url in urls:
                yield scrapy.Request(url)
        else:
            urls = response.xpath("//*[name()='loc']/text()").extract()
            # print(urls)
            for url in urls:
                if "/m/" in url:
                    yield scrapy.Request(url, callback=self.parse_movies)
                elif "/tv/" in url:
                    yield scrapy.Request(url, callback=self.parse_tv)
                elif "/critic/" in url:
                    yield scrapy.Request(url, callback=self.parse_critic)
                elif "/celebrity/" in url:
                    yield scrapy.Request(url, callback=self.parse_celebrity)
                else:
                    yield scrapy.Request(url, callback=self.parse_else)

    def parse_movies(self, responce):
        # print("parse_movies")
        pass

    def parse_tv(self, responce):
        # print("parse_tv")
        pass

    def parse_critic(self, responce):
        # print("parse_critic")
        pass

    def parse_celebrity(self, responce):
        # print("parse_celebrity")
        pass

    def parse_else(self, responce):
        print("parse_else")

