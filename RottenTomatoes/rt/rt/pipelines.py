# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import inspect
from rt.items import *

class RtPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.filesList = ['%s_movies.csv', '%s_person.csv', '%s_items.csv']
        fl = []
        for filename in self.filesList:
            fl.append(open(filename % spider.name, 'wb'))
        self.files[spider] = fl

        self.exporterMovie = CsvItemExporter(fl[0])
        self.exporterMovie.start_exporting()

        self.exporterPerson = CsvItemExporter(fl[1])
        self.exporterPerson.start_exporting()

        self.exporter = CsvItemExporter(fl[-1])
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporterMovie.finish_exporting()
        self.exporterPerson.finish_exporting()
        self.exporter.finish_exporting()
        files = self.files.pop(spider)
        for file in files:
            file.close()

        for filename in self.filesList:
            # given I am using Windows i need to elimate the blank lines in the csv file
            print("Starting csv blank line cleaning")
            with open(filename % spider.name, 'r') as f:
                reader = csv.reader(f)
                original_list = list(reader)
                cleaned_list = list(filter(None, original_list))

            with open(filename % (spider.name + "_cleaned"), 'w', newline='') as output_file:
                wr = csv.writer(output_file, dialect='excel')
                for data in cleaned_list:
                    wr.writerow(data)

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            self.exporterMovie.export_item(item)
        elif isinstance(item, Person):
            self.exporterPerson.export_item(item)
        else:
            self.exporter.export_item(item)
        return item
