import os

from pprint import pprint
from collections import defaultdict

from gensim import models
from gensim import similarities
from gensim import corpora

CORPUS = [
    [(0, 1.0), (1, 1.0), (2, 1.0)],
    [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
    [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
    [(0, 1.0), (4, 2.0), (7, 1.0)],
    [(3, 1.0), (5, 1.0), (6, 1.0)],
    [(9, 1.0)],
    [(9, 1.0), (10, 1.0)],
    [(9, 1.0), (10, 1.0), (11, 1.0)],
    [(8, 1.0), (10, 1.0), (11, 1.0)]
]


DOCUMENTS = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",              
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]


class MyCorpus:
    def __init__(self, filename, dictionary):
        self.filename = filename
        self.dictionary = dictionary

    def __iter__(self):
        for line in open(self.filename):
            yield self.dictionary.doc2bow(line.lower().split())


def tdifd_test():
    tfidf = models.TfidfModel(CORPUS)

    vec = [(0, 1), (4, 1)]
    print(tfidf[vec])

    index = similarities.SparseMatrixSimilarity(tfidf[CORPUS], num_features=12)
    sims = index[tfidf[vec]]
    print(list(enumerate(sims)))


def corpora_test():
    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [
        [word for word in document.lower().split() if word not in stoplist]
        for document in DOCUMENTS
    ]

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for word in text:
            frequency[word] += 1

    texts = [
        [token for token in text if frequency[token] > 1]
        for text in texts
    ]

    pprint(texts)

    dictionary = corpora.Dictionary(texts)
    dictionary.save('deerwester.dict')
    print(dictionary.token2id)

    new_doc = 'Human computer interacion'
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    print(new_vec)

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('deerwester.mm', corpus)
    pprint(corpus)

    corpus_memory_friendly = MyCorpus('mycorpus.txt', dictionary)
    print(corpus_memory_friendly)

    for vector in corpus_memory_friendly:
        print(vector)


def corpus_formats():
    corpus = [[(1, 0.5)], []]
    corpora.MmCorpus.serialize('corpus.mm', corpus)
    corpora.SvmLightCorpus.serialize('corpus.svmlight', corpus)
    corpora.BleiCorpus.serialize('corpus.lda-c', corpus)
    corpora.LowCorpus.serialize('corpus.low', corpus)

    corpus = corpora.MmCorpus('corpus.mm')
    print(corpus)
    print(list(corpus))
    for doc in corpus:
        print(doc)


def transformation():
    if (os.path.exists('deerwester.dict')):
        dictionary = corpora.Dictionary.load('deerwester.dict')
        corpus = corpora.MmCorpus('deerwester.mm')
        print('Used files generated from first tutorial')
    else:
        print('Please run first tutorial to generate data set')

    tfidf = models.TfidfModel(corpus)

    doc_bow = [(0, 1), (1, 1)]
    print(tfidf[doc_bow])

    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print(doc)

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
    corpus_lsi = lsi[corpus_tfidf]
    print(lsi.print_topics(2))

    for doc in corpus_lsi:
        print(doc)

    lsi.save('model.lsi')
    lsi = models.LsiModel.load('model.lsi')


def similariti_interface():
    dictionary = corpora.Dictionary.load('deerwester.dict')
    corpus = corpora.MmCorpus('deerwester.mm')
    print(corpus)

    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    doc = 'Human computer interaction'
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow]
    print(vec_lsi)

    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save('deerwester.index')
    index = similarities.MatrixSimilarity.load('deerwester.index')

    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)
    print(sims)


if __name__ == "__main__":
    similariti_interface()
