# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.response.html import HtmlResponse
from scrapy.exceptions import NotSupported

TAG_FIELD_MAP = {
    '*': '@value',
    'span': 'text()',
    'a': 'text()',
    'button': 'text()'
}

CHARS_TO_TRANSLATE = 'КВ'


def is_page_contains_keyword(response: HtmlResponse, keyword: str) -> bool:
    """Check if page contains given keyword in tag provided by TAG_FIELD_MAP"""
    for tag, field in TAG_FIELD_MAP.items():
        try:
            if response.xpath(
                f'//{tag}[contains(translate({field}, "{CHARS_TO_TRANSLATE}", "{CHARS_TO_TRANSLATE.lower()}"), "{keyword}")]'
            ).getall():
                return True
        except NotSupported:
            return False

    return False


def is_product_page(response: HtmlResponse) -> bool:
    """Check if page contains any of possible product page keywords"""
    return is_page_contains_keyword(response, 'купить') or \
        is_page_contains_keyword(response, 'в корзину')


class AdSpider(CrawlSpider):
    """
    Spider that get all product pages from given domain

    Command to run: scrapy crawl ad -o <file_name>.csv -t csv -a domain=<domain_name>
    """
    name = 'ad'

    def __init__(self, *args, **kwargs):
        self.allowed_domains = [f'{kwargs.get("domain")}']
        self.start_urls = [f'https://{kwargs.get("domain")}']

        self.rules = [
            Rule(LinkExtractor(canonicalize=True, unique=True),
                 callback='parse_item',
                 follow=True)
        ]

        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        if is_product_page(response):
            return {'url': response.url}
