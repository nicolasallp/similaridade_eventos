import pandas as pd
import numpy as np
import string
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def nltk_downloads():
  nltk.download("punkt_tab")
  nltk.download("stopwords")

def tratamento_texto(texto):
    texto = texto.lower()
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(texto)
    stop_words = set(stopwords.words("english"))
    tokens = [palavra for palavra in tokens if palavra not in stop_words]
    return ' '.join(tokens)

def obter_similaridade(query, dataFrame, top):
    consulta_tratada = tratamento_texto(query)
    tfidf = TfidfVectorizer()
    descricoes = dataFrame["texto_tratado"].tolist() + [consulta_tratada]
    tfidf_matriz = tfidf.fit_transform(descricoes)
    cosine_sim = cosine_similarity(tfidf_matriz[-1], tfidf_matriz[:-1])

    recomendacao = dataFrame
    recomendacao["Similaridade"] = cosine_sim[0].tolist()
    recomendacao = recomendacao.sort_values("Similaridade", ascending=False)
    return recomendacao.head(top)

def obter_similaridade_manual(query, dataFrame, top):
    tokens_consulta = word_tokenize(tratamento_texto(query))
    lista_tokens = [word_tokenize(descricao) for descricao in dataFrame["texto_tratado"]]

    bag_of_words_set = set()
    for tokens in lista_tokens:
        bag_of_words_set.update(tokens)
    bag_of_words = list(bag_of_words_set)
    vetor_consulta = [tokens_consulta.count(palavra) for palavra in bag_of_words]

    lista_vetores = []
    for tokens in lista_tokens:
        vetor = [tokens.count(palavra) for palavra in bag_of_words]
        lista_vetores.append(vetor)

    def valor_cosseno(v1, v2):
        u = np.array(v1)
        v = np.array(v2)
        cos = np.dot(u,v)/((np.linalg.norm(u))*(np.linalg.norm(v)))
        return np.degrees(np.arccos(cos))
    
    recomendacao = dataFrame
    recomendacao["Similaridade"] = [valor_cosseno(vetor_consulta, v) for v in lista_vetores]
    recomendacao = recomendacao.sort_values("Similaridade")
    return recomendacao.head(top)



