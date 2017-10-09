# -*- coding: utf-8 -*-
import scrapy
from rt.items import *

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ['https://www.rottentomatoes.com/m/blade_runner_2049']

    def parse(self, response):
        pass
