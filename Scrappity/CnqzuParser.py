import scrapy
import os

class CnqzuParser(scrapy.Spider):
    # Name of the spider (class variable)
    name = 'CnqzuSpider'

    def __init__(self,
                 domain='',
                 *args,
                 **kwargs):

        # Call constructor of parent class
        super(CnqzuParser, self).__init__(*args, **kwargs)

        self.url = kwargs.get("url")
        self.path = kwargs.get("path")
        self.genre = kwargs.get("genre")
        self.limit = kwargs.get("limit")
        self.verbose = kwargs.get("verbose")

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self,
              response):

        # A way to get all the links to the next page
        # TODO: Remove below line and implement appropriate
        # logic
        #print (response.xpath('//li/a/@href').extract())
        pass
