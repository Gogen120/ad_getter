import ad_getter.spiders.constants as const

from scrapy.exceptions import NotSupported
from scrapy.http.response.html import HtmlResponse


def is_page_contains_keyword(response: HtmlResponse, keyword: str, tags: dict) -> bool:
    """Check if page contains given keyword in tag provided by tags argument"""
    for tag, field in tags.items():
        try:
            if response.xpath(
                f'//{tag}[(translate({field}, "{const.CHARS_TO_TRANSLATE}", "{const.CHARS_TO_TRANSLATE.lower()}") = "{keyword}")]'
            ).get() is not None:
                return True
        except NotSupported:
            return False

    return False


def is_product_page(response: HtmlResponse, tags: dict, keywords: dict) -> bool:
    """Check if page contains any of possible product page keywords"""
    return any([is_page_contains_keyword(response, keyword, tags) for keyword in keywords])
