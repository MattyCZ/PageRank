from scrapy.crawler import CrawlerProcess
from graphScraper.graphScraper.spiders.graph_scraper import GraphScraperSpider
import os
import platform


class Scraper:
    def __init__(self, output):
        print(output)
        if os.path.exists(output):
            os.remove(output)

        if platform.system() == 'Windows':
            output = output[3:]
            output = output.replace('\\', '/')
            output = f'file:///{output}'
        self.settings = {
            'FEEDS': {
                output: {'format': 'jsonlines'},
            },
            'CONCURRENT_REQUESTS': 32,
        }

    def run(self, max_pages, start_urls, stay_on_domains):
        process = CrawlerProcess(self.settings)
        process.crawl(GraphScraperSpider, max_pages=max_pages, start_urls=start_urls, stay_on_domains=stay_on_domains)
        process.start()

    def runDefault(self):
        process = CrawlerProcess(self.settings)
        process.crawl(GraphScraperSpider)
        process.start()
