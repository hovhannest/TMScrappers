# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItem(scrapy.Item):
    sourceURL = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    info = scrapy.Field()
    Rating = scrapy.Field()
    Genre = scrapy.Field()
    DirectedBy_url = scrapy.Field()
    DirectedBy = scrapy.Field()
    WrittenBy_url = scrapy.Field()
    WrittenBy = scrapy.Field()
    InTheaters = scrapy.Field()
    BoxOffice = scrapy.Field()
    Runtime = scrapy.Field()
    Studio = scrapy.Field()

    webSyte = scrapy.Field()

    posterImage = scrapy.Field()

    cast_url = scrapy.Field()
    cast = scrapy.Field()
    cast_role = scrapy.Field()

    RTMainScore = scrapy.Field()
    RTTopScore = scrapy.Field()
    RTCAvRating = scrapy.Field()
    RTFresh = scrapy.Field()
    RTRotten = scrapy.Field()
    RTAAvRating = scrapy.Field()
    RTUserRatings = scrapy.Field()
    Season = scrapy.Field()
    Episode = scrapy.Field()
    TVShow = scrapy.Field()


class Person(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    birthday = scrapy.Field()
    birthplace = scrapy.Field()
    bio = scrapy.Field()
    photo_url = scrapy.Field()
    Screenwriter = scrapy.Field()
    Director = scrapy.Field()
    Actor = scrapy.Field()
    Producer = scrapy.Field()
    ExecutiveProducer = scrapy.Field()


class PersonUrl(scrapy.Item):
    url = scrapy.Field()

class PersonMovie(scrapy.Item):
    Person_URL = scrapy.Field()
    Movie_URL = scrapy.Field()
    Character = scrapy.Field()
    ProfessionID = scrapy.Field()

class EndItem(scrapy.Item):
    tvar = scrapy.Field()