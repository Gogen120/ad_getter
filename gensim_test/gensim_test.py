import re
import sys
import logging
import zipfile
import wget
import gensim
import requests

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

MODEL1 = 'ruscorpora_upos_cbow_300_20_2019'
MODEL2 = 'tayga_upos_skipgram_300_2_2019'
FORMAT = 'csv'


def api_neighbor(model, word, output_format):
    neighbors = {}
    url = f'https://rusvectores.org/{model}/{word}/api/{output_format}/'
    response = requests.get(url=url, stream=True)
    for line in response.text.split('\n')[2:-1]:
        neighbor, similarity = re.split('\s+', line)
        neighbors[neighbor] = similarity

    return neighbors


def api_similarity(model, word1, word2):
    url = f'https://rusvectores.org/{model}/{word1}__{word2}/api/similarity/'
    response = requests.get(url, stream=True)
    return response.text.split('\t')


def download_model(model_url):
    model = wget.download(model_url)
    model_file = model_url.split('/')[-1]
    with zipfile.ZipFile(model_file, 'r') as archive:
        stream = archive.open('model.bin')
        model = gensim.models.KeyedVectors.load_word2vec_format(stream, binary=True)

    return model


def found_k_nearest_neighboors(model, words, k=10):
    for word in words:
        if word in model:
            print(word)
            for i in model.most_similar(positive=[word], topn=k):
                print(i[0], i[1])
            print('\n')
        else:
            print(f'{word} is not present in the model')


if __name__ == "__main__":
    model = download_model('http://vectors.nlpl.eu/repository/11/180.zip')
    words = ['день_NOUN', 'ночь_NOUN', 'человек_NOUN', 'семантика_NOUN', 'студент_NOUN', 'студент_ADJ']

    found_k_nearest_neighboors(model, words)
    print(model.similarity('человек_NOUN', 'обезьяна_NOUN'))
    print(model.doesnt_match('яблоко_NOUN груша_NOUN виноград_NOUN банан_NOUN лимон_NOUN картофель_NOUN'.split()))
    print(model.most_similar(positive=['пицца_NOUN', 'россия_NOUN'], negative=['италия_NOUN']))

    # print(api_neighbor(MODEL1, 'человек_NOUN', FORMAT))
    # print(api_similarity(MODEL2, 'человек_NOUN', 'мех_NOUN'))

