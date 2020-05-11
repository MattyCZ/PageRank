import os
import sys

from scraper import Scraper

scraped_data = f'{os.path.dirname(os.path.realpath(__file__))}/scraped_data.json'
graph_data = f'{os.path.dirname(os.path.realpath(__file__))}/graph_data.json'
indexdir = 'indexdir'


if __name__ == '__main__':
    scraper = Scraper(scraped_data)

    scraper.run(max_pages=int(sys.argv[1]),
                start_urls=[sys.argv[2]],
                stay_on_domains=True if sys.argv[3] == 'True' else False)
