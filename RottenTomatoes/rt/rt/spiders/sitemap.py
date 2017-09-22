# -*- coding: utf-8 -*-
import scrapy


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
            print("Hello")
