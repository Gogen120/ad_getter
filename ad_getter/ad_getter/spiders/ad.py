# -*- coding: utf-8 -*-
import scrapy
import html2text

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AdSpider(CrawlSpider):
    handler = html2text.HTML2Text()
    handler.ignore_links = True
    handler.ignore_images = True
    name = 'ad'
    allowed_domains = ['55m.ru']
    start_urls = ['https://55m.ru']
    all_urls = set()

    rules = [Rule(LinkExtractor(canonicalize=True, unique=True, allow_domains=allowed_domains), callback='parse_item', follow=True)]

    def parse_item(self, response):
        urls = []
        links = LinkExtractor(canonicalize=True, unique=True, allow_domains=self.allowed_domains).extract_links(response)

        for link in links:
            if link.url not in self.all_urls:
                urls.append({'url': link.url, 'description': self.handler.handle(response.body.decode())})

        for url in urls:
            self.all_urls.add(url['url'])

        return urls
