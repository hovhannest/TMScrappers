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
                gl = ""
                for genre in li.css('div.meta-value a::text').extract():
                    if gl != "":
                        gl += ","
                    gl += re.findall(r'\S+.*', genre)[0]
                movie["Genre"] = gl
            elif 'Directed' in liName:
                ll = ""
                nl = ""
                for a in li.css('div.meta-value a'):
                    if ll != "":
                        ll += ","
                    if nl != "":
                        nl += ","
                    ll += a.css("::attr(href)").extract_first()
                    nl += a.css("::text").extract_first()
                movie["DirectedBy_url"] = ll
                movie["DirectedBy"] = nl
            elif 'Written' in liName:
                ll = ""
                nl = ""
                for a in li.css('div.meta-value a'):
                    if ll != "":
                        ll += ","
                    if nl != "":
                        nl += ","
                    ll += a.css("::attr(href)").extract_first()
                    nl += a.css("::text").extract_first()
                movie["WrittenBy_url"] = ll
                movie["WrittenBy"] = nl
            elif 'In Theaters' in liName:
                movie["InTheaters"] = li.css('div.meta-value time::attr(datetime)').extract_first()
            elif 'Box Office' in liName:
                movie["BoxOffice"] = int(re.sub(r'\D+', '', li.css('div.meta-value::text').extract_first()))
            elif 'Runtime' in liName:
                movie["Runtime"] = li.css('div.meta-value time::attr(datetime)').extract_first()
            elif 'Studio' in liName:
                ll = ""
                nl = ""
                for a in li.css('div.meta-value a'):
                    if ll != "":
                        ll += ","
                    if nl != "":
                        nl += ","
                    ll += a.css("::attr(href)").extract_first()
                    nl += a.css("::text").extract_first()
                movie["webSyte"] = ll
                movie["Studio"] = nl
        movie["posterImage"] = response.css('img.posterImage::attr(src)').extract_first()

