from gensim.models.fasttext import FastText as FT_gensim
from gensim.test.utils import datapath
from nltk.corpus import stopwords


if __name__ == "__main__":
    corpus_file = datapath('lee_background.cor')
    model_gensim = FT_gensim(size=100)

    model_gensim.build_vocab(corpus_file=corpus_file)

    model_gensim.train(
        corpus_file=corpus_file, epochs=model_gensim.epochs,
        total_example=model_gensim.corpus_count, total_words=model_gensim.corpus_total_words
    )

    print(model_gensim)

    print('night' in model_gensim.wv.vocab)
    print('nights' in model_gensim.wv.vocab)
    print(model_gensim.similarity('night', 'nights'))
    print(model_gensim.most_similar('nights'))

    sentence_obama = 'Obama speaks to the media in Illinois'.lower().split()
    sentence_president = 'The president greets the press in Chicago'.lower().split()

    stopwords = stopwords.words('english')
    sentence_obama = [w for w in sentence_obama if w not in stopwords]
    sentence_president = [w for w in sentence_president if w not in stopwords]

    distance = model_gensim
