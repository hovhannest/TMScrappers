from subprocess import call
import sys
import os

try:
    os.remove(sys.argv[2])
except:
    pass
call(["scrapy", "crawl", sys.argv[1]])
