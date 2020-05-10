from scrapy.crawler import CrawlerProcess
from graphScraper.graphScraper.spiders.graph_scraper import GraphScraperSpider
import os


class Scraper:
    def __init__(self, output=f'{os.path.dirname(os.path.realpath(__file__))}/scraped_data.json'):
        if os.path.exists(output):
            os.remove(output)
        self.settings = {
            "FEEDS": {
                output: {"format": "jsonlines"},
            },
            "CONCURRENT_REQUESTS" : 32
        }

    def run(self, max_pages, start_urls, stay_on_domains):
        process = CrawlerProcess(self.settings)
        spider = GraphScraperSpider(max_pages=max_pages, start_urls=start_urls, stay_on_domains=stay_on_domains)
        process.crawl(GraphScraperSpider, max_pages=max_pages, start_urls=start_urls, stay_on_domains=stay_on_domains)
        process.start()

    def runDefault(self):
        process = CrawlerProcess(self.settings)
        spider = GraphScraperSpider()
        process.crawl(spider)
        process.start()
