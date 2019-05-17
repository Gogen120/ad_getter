import os
import re
import sys
import requests
import zipfile
import wget
import gensim
import xml
import time
import pandas as pd
import numpy as np
import defusedxml.ElementTree as et

from pprint import pprint

from preprocessing_udpipe import tag_uds


'''
1. Создать датасет с описаниеми товаров
2. Добавить данные для отрицательного класса
3. Обработать данные используя скрипт от rusvectors
4 Разбить датасет на тренировочный и тестовый
5. Обучить модель, для бейслайна Логистическую регрессию
6. Провалидировать модель на тестовых данных
'''


CSV_FILE = 'feed_urls.csv'
MODEL_URL = 'http://vectors.nlpl.eu/repository/11/180.zip'
MODEL_NAME = MODEL_URL.split('/')[-1]
INVALID_URLS = (
    'https://compiled.petrovichstd.ru/feed/yandex_spb.yml',
    'http://export.admitad.com/ru/webmaster/websites/951576/products/export_adv_products/?user=OlegEgorov&code=a5b68f0367&feed_id=15260&format=xml'
)


def read_feed_urls():
    urls_df = pd.read_csv('feed_urls.csv', sep='\t')
    return urls_df.drop(['client_id', 'project_id', 'title'], axis=1)


def create_df(urls, descriptions):
    processed_descriptions = tag_uds(descriptions)
    df = pd.DataFrame(data={'url': urls, 'description': processed_descriptions, 'is_product_page': 1})
    return df


def get_xml_data(xml_url):
    if not os.path.exists('test.xml'):
        xml_data = requests.get(xml_url).text
        with open('test.xml', 'w') as f:
            f.write(xml_data)
    else:
        with open('test.xml', 'r') as f:
            xml_data = f.read()

    return xml_data


def preprocess_data(texts):
    for document in texts:
        yield gensim.utils.simple_preprocess(document)


def parse_xml(xml_url):
    urls = []
    descriptions = []
    for xml_url in urls_df['url'][1:3]:
        print(xml_url)
        if xml_url in INVALID_URLS:
            continue
        try:
            xml_data = requests.get(xml_url).text
        except (requests.exceptions.SSLError, requests.exceptions.InvalidSchema):
            continue
        try:
            root = et.fromstring(xml_data)
        except xml.etree.ElementTree.ParseError:
            continue
        for offer in root.iter('offer'):
            texts = []
            if offer.find('description') is None:
                continue
            if offer.find('description').text is not None:
                texts.append(offer.find('description').text)
            try:
                for child in list(offer.find('description')):
                    if not list(child):
                        texts.append(child.text)
                    else:
                        for subchild in child:
                            texts.append(subchild.text)
                if texts:
                    descriptions.append(texts)
                else:
                    continue
            except TypeError:
                continue

            urls.append(offer.findtext('url'))

    return urls, descriptions


def extract_model_from_zip():
    with zipfile.ZipFile(MODEL_NAME, 'r') as archive:
        stream = archive.open('model.bin')
        model = gensim.models.KeyedVectors.load_word2vec_format(stream, binary=True)

    return model


def download_model():
    if os.path.exists(MODEL_NAME):
        return extract_model_from_zip()

    model = wget.download(MODEL_URL)
    return extract_model_from_zip()


if __name__ == "__main__":
    urls_df = read_feed_urls()
    start = time.time()
    urls, descriptions = parse_xml(urls_df)
    print('=====================================================')
    print(f'Parsing taken {(time.time() - start) / 60} minutes')
    print('=====================================================')
    descriptions = list(descriptions)
    print(len(urls))
    print(len(descriptions))

    df = create_df(urls, descriptions)
    print(df.head())
    print(df.tail())
    print(df.shape)

    df.to_csv('partial_df.csv')

    # df.to_csv('df.csv')

    # model = download_model()
    # model.build_vocab(descriptions)
