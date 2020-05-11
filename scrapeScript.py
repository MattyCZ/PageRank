import os
import sys

from scraper import Scraper

if __name__ == '__main__':
    scraper = Scraper(sys.argv[1])
    scraper.run(max_pages=int(sys.argv[2]),
                start_urls=[sys.argv[3]],
                stay_on_domains=True if sys.argv[4] == 'True' else False)
