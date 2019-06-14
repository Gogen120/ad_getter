import ad_getter.spiders.constants as const

from scrapy.exceptions import NotSupported
from scrapy.http.response.html import HtmlResponse


def extract_matched_tags_values(response: HtmlResponse, tags: dict) -> list:
    """Extract and clean all values that match given tags map"""
    matched_values = []
    for tag, fields in tags.items():
        if isinstance(fields, str):
            matched_values.append(response.xpath(f'//{tag}/{fields}').getall())
        else:
            for field in fields:
                matched_values.append(response.xpath(f'//{tag}/{field}').getall())
    return [
        value.lower().strip().replace(':', '') for values in matched_values
        for value in values if value is not None
    ]


def page_has_keywords(response: HtmlResponse, tags: dict, keywords: tuple) -> bool:
    """Check if page contains any of possible product page keywords"""
    try:
        matched_values = extract_matched_tags_values(response, tags)
    except NotSupported:
        return False

    for keyword in keywords:
        if keyword in matched_values:
            return True

    return False


def page_contains_buy_tags(response: HtmlResponse) -> bool:
    if '?' in response.url:
        return False

    return page_has_keywords(response, const.BUY_TAGS, const.BUY_KEYWORDS) or \
        page_has_keywords(response, const.NOT_IN_SHOP_TAGS, const.NOT_IN_SHOP_KEYWORDS)


def page_contains_description_tags(response: HtmlResponse) -> bool:
    if '?' in response.url:
        return False

    return page_has_keywords(response, const.SIMILAR_PRODUCT_TAGS, const.SIMILAR_PRODUCT_KEYWORDS) or \
        page_has_keywords(response, const.DESCRIPTION_TAGS, const.DESCRIPTION_KEYWORDS) or \
        page_has_keywords(response, const.REVIEW_TAGS, const.REVIEW_KEYWORDS)
