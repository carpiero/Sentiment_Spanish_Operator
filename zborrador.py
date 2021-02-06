import matplotlib.pyplot as plt
from os import path
from PIL import Image
import seaborn as sns
import numpy as np
import plotly.express as px
plt.style.use('seaborn')
import re
# import tweepy
import pandas as pd
import datetime
from sqlalchemy import create_engine
# from sshtunnel import SSHTunnelForwarder
import configparser
import psycopg2
from wrangling import word_cloud


if __name__ == "__main__":

    cfg = configparser.RawConfigParser()
    cfg.read('/home/carpiero/ir/pass_projects/pass.ini')

    user = cfg['ssh']['username']
    passw = cfg['ssh']['password']
    engine = create_engine(f'postgresql://{user}:{passw}@192.168.1.170/carpiero' , echo=True)
    # engine = create_engine(f'postgresql://{user}:{passw}@localhost/carpiero' , echo=True)
    sqlite_connection = engine.connect()

    df_postgresql = pd.read_sql_query("SELECT * FROM twitter_operators_sent" , engine , coerce_float=True ,parse_dates=['created_at'])

    feature_types = {
        'name': 'category' ,
        'user_id': 'category' ,
        'user_location': 'category' ,
        'source': 'category' ,
        'reply_user_id': 'category' ,
        'reply_status_id': 'category' ,
        'username': 'category' ,
        'GRUPO': 'category' ,
    }
    for feature , dtype in feature_types.items():
        df_postgresql.loc[: , feature] = df_postgresql[feature].astype(dtype)

    df_postgresql['Year'] = pd.DatetimeIndex(df_postgresql['created_at']).year
    df_postgresql['Month'] = pd.DatetimeIndex(df_postgresql['created_at']).month
    df_postgresql['Day'] = pd.DatetimeIndex(df_postgresql['created_at']).day

    df = df_postgresql.loc[~df_postgresql['Tweet_Content'].str.contains(
        'viernestopenmasmovil|s o r t e o|realmadrid|colorweek|taehyung|sorteo|concurso|sorteazo|regalamos|cumplelowiconlg|laliga|concierto|cestavodafone|Movistar Liga de Campeones' ,
        case=False)]


    print(df_postgresql.info(memory_usage='deep'))
    print(df.info(memory_usage='deep'))


    df['Tweet_Content_Token'] = df['Tweet_Content'].apply(word_cloud.spacy_tokenizer)

    star = 5
    # all_words = ' '.join([text for i in df.loc[(df['stars']==star)&(df['username']== user),'Tweet_Content_Token'] for text in i])
    all_words = ' '.join([text for i in df.loc[(df['stars'] == star) , 'Tweet_Content_Token'] for text in i])
    # all_words = ' '.join([text for i in df['Tweet_Content_Token'] for text in i])
    print(len(all_words))

    wc=word_cloud.generate_wordcloud(all_words)

    plt.figure(figsize=(14 , 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')
    plt.savefig(f'./Data/Wordcloud_{star}.pdf' ,
                transparent=False ,
                dpi=80 ,
                bbox_inches="tight")






















