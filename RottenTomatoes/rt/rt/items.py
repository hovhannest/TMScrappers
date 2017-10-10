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
    DirectedBy = scrapy.Field()
    WrittenBy = scrapy.Field()
    InTheaters = scrapy.Field()
    BoxOffice = scrapy.Field()
    Runtime = scrapy.Field()
    Studio = scrapy.Field()

    webSyte = scrapy.Field()

    posterImage = scrapy.Field()

    videos = scrapy.Field()
    photos = scrapy.Field()


class Person(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
