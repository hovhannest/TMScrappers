import scrapy
from rt.items import *
import re

class PersonSpider(scrapy.Spider):
    name = 'person'
    allowed_domains = ['rottentomatoes.com']
    # start_urls = ['https://www.rottentomatoes.com/m/blade_runner_2049']
    start_urls = ['https://www.rottentomatoes.com/celebrity/ben_affleck']

    def parse(self, response):
        # init
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
            person["birthplace"] = re.findall(r'\S+.*', response.css("div.celeb_bio div.celeb_bio_row ::text").extract()[-1])[0]
        except:
            person["birthplace"] = ""

        try:
            person['bio'] = response.css("div.celeb_bio div.celeb_summary_bio ::text").extract_first()
        except:
            person['bio'] = ""

        person['photo_url'] = re.findall(r'(http\S*)\)', response.css('div.celebHeroImage::attr("style")').extract_first())[0]

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