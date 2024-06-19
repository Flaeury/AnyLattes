import datetime
import os
from models.consulta import *
import wordcloud
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def nuvem_geral():
    texto = []
    res = lista('1500', str(datetime.date.today().year))

    nltk.download('stopwords')

    researchers_words = ' '
    pt_words = list(nltk.corpus.stopwords.words('portuguese'))
    en_words = list(wordcloud.STOPWORDS)
    stop = pt_words + en_words

    stop.append('based')
    stop.append('using')
    stop.append('use')
    stop.append('study')
    stop.append('baseado')
    stop.append('usando')
    stop.append('dizem')
    stop.append('estudo')

    for r in res:
        texto.append(r[4])


    if type(texto) == list:
        for text in texto:
            if text != None:
                researchers_words = researchers_words + text + ' '
        wc = WordCloud(width=3000, height=2000, stopwords=stop, min_word_length=2,
                       random_state=1, collocations=False).generate(researchers_words)

   
    plt.figure(1, figsize=(20, 15), dpi=100)
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    wc.to_file('static/images/nuvem_de_palavras.png')
    plt.clf()
    plt.cla()
    # plt.savefig('static/images/nuvem_de_palavras.png',transparent= True)


