from unicodedata import normalize
from nltk.corpus import stopwords

import re
import pandas as pd
import requests
import json
import nltk


#nltk.data.path.append("/home/agu/Desktop/tesis/utils/stopwords") # Ubuntu Virtualbox
nltk.data.path.append("/home/agu/repos/tesis/utils/stopwords") # Notebook
stop = stopwords.words('spanish')

def obtener_id_from_url(url):
    """Funcion para obtener el ID de productos a través de su URL"""
    id_prod = re.search(r'/p/(.+?)\?', url)
    if id_prod:
        return id_prod.group(1)
    url_split = url.split("/p/")
    if len(url_split) > 1:
        return url_split[1]
    return False


def convert_response_to_list(reviews):
    """Funcion para retornar algunas cosas de los comentarios"""
    list_reviews = []
    for review in reviews:
        new_json = {
            "titulo": review['title'].lower(),
            "comentario": review['content'].lower(),
            "valoracion": review['rate']
        }
        list_reviews.append(new_json)
    return list_reviews

def obtener_df_reviews(id_prod):
    """Funcion para llamar a la API de ML y obtener los comentarios"""
    url_api = "https://api.mercadolibre.com/reviews/item/"
    url = url_api + id_prod
    args = {'limit': 200}

    response = requests.get(url, params=args)
    if response.status_code != 200:
        return ""
    response_json = json.loads(response.text)
    reviews = convert_response_to_list(response_json['reviews'])
    df_comentarios = pd.DataFrame.from_records(reviews)
    return df_comentarios


def preprocesar_comentarios_df(df_comentarios):
    """funcion para realizar un preprocesado de los comentarios"""

    # Elimino signos como guines, dos puntos, etc.
    df_comentarios["comentario"] = df_comentarios['comentario'].str.replace(r'[^\w\s]','')


    # Dejo solo las palabras que no se encuentren dentro de las stopwords y que no son numericas
    df_comentarios["comentario"] = df_comentarios["comentario"].apply(
        lambda x: ' '.join(
            [word for word in x.split()
             if (word.lower() not in (stop)) and (word.isnumeric() is False)
            ]
        )
    )


    # Con estas sentencias elimino todo tilpo de tildes, dieresis, etc (a excepcion de las ñ)
    df_comentarios["comentario"] = df_comentarios["comentario"].apply(
        lambda x: normalize(
            'NFC',
             re.sub(
                r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
                normalize("NFD", x), 0, re.I
            )
       )
    )
    return df_comentarios[["comentario"]]
