# -*- coding: utf-8 -*-
import scrapy

import ad_getter.spiders.constants as const

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ad_getter.spiders.utils import is_product_page


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
            Rule(LinkExtractor(allow=[r'{}'.format(self.start_urls[0])], deny=[r'compare', r'/tel:', r'\.php'], unique=True),
                 callback='parse_item', follow=True)
        ]

        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        if (is_product_page(response, const.BUY_TAGS, const.BUY_KEYWORDS) or
            is_product_page(response, const.NOT_IN_SHOP_TAGS, const.NOT_IN_SHOP_KEYWORDS)) and (
            is_product_page(response, const.SIMILAR_PRODUCT_TAGS, const.SIMILAR_PRODUCT_KEYWORDS) or
            is_product_page(response, const.DESCRIPTION_TAGS, const.DESCRIPTION_KEYWORDS)
        ):
            return {'url': response.url}
