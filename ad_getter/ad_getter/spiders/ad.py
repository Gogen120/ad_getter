# -*- coding: utf-8 -*-
import scrapy

import ad_getter.spiders.constants as const

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ad_getter.spiders.utils import is_product_page


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
            Rule(LinkExtractor(deny=[r'compare', r'/tel:'], unique=True), callback='parse_item', follow=True)
        ]

        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        if (is_product_page(response, const.TAG_FIELD_MAP, const.PRODUCT_KEYWORDS) or
            is_product_page(response, const.NOT_IN_SHOP_TAGS, const.NOT_IN_SHOP_KEYWORDS)) and (
            is_product_page(response, const.SIMILAR_PRODUCT_TAGS, const.SIMILAR_PRODUCT_KEYWORDS) or
            is_product_page(response, const.DESCRIPTION_TAGS, const.DESCRIPTION_KEYWORDS)
        ):
            return {'url': response.url}
