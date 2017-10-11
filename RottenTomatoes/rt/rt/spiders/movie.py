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
                    if ll != "" or nl != "":
                        ll += ","
                        nl += ","
                    name = a.css("::text").extract_first()
                    url = a.css("::attr(href)").extract_first()
                    person = Person()
                    person['name'] = name
                    person['url'] = url
                    yield person
                    ll += url
                    nl += name
                movie["DirectedBy_url"] = ll
                movie["DirectedBy"] = nl
            elif 'Written' in liName:
                ll = ""
                nl = ""
                for a in li.css('div.meta-value a'):
                    if ll != "" or nl != "":
                        ll += ","
                        nl += ","
                    name = a.css("::text").extract_first()
                    url = a.css("::attr(href)").extract_first()
                    person = Person()
                    person['name'] = name
                    person['url'] = url
                    yield person
                    ll += url
                    nl += name
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
                    if ll != "" or nl != "":
                        ll += ","
                        nl += ","
                    name = a.css("::text").extract_first()
                    url = a.css("::attr(href)").extract_first()
                    # person = Person()
                    # person['name'] = name
                    # person['url'] = url
                    # yield person
                    ll += url
                    nl += name
                movie["webSyte"] = ll
                movie["Studio"] = nl
        movie["posterImage"] = response.css('img.posterImage::attr(src)').extract_first()
        ll = ""
        nl = ""
        cl = ""
        for div in response.css('div.castSection  div div.media-body'):
            if ll != "" or nl != "":
                ll += ","
                nl += ","
                cl += ","
            name = re.findall(r'\S+.*', div.css('a span::text').extract_first())[0]
            url = div.css('a::attr(href)').extract_first()
            person = Person()
            person['name'] = name
            person['url'] = url
            yield person
            ll += url
            nl += name
            ccl = ""
            for s in div.css('span.characters'):
                if ccl != "":
                    ccl += "|"
                ccl += s.css('::text').extract_first()
            cl += ccl
        movie["cast_url"] = ll
        movie["cast"] = nl
        movie["cast_role"] = cl #div.css('span.characters::text').extract_first()
        yield movie