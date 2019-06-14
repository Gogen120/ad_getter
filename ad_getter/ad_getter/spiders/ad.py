# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ad_getter.spiders.utils import page_contains_buy_tags, page_contains_description_tags


class AdSpider(CrawlSpider):
    """
    Spider that get all product pages from given domain

    Command to run: scrapy crawl ad -o <file_name>.csv -t csv -a domain=<domain_name> -a start_url=<start_url>
    """
    name = 'ad'

    def __init__(self, *args, **kwargs):
        self.allowed_domains = [f'{kwargs.get("domain")}']
        self.start_urls = [f'{kwargs.get("start_url")}']

        self.rules = [
            Rule(
                LinkExtractor(
                    allow=[r"{}".format(self.start_urls[0])],
                    deny=[r"compare", r"/tel:", r"\.php"],
                    unique=True,
                ),
                callback='parse_item',
                follow=True,
            )
        ]

        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        if page_contains_buy_tags(response) and page_contains_description_tags(response):
            return {'url': response.url}
