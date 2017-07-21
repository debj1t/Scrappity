import argparse
import os
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

# The parser
from CnqzuParser import CnqzuParser

def CommonErrorFunction(err):
    print("Unexpected error occured. Traceback :\n%s" %err.getBriefTraceback())
    reactor.stop()

# Parser handle to parse the arguments
parser = argparse.ArgumentParser()

# Add positional argument
parser.add_argument("url",
                    help="url address to crawl")

# Add optional arguments
parser.add_argument("-p",
                    "--path",
                    help="path to store downloaded files")


parser.add_argument("-g",
                    "--genre",
                    help="download files specific to genre")

parser.add_argument("-l",
                    "--limit",
                    type=int,
                    default=1,
                    help="limit downloaded files count")

parser.add_argument("-v",
                    "--verbose",
                    default=False,
                    action="store_true",
                    help="increase output verbosity")

# Parse all the arguments
args = parser.parse_args()

# In case no path is provided, 'pwd' is used
if args.path is None:
    args.path = os.getcwd()

# Get a runner for scrappy
runner = CrawlerRunner()

# Add the parser spider
d = runner.crawl(CnqzuParser,
                 **args.__dict__)

# Add reactor stop so that after done it can close
d.addCallbacks(lambda _: reactor.stop(), CommonErrorFunction)

# Run the reactor
reactor.run()
