import pandas as pd
import datetime
from sqlalchemy import create_engine
import configparser
import psycopg2
from wrangling import word_cloud
import collections

if __name__ == "__main__":
########## carga de database

    cfg = configparser.RawConfigParser()
    cfg.read('/home/carpiero/ir/pass_projects/pass.ini')

    user = cfg['ssh']['username']
    passw = cfg['ssh']['password']
    # engine = create_engine(f'postgresql://{user}:{passw}@192.168.1.170/carpiero' )
    # engine = create_engine(f'postgresql://{user}:{passw}@asuscar.duckdns.org/carpiero',echo=True )

    engine = create_engine(f'postgresql://{user}:{passw}@localhost/carpiero' )
    sqlite_connection = engine.connect()

    df = pd.read_sql_query("SELECT * FROM twitter_operators_sent_02" , engine , coerce_float=True ,parse_dates=['created_at'])

    today = datetime.date.today()
    yest = today - datetime.timedelta(days=1)

    today2=pd.to_datetime(today)
    yest2=pd.to_datetime(yest)

    start_date=yest2
    end_date=today2

    df=df.loc[(df['created_at'] >= start_date) & (df['created_at'] < end_date)]

    df['Year'] = pd.DatetimeIndex(df['created_at']).year
    df['Month'] = pd.DatetimeIndex(df['created_at']).month
    df['Day'] = pd.DatetimeIndex(df['created_at']).day

    df = df.loc[~df['Tweet_Content'].str.contains(
            'viernestopenmasmovil|redlovesgreen|Estudiantes|sorteamos|sorteando|cuspinera|s o r t e o|realmadrid|colorweek|taehyung|sorteo|concurso|concursazo|sorteazo|regalamos|cumplelowiconlg|laliga|concierto|cestavodafone|Movistar Liga de Campeones' ,
            case=False)]

    df['Tweet_Content_Token'] = df['Tweet_Content'].apply(word_cloud.spacy_tokenizer)

    counts_nsw = collections.Counter([text for i in df['Tweet_Content_Token'] for text in i])

    sorted_keys = sorted(counts_nsw, key=counts_nsw.get, reverse=True)

    for p,i in enumerate(sorted_keys):
        if p < 7:
            print(i,':', counts_nsw[i])

    # df_yest=pd.read_parquet('./data/df.parquet')
    df_yest=pd.read_parquet('/home/carpiero/ir/Sentiment_Spanish_Operator/data/df_total.parquet')
    print(df_yest)
    df_total = pd.concat([df_yest , df] , axis=0)
    print(df_total)

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
        df_total.loc[: , feature] = df_total[feature].astype(dtype)

    # df_total = df_total[df_total['username'] != '@vodafoneyu']
    print('\n\nwrite parquet')
    df_total.to_parquet('/home/carpiero/ir/Sentiment_Spanish_Operator/data/df_total.parquet')


    print(f'\n\nFinish Update Day: \n\n{datetime.date.today()} - {datetime.datetime.now().strftime("%H:%M:%S")}\n\n')







