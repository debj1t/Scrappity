import scrapy
from twisted.internet import reactor
from logger import ScrappityLogger as log
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

        self.downloaded_count = 0
        self.pending_downloads = []
        self.urls_to_be_processed = [self.url]
        reactor.suggestThreadPoolSize(1)

    def start_requests(self):
        # Our journey begins from here
        if self.urls_to_be_processed:
            url = self.urls_to_be_processed.pop(0)
            yield scrapy.Request(url=url, callback=self.parse)
        else :
            log.debug('All URLs are processed')

    def parse(self,
              response):

        # A way to get all the links to the next page
        links = response.xpath('//li/a/@href').extract()

        # The first entry is parent directory. We will avoid it.
        # Otherwise it will be an endless loop
        parent_directory = links.pop(0)

        # Check for all the links
        for link in links:
            # The full url
            link = response.url + link

            # In case of download limit reached no need to keep going
            if self.downloaded_count >= self.limit:
                return

            # If link does not ends with '/' then it is file
            elif not link.endswith('/'):
                # Get appropriate path to store this file
                path = self.get_path(link)

                # If file exists or allowable amount of file download is in process,
                # no need to go further
                if os.path.exists(path):
                    continue

                # Create the directory for the file to store
                directory = os.path.dirname(path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Keep track of downloaded files
                self.downloaded_count += 1

                # Append in pending job.
                # Will be removed when file is downloaded
                self.pending_downloads.append(link)

                # Process this file to store
                log.info("Downloading : {}".format(link))
                yield scrapy.Request(url=link, callback=self.save_file)
                continue

            # Go one level deep in directory structure
            self.urls_to_be_processed.append(link)

        if(self.urls_to_be_processed):
            url = self.urls_to_be_processed.pop(0)
            yield scrapy.Request(url=url, callback=self.parse)

    def get_path(self, url):
        # From URL generate path in file system where it will
        # be stored
        path = url.split(self.url)
        path = self.path + '/' + path[1]
        # Replace %20 with whitespace
        path = path.replace('%20', ' ')
        return path

    def save_file(self, response):
        # Get the path to store the file
        path = self.get_path(response.url)

        # Consider this file download job done
        self.pending_downloads.remove(response.url)

        # Write the content of the file
        with open(path, "wb") as f:
            f.write(response.body)

        log.info("Download Complete : {}".format(path))
        # Check if all pending jobs are done
        if not self.pending_downloads and \
           self.limit <= self.downloaded_count:
            # Stop the spider
            reactor.stop()
