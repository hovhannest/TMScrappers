import csv
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import inspect
from rt.items import *
import pymssql

class MsSqlPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.conn = pymssql.connect(host='tapmovie.cncxzttlagub.us-east-2.rds.amazonaws.com',
                                    port='1433',
                                    user='master',
                                    password='CIS<322>',
                                    database='tapmovie')
        self.cursor = self.conn.cursor()

    def spider_closed(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            try:
                # self.cursor.execute("INSERT INTO [dbo].[RTMovie] ([name] ,[Rating] ,[year] ,[Runtime] ,[InTheaters] ,[WrittenBy] ,[WrittenBy_url] ,[Genre] ,[DirectedBy_url] ,[cast_url] ,[posterImage] ,[info] ,[BoxOffice] ,[DirectedBy] ,[cast_role] ,[Studio] ,[cast] ,[webSyte] ,[sourceURL] ,[TOMATOMETER] ,[AverageRating] ,[ReviewsCounted] ,[Fresh] ,[Rotten] ,[AUDIENCE_SCORE] ,[UserRatings])    VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s,%s ,%s ,%s ,%s,%s,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)",
                #                     (item['name'], item['Rating'], item['year'], item['year'], item['Runtime'], item['InTheaters'], item['WrittenBy'], item['WrittenBy_url'], item['Genre'], item['DirectedBy_url'], item['cast_url'], item['posterImage'], item['info'], item['BoxOffice'], item['DirectedBy'], item['cast_role'], item['Studio'], item['cast'], item['webSyte'], item['sourceURL'], item['TOMATOMETER'], item['AverageRating'], item['ReviewsCounted'], item['Fresh'], item['Rotten'], item['AUDIENCE_SCORE'], item['UserRatings']))

                if item["Season"] >= 0:
                    if item["Episode"] >= 0:
                        self.cursor.execute("INSERT INTO [dbo].[RTMovie] ([name], [sourceURL], [year], [info], [Rating], \
[Genre], [DirectedBy_url], [DirectedBy], [WrittenBy_url], \
[WrittenBy], [InTheaters], [BoxOffice], [Runtime], [Studio], \
[webSyte], [posterImage], [cast_url], [cast], [cast_role], \
[RTMainScore], [RTTopScore], [RTCAvRating], [RTFresh], [RTRotten], \
[RTAAvRating], [RTUserRatings], [TVShow], [Season], [Episode]) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (item['name'], item['sourceURL'], item['year'], item['info'], item['Rating'],
                                     item['Genre'], item['DirectedBy_url'], item['DirectedBy'], item['WrittenBy_url'],
                                     item['WrittenBy'], item['InTheaters'], item['BoxOffice'], item['Runtime'], item['Studio'],
                                     item['webSyte'], item['posterImage'], item['cast_url'], item['cast'], item['cast_role'],
                                     item['RTMainScore'], item['RTTopScore'], item['RTCAvRating'], item['RTFresh'], item['RTRotten'],
                                     item['RTAAvRating'], item['RTUserRatings'], item['TVShow'], item['Season'], item['Episode']))
                    else:
                        self.cursor.execute("INSERT INTO [dbo].[RTMovie] ([name], [sourceURL], [year], [info], [Rating], \
[Genre], [DirectedBy_url], [DirectedBy], [WrittenBy_url], \
[WrittenBy], [InTheaters], [BoxOffice], [Runtime], [Studio], \
[webSyte], [posterImage], [cast_url], [cast], [cast_role], \
[RTMainScore], [RTTopScore], [RTCAvRating], [RTFresh], [RTRotten], \
[RTAAvRating], [RTUserRatings], [TVShow], [Season]) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (item['name'], item['sourceURL'], item['year'], item['info'], item['Rating'],
                                     item['Genre'], item['DirectedBy_url'], item['DirectedBy'], item['WrittenBy_url'],
                                     item['WrittenBy'], item['InTheaters'], item['BoxOffice'], item['Runtime'], item['Studio'],
                                     item['webSyte'], item['posterImage'], item['cast_url'], item['cast'], item['cast_role'],
                                     item['RTMainScore'], item['RTTopScore'], item['RTCAvRating'], item['RTFresh'], item['RTRotten'],
                                     item['RTAAvRating'], item['RTUserRatings'], item['TVShow'], item['Season']))
                else:
                    self.cursor.execute("INSERT INTO [dbo].[RTMovie] ([name], [sourceURL], [year], [info], [Rating], \
[Genre], [DirectedBy_url], [DirectedBy], [WrittenBy_url], \
[WrittenBy], [InTheaters], [BoxOffice], [Runtime], [Studio], \
[webSyte], [posterImage], [cast_url], [cast], [cast_role], \
[RTMainScore], [RTTopScore], [RTCAvRating], [RTFresh], [RTRotten], \
[RTAAvRating], [RTUserRatings], [TVShow]) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (item['name'], item['sourceURL'], item['year'], item['info'], item['Rating'],
                                     item['Genre'], item['DirectedBy_url'], item['DirectedBy'], item['WrittenBy_url'],
                                     item['WrittenBy'], item['InTheaters'], item['BoxOffice'], item['Runtime'], item['Studio'],
                                     item['webSyte'], item['posterImage'], item['cast_url'], item['cast'], item['cast_role'],
                                     item['RTMainScore'], item['RTTopScore'], item['RTCAvRating'], item['RTFresh'], item['RTRotten'],
                                     item['RTAAvRating'], item['RTUserRatings'], item['TVShow']))

                self.conn.commit()
                print("MSSQL: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except pymssql.Error as e:
                print("ERROR: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
        elif isinstance(item, Person):
            # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            try:
                self.cursor.execute("INSERT INTO [dbo].[RTPerson] ([name], [url], [birthday], [birthplace], [bio], \
                                    [photo_url], [Screenwriter], [Director], [Actor], [Producer], [Executive Producer]) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",
                                    (item['name'], item['url'], item['birthday'], item['birthplace'], item['bio'],
                                     item['photo_url'], item['Screenwriter'], item['Director'], item['Actor'], item['Producer'], item['ExecutiveProducer']))

                # self.conn.commit()
                print("MSSQL: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except pymssql.Error as e:
                print("ERROR: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
        elif isinstance(item, PersonMovie):
            try:
                self.cursor.execute("INSERT INTO [dbo].[RTMoviePerson] ( [Movie_URL],[Person_URL],[Character],[ProfessionID]) \
                                    VALUES (%s, %s, %s, %s)",
                                    (item['Movie_URL'], item['Person_URL'], item['Character'], item['ProfessionID']))

                # self.conn.commit()
                print("MSSQL: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except pymssql.Error as e:
                print("ERROR: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
        elif isinstance(item, PersonUrl):
            try:
                self.cursor.execute("INSERT INTO [dbo].[RTPerson] ([url]) \
                                    VALUES (%s )",
                                    (item['url']))

                # self.conn.commit()
                print("MSSQL: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except pymssql.Error as e:
                print("ERROR: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
        elif isinstance(item, EndItem):
            try:
                self.conn.commit()
                print("MSSQL: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except pymssql.Error as e:
                print("ERROR: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
        else:
            pass;
        return item
