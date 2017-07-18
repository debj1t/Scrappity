import scrapy
from twisted.internet import reactor
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
        self.downloaded_count = 0
        self.pending_jobs = []

    def start_requests(self):
        # Our journey begins from here
        yield scrapy.Request(url=self.url, callback=self.parse)

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
                if os.path.exists(path) or self.downloaded_count >= self.limit:
                    return

                # Create the directory for the file to store
                directory = os.path.dirname(path)
                os.makedirs(directory)

                # Keep track of downloaded files
                self.downloaded_count += 1

                # Append in pending job.
                # Will be removed when file is downloaded
                self.pending_jobs.append(link)

                # Process this file to store
                yield scrapy.Request(url=link, callback=self.save_file)
                continue

            # Go one level deep in directory structure
            yield scrapy.Request(url=link, callback=self.parse)

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
        print ("Downloading :", path)
        # Consider this file download job done
        self.pending_jobs.remove(response.url)

        # Write the content of the file
        with open(path, "wb") as f:
            f.write(response.body)

        # Check if all pending jobs are done
        if not self.pending_jobs:
            # Stop the spider
            reactor.stop()
