# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import slugify
from threading import Lock

from graphScraper.items import GraphscraperItem


class GraphScraperSpider(scrapy.Spider):
    name = 'graph_scraper'
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']
    max_pages = 100
    visited = set()
    scraped = 0
    mutex = Lock()
    allowed_domains = ['en.wikipedia.org']

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

        for link in links:
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
