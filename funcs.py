import pandas as pd
import string
import nltk
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