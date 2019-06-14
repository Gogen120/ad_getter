import argparse
import re

import ad_getter.spiders.constants as const


def read_urls_file(url_file: str) -> list:
    """Read file with urls and return list of urls"""
    with open(url_file, 'r') as f:
        urls = [url.strip() for url in f.readlines()[1:]]

    return urls


def get_product_pages_counter(urls: list, domain: str) -> dict:
    """
        Count pages that match given pattern (product pages)
        and flase positive not product pages
    """
    product_page_counter = {}
    for url in urls:
        if re.fullmatch(
            r'http[s]?://{}/{}{}'.format(domain, const.PRODUCT_ROUTES, const.EXTRA_ROUTES), url
        ) is not None:
            product_page_counter['product_page'] = (
                product_page_counter.get('product_page', 0) + 1
            )
        else:
            product_page_counter['not_product_page'] = (
                product_page_counter.get('not_product_page', 0) + 1
            )

    return product_page_counter


def precision_score(product_page_counter: dict) -> float:
    """Get precision score"""
    if not product_page_counter:
        return 0.0

    return product_page_counter.get('product_page', 0) / (
        product_page_counter.get('product_page', 0) + product_page_counter.get('not_product_page', 0)
    )


def init_args():
    """Initialize cli arguments"""
    args = argparse.ArgumentParser()
    args.add_argument('-d', '--domain', required=True, help='domain to check')
    args.add_argument('-f', '--filename', required=True, help='file with urls to check')

    return args.parse_args()


def main():
    args = init_args()

    urls = read_urls_file(args.filename)
    product_page_counter = get_product_pages_counter(urls, args.domain)

    print(precision_score(product_page_counter))


if __name__ == "__main__":
    main()
