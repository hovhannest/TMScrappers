# -*- coding: utf-8 -*-
import scrapy
from rt.items import *
import re

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ['https://www.rottentomatoes.com/m/blade_runner_2049']

    def parse(self, response):
        movie = MovieItem()
        movie["sourceURL"] = response.url
        movie["name"] = re.findall(r'\S+.*', response.css('h1[id=movie-title]::text').extract_first())[0]
        movie["year"] = re.findall('[(](\d\d\d\d)[)]', response.css('h1[id=movie-title] span::text').extract_first())[0]
        movie["info"] = re.findall(r'\S+.*', response.css("div[id=movieSynopsis]::text").extract_first())[0]

        intoList = response.css('ul.content-meta')[0]
        for li in intoList.css('li'):
            liName = li.css('div.meta-label::text').extract_first()
            if('Rating' in liName):
                movie['Rating'] = li.css('div.meta-value::text').extract_first()
            elif 'Genre' in liName:
                print(li.css('div.meta-value a::text').extract())
