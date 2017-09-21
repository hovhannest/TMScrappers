from subprocess import call
import sys

call(["scrapy", "crawl", sys.argv[1], "-o", sys.argv[2]])
