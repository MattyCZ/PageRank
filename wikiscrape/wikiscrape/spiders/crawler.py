import scrapy
import threading
from slugify import slugify

START_URL = 'https://en.wikipedia.org/wiki/Main_Page'
ALLOWED_DOMAIN = 'en.wikipedia.org'

max_pages = 20
pages_lock = threading.Lock()
visited = set()


class PageRankSpider(scrapy.Spider):
    name = "wikiscrape"
    start_urls = [START_URL]
    allowed_domains = [ALLOWED_DOMAIN]

    def parse(self, response):
        title = response.css('title::text').get()
        url = response.request.url

        content = response.css('body').getall()
        content = ''.join(content)
        content = content.splitlines()
        content = [x.strip() for x in content if x.strip() != '']
        content = '\n'.join(content)
        slug = slugify(url)
        yield {
            'title': title,
            'url': url,
            'slug': slug,
            'content': content,
        }
        print(f'Len of visited: {len(visited)}')

        for next_page in response.css('a::attr(href)').getall():
            if next_page[0] == '/':
                to_url = response.url.split(ALLOWED_DOMAIN)[0] + ALLOWED_DOMAIN + next_page
            else:
                to_url = next_page
            if slugify(to_url) not in visited:
                if len(visited) < max_pages:
                    visited.add(slugify(to_url))
                    yield response.follow(next_page, self.parse)
            else:
                pass  # Add to graph
