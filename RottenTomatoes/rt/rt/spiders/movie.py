# -*- coding: utf-8 -*-
import scrapy
from rt.items import *
import re

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['rottentomatoes.com']
    # start_urls = ['https://www.rottentomatoes.com/m/blade_runner_2049']
    start_urls = ['https://www.rottentomatoes.com/tv/good_place/s01/e01']

    def parse(self, response):
        # init
        movie = MovieItem()
        movie['name'] = ''
        movie['sourceURL'] = ''
        movie['year'] = ''
        movie['info'] = ''
        movie['Rating'] = ''
        movie['Genre'] = ''
        movie['DirectedBy_url'] = ''
        movie['DirectedBy'] = ''
        movie['WrittenBy_url'] = ''
        movie['WrittenBy'] = ''
        movie['InTheaters'] = ''
        movie['BoxOffice'] = ''
        movie['Runtime'] = ''
        movie['Studio'] = ''
        movie['webSyte'] = ''
        movie['posterImage'] = ''
        movie['cast_url'] = ''
        movie['cast'] = ''
        movie['cast_role'] = ''
        movie['RTMainScore'] = ''
        movie['RTTopScore'] = ''
        movie['RTCAvRating'] = ''
        movie['RTFresh'] = ''
        movie['RTRotten'] = ''
        movie['RTAAvRating'] = ''
        movie['RTUserRatings'] = ''

        movie["sourceURL"] = response.url

        if '/m/' in movie["sourceURL"]:
            movie['TVShow'] = 0
        else:
            movie['TVShow'] = 1

        try:
            movie['Episode'] = int(re.findall(r'http\S*\/\/\S*\/[e][0]*(\d*)[\/]*', movie['sourceURL'])[0])
            if movie['Episode'] is None:
                movie['Episode'] = -1
        except:
            movie['Episode'] = -1

        try:
            movie['Season'] = int(re.findall(r'http\S*\/\/\S*\/[s][0]*(\d*)[\/]*', movie['sourceURL'])[0])
            if movie['Season'] is None:
                movie['Season'] = -1
        except:
            movie['Season'] = -1

        try:
            movie["name"] = re.findall(r'\S+.*', response.css('h1[id=movie-title]::text').extract_first())[0]
        except:
            try:
                movie["name"] = re.findall(r'\S+.*', response.css('div.seriesHeader h1::text').extract_first())[0]
            except:
                try:
                    movie["name"] = re.findall(r'\S+.*', response.css('div.super_series_header h1::text').extract_first())[0]
                except:
                    try:
                        movie["name"] = re.findall(r'\S+.*', response.css('h1.movie-title::text').extract_first())[0]
                    except:
                        movie["name"] = ""
        try:
            movie["year"] = re.findall('[(](\d\d\d\d)[)]', response.css('h1[id=movie-title] span::text').extract_first())[0]
        except:
            movie["year"] = ""
        movie["info"] = re.findall(r'\S+.*', response.css("div[id=movieSynopsis]::text").extract_first())[0]

        try:
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
                        # person = Person()
                        # person['name'] = name
                        # person['url'] = url
                        # yield person
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
                        # person = Person()
                        # person['name'] = name
                        # person['url'] = url
                        # yield person
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
        except:
            pass
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
            # person = Person()
            # person['name'] = name
            # person['url'] = url
            # yield person
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

        allReviesDiv = response.css('div#all-critics-numbers')
        topReviesDiv = response.css('div#top-critics-numbers')

        currDiv = allReviesDiv

        rateSpan = currDiv.css('span.meter-value')

        try:
            movie["RTMainScore"] = int(rateSpan.css('span::text').extract_first())
        except:
            movie["RTMainScore"] = 0.0;

        scoresDiv = currDiv.css('div#scoreStats')
        scds = scoresDiv.css('div.superPageFontColor')
        if len(scds) >= 4:
            RTCAvRating = scoresDiv.css('div.superPageFontColor').extract_first()
            movie["RTCAvRating"] = float(re.search(r'.*(\d[.]\d)', RTCAvRating).group(0))
            try:
                movie["RTFresh"] = int(scds[2].css('span::text').extract()[1])
            except:
                movie["RTFresh"] = 0
            try:
                movie["RTRotten"] = int(scds[3].css('span::text').extract()[1])
            except:
                movie["RTRotten"] = 0

        currDiv = topReviesDiv

        rateSpan = currDiv.css('span.meter-value')

        try:
            movie["RTTopScore"] = int(rateSpan.css('span::text').extract_first())
        except:
            movie["RTTopScore"] = 0

        currDiv = response.css('div.audience-score')

        try:
            movie["RTAAvRating"] = float(currDiv.css('span::text').extract_first().replace('%', ''))
        except:
            movie["RTAAvRating"] = 0.0

        currDiv = response.css('audience-info')
        try:
            movie["RTUserRatings"] = int(currDiv.css('div::text').extract()[1].replace(',', ''))
        except:
            movie["RTUserRatings"] = 0



        yield movie