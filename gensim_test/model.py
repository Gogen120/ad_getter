import os
import gensim
import zipfile
import pandas as pd
import numpy as np

from preprocessing_udpipe import tag_uds, tag_ud


MODEL_URL = 'http://vectors.nlpl.eu/repository/11/180.zip'
MODEL_NAME = MODEL_URL.split('/')[-1]


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


def word_averaging(wv, words):
    all_words, mean = set(), []

    for word in words:
        if isinstance(word, np.ndarray):
            mean.append(word)
        elif word in wv.vocab:
            print(word)
            mean.append(wv.syn0norm[wv.vocab[word].index])
            all_words.add(wv.vocab[word].index)

    if not mean:
        print(f'Cannot compute similarity with no input {words}')
        return 0

    mean = gensim.matutils.unitvec(np.array(mean).mean(axis=0)).astype(np.float32)
    return mean


def word_averaging_list(wv, text_list):
    return np.vstack([word_averaging(wv, description) for description in text_list])


if __name__ == "__main__":
    df = pd.read_csv('partial_df.csv')
    print(df.shape)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    print(df.head())

    urls = pd.read_csv('urls.csv')
    print(urls.shape)
    print(urls['url'].head())
    first = df['description'][0].split()
    second = tag_ud([urls['html'][0]]).split()

    model = download_model()
    model.init_sims(replace=True)

    first_mean = word_averaging(model, first)
    print(first_mean)
