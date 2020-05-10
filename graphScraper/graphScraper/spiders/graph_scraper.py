# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import slugify
from threading import Lock
from urllib.parse import urlparse
from ..items import GraphscraperItem



class GraphScraperSpider(scrapy.Spider):
    name = 'graph_scraper'

    def __init__(self, max_pages=100, start_urls=None, stay_on_domains=True, **kw):
        super(GraphScraperSpider, self).__init__(**kw)
        if start_urls is None:
            start_urls = ['https://en.wikipedia.org/wiki/Main_Page']
        self.start_urls = start_urls
        if stay_on_domains:
            self.allowed_domains = [urlparse(x).netloc for x in start_urls]
        self.max_pages = max_pages
        self.visited = set()
        self.scraped = 0
        self.mutex = Lock()

    def parse(self, response):

        slug = slugify.slugify(response.request.url)
        title = response.xpath("//title/text()").get()
        title = ' '.join(BeautifulSoup(title, features="lxml").get_text().strip().split())

        dirtyText = ''.join(response.xpath("//body").getall())
        cleanText = ' '.join(BeautifulSoup(dirtyText, features="lxml").get_text().strip().split())
        links = set([response.urljoin(link) for link in response.xpath("//a/@href").getall()])

        item = GraphscraperItem()
        item["title"] = title
        item["url"] = response.request.url
        item["slug"] = slug
        item["outlinks"] = set()
        item["text"] = cleanText

        self.visited.add(slug)

        for link in links :
            link_slug = slugify.slugify(link)
            item["outlinks"].add(link_slug)

            if link_slug not in self.visited:
                self.visited.add(link_slug)
                yield response.follow(link, callback=self.parse)

        self.mutex.acquire()
        self.scraped += 1
        if self.scraped > self.max_pages:
            self.crawler.engine.close_spider(self, reason='finished')
            self.mutex.release()
            return
        self.mutex.release()
        yield item


