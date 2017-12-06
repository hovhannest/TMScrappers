# -*- coding: utf-8 -*-
import scrapy
from rt.items import *
import re
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.spiders import Rule

class SitemapSpider(scrapy.Spider):
    passed = False

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
                yield self.parseNexUrl(url)

    def parseNexUrl(self, burl):
        url = burl
        if "http" not in url:
            url = "https://www.rottentomatoes.com" + burl

        # if not self.passed and ("https://www.rottentomatoes.com/m/bells_of_coronado" in url):
        #    self.passed = True
        #
        # if not self.passed:
        #    return ;
        # if not self.passed and ("https://www.rottentomatoes.com/tv/real_husbands_of_hollywood" in url):
        #    self.passed = True
        #
        # if not self.passed:
        #    return ;

        # if "/m/" in url and url.count('/') < 5:
        #    return scrapy.Request(url, callback=self.parse_movies)
        if "/tv/" in url and url.count('/') == 5:
            return scrapy.Request(url, callback=self.parse_movies)
        #     yield scrapy.Request(url, callback=self.parse_tv)
        #elif "/critic/" in url:
        #    yield scrapy.Request(url, callback=self.parse_critic)
        # elif "/celebrity/" in url:
        #    print(url)
        #     return scrapy.Request(url, callback=self.parse_celebrity)
        # else:
        #     yield scrapy.Request(url, callback=self.parse_else)

    def parse_movies(self, response):
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
        movie['Episode'] = -1
        movie['Season'] = -1

        movie["sourceURL"] = response.url
        if '/m/' in movie["sourceURL"]:
            movie['TVShow'] = 0
        else:
            movie['TVShow'] = 1

        try:
            movie['Episode'] = int(re.findall(r'http\S*\/\/\S*\/[e][0]*(\d*)[\/]*', movie['sourceURL'])[0])
        except:
            movie['Episode'] = -1

        try:
            movie['Season'] = int(re.findall(r'http\S*\/\/\S*\/[s][0]*(\d*)[\/]*', movie['sourceURL'])[0])
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
                        person = PersonMovie()
                        person['Movie_URL'] = response.url
                        person['Person_URL'] = url
                        person['Character'] = ""
                        person['ProfessionID'] = 2
                        yield person
                        person = PersonUrl()
                        person['url'] = url
                        yield person
                        ll += url
                        nl += name
                        yield self.parseNexUrl(url)
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
                        person = PersonMovie()
                        person['Movie_URL'] = response.url
                        person['Person_URL'] = url
                        person['Character'] = ""
                        person['ProfessionID'] = 4
                        yield person
                        person = PersonUrl()
                        person['url'] = url
                        yield person
                        ll += url
                        nl += name
                        yield self.parseNexUrl(url)
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
            person = PersonMovie()
            person['Movie_URL'] = response.url
            person['Person_URL'] = url
            person['Character'] = ""
            person['ProfessionID'] = 1
            yield person
            person = PersonUrl()
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
            yield self.parseNexUrl(url)
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
            movie["RTMainScore"] = 0.0

        scoresDiv = currDiv.css('div#scoreStats')
        scds = scoresDiv.css('div.superPageFontColor')
        if len(scds) >= 4:
            RTCAvRating = scoresDiv.css('div.superPageFontColor').extract_first()
            try:
                movie["RTCAvRating"] = float(re.search(r'.*(\d[.]\d)', RTCAvRating).group(0))
            except:
                movie["RTCAvRating"] = 0.0
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
        # yield EndItem()

    def parse_tv(self, response):
        # print("parse_tv")
        pass

    def parse_critic(self, response):
        # print("parse_critic")
        pass

    def parse_celebrity(self, response):
        person = Person()

        person['Screenwriter'] = 0
        person['Director'] = 0
        person['Actor'] = 0
        person['Producer'] = 0
        person['ExecutiveProducer'] = 0

        person["url"] = re.findall(r'\/celebrity\S*', response.url)[0]
        person["name"] = response.css("div.celeb_name h1::text").extract_first()

        person["birthday"] = response.css("div.celeb_bio_row time::attr('datetime')").extract_first()

        try:
            person["birthplace"] = \
            re.findall(r'\S+.*', response.css("div.celeb_bio div.celeb_bio_row ::text").extract()[-1])[0]
        except:
            person["birthplace"] = ""

        try:
            person['bio'] = response.css("div.celeb_bio div.celeb_summary_bio ::text").extract_first()
        except:
            person['bio'] = ""

        person['photo_url'] = \
        re.findall(r'(http\S*)\)', response.css('div.celebHeroImage::attr("style")').extract_first())[0]

        mlist = response.css("table#filmographyTbl")

        for tr in mlist.css('tr'):
            try:
                td = tr.css('td')[2]
                for li in td.css('li::text').extract():
                    if "Screenwriter" in li:
                        person["Screenwriter"] = 1
                    elif "Director" in li:
                        person["Director"] = 1
                    elif "Executive Producer" in li:
                        person["ExecutiveProducer"] = 1
                    elif "Producer" in li:
                        person["Producer"] = 1
                    else:
                        person["Actor"] = 1
                for li in td.css('em::text').extract():
                    if "Screenwriter" in li:
                        person["Screenwriter"] = 1
                    elif "Director" in li:
                        person["Director"] = 1
                    elif "Executive Producer" in li:
                        person["ExecutiveProducer"] = 1
                    elif "Producer" in li:
                        person["Producer"] = 1
                    else:
                        person["Actor"] = 1
            except:
                pass

        if person['photo_url'] is None:
            person['photo_url'] = ""
        if person['bio'] is None:
            person['bio'] = ""
        if person['birthplace'] is None:
            person['birthplace'] = ""
        if person['birthday'] is None:
            person['birthday'] = ""
        yield person


    def parse_else(self, response):
        print("parse_else")

