import ad_getter.spiders.constants as const

from scrapy.exceptions import NotSupported
from scrapy.http.response.html import HtmlResponse


def extract_matched_tags_values(response: HtmlResponse, tags: dict) -> list:
    """Extract and clean all values that match given tags map"""
    matched_values = [response.xpath(f'//{tag}/{field}').getall() for tag, field in tags.items()]
    return [
        value.lower().strip().replace(':', '') for values in matched_values
        for value in values if value is not None
    ]


def is_product_page(response: HtmlResponse, tags: dict, keywords: tuple) -> bool:
    """Check if page contains any of possible product page keywords"""
    try:
        matched_values = extract_matched_tags_values(response, tags)
    except NotSupported:
        return False

    for keyword in keywords:
        if keyword in matched_values:
            return True

    return False
