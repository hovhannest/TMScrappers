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
    info
    Rating
    Genre
    DirectedBy
    WrittenBy
    InTheaters
    BoxOffice
    Runtime
    Studio

    webSyte

    posterImage

    videos
    photos


class Person(scrapy.Item):
    name
    url
