import tweepy
import pandas as pd
import numpy as np
import datetime
import configparser
from sqlalchemy import create_engine
import sqlalchemy

def update_twitter_database():
    cfg = configparser.RawConfigParser()
    cfg.read('/home/carpiero/ir/pass_projects/pass.ini')

    CK= cfg['token_twitter']['CONSUMER_KEY']
    CS= cfg['token_twitter']['CONSUMER_SECRET']
    AT= cfg['token_twitter']['ACCESS_TOKEN']
    AS= cfg['token_twitter']['ACCESS_SECRET']

    CONSUMER_KEY = CK
    CONSUMER_SECRET = CS
    ACCESS_TOKEN = AT
    ACCESS_SECRET = AS

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


    CK2= cfg['token_twitter']['CONSUMER_KEY2']
    CS2= cfg['token_twitter']['CONSUMER_SECRET2']
    AT2= cfg['token_twitter']['ACCESS_TOKEN2']
    AS2= cfg['token_twitter']['ACCESS_SECRET2']

    CONSUMER_KEY = CK2
    CONSUMER_SECRET = CS2
    ACCESS_TOKEN = AT2
    ACCESS_SECRET = AS2

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api2 = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


    CK3= cfg['token_twitter']['CONSUMER_KEY3']
    CS3= cfg['token_twitter']['CONSUMER_SECRET3']
    AT3= cfg['token_twitter']['ACCESS_TOKEN3']
    AS3= cfg['token_twitter']['ACCESS_SECRET3']

    CONSUMER_KEY = CK3
    CONSUMER_SECRET = CS3
    ACCESS_TOKEN = AT3
    ACCESS_SECRET = AS3

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api3 = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    # username = ['@vodafone_es','@orange_es','@Amena','@TuentiES','@jazztel_es',
    #             '@masmovil','@pepephone','@o2es','@simyo_es',
    #             '@movistar_es','@vodafoneyu',
    #             '@Lowi_es','@yoigo']

    apis_username = {api: ['@vodafone_es' , '@vodafoneyu' , '@simyo_es' , '@pepephone'] ,
                     api2: ['@yoigo' , '@o2es' , '@masmovil' , '@Amena'] ,
                     api3: ['@orange_es' , '@movistar_es' , '@Lowi_es' , '@TuentiES' , '@jazztel_es'],
                     }

    # apis_username = {api: ['@pepephone'] ,
    #
    #                  }

    count = 6000

    today = datetime.date.today()
    yest = today - datetime.timedelta(days=1)
    yest2 = today - datetime.timedelta(days=2)
    tomorrow = today + datetime.timedelta(days=1)
    since=yest
    until=today
    print(f'Until: {until}')
    print(f'Since: {since}')
    # print(tomorrow)

    tweets_df_total = pd.DataFrame()

    for k , v in apis_username.items():
        for x in range(len(v)):

            # for x in username:
            # Creation of query method using parameters
            #     tweets = tweepy.Cursor(api.user_timeline,id=username, since=date_since, until=date_until).items(count)

            tweets = tweepy.Cursor(k.search , q=v[x] , since=since , until=until,result_type='recent').items(count)

            tweets_list = [[tweet.created_at , tweet.id_str , tweet.text , tweet.user.name , tweet.user.id_str ,
                            tweet.user.followers_count ,
                            tweet.user.location , tweet.source , tweet.entities ,
                            tweet.in_reply_to_user_id_str , tweet.in_reply_to_status_id_str ,
                            tweet.favorite_count , tweet.retweet_count] for tweet in tweets]

            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet information
            tweets_df = pd.DataFrame(tweets_list)

            if len(tweets_df) == 0:
                pass
            else:
                tweets_df['username'] = v[x]

            tweets_df_total = pd.concat([tweets_df_total , tweets_df] , axis=0)
            print(f'Api: {k} , {v[x]}: {datetime.date.today()} - {datetime.datetime.now().strftime("%H:%M:%S")}  Nº tweets: {tweets_df.shape[0]}')


    tweets_df_total.columns = ['created_at' , 'tweet_id' , 'Tweet_Content' , 'name' , 'user_id' , 'user_followers' ,
                               'user_location' , 'source' ,'entities' , 'reply_user_id' , 'reply_status_id' ,
                               'Tweet_Number_of_Likes' ,'Tweet_Number_of_Retweets' , 'username']

    sum=tweets_df_total['username'].value_counts().sum()
    print(f'\n\n Total tweets: {sum}')

    value=pd.DataFrame(tweets_df_total['username'].value_counts())
    value['Percentage']=value['username']/value['username'].sum()
    value.style.format({'Percentage': '{:,.0%}'.format})
    print(f'\n\n{value}')


    tweets_df_total['GRUPO'] = ''

    tweets_df_total.loc[tweets_df_total['username'] == '@vodafone_es' , 'GRUPO'] = 'Vodafone'
    tweets_df_total.loc[tweets_df_total['username'] == '@Lowi_es' , 'GRUPO'] = 'Vodafone'
    tweets_df_total.loc[tweets_df_total['username'] == '@vodafoneyu' , 'GRUPO'] = 'Vodafone'
    tweets_df_total.loc[tweets_df_total['username'] == '@movistar_es' , 'GRUPO'] = 'Movistar'
    tweets_df_total.loc[tweets_df_total['username'] == '@TuentiES' , 'GRUPO'] = 'Movistar'
    tweets_df_total.loc[tweets_df_total['username'] == '@o2es' , 'GRUPO'] = 'Movistar'
    tweets_df_total.loc[tweets_df_total['username'] == '@orange_es' , 'GRUPO'] = 'Orange'
    tweets_df_total.loc[tweets_df_total['username'] == '@jazztel_es' , 'GRUPO'] = 'Orange'
    tweets_df_total.loc[tweets_df_total['username'] == '@Amena' , 'GRUPO'] = 'Orange'
    tweets_df_total.loc[tweets_df_total['username'] == '@simyo_es' , 'GRUPO'] = 'Orange'
    tweets_df_total.loc[tweets_df_total['username'] == '@masmovil' , 'GRUPO'] = 'Masmovil'
    tweets_df_total.loc[tweets_df_total['username'] == '@pepephone' , 'GRUPO'] = 'Masmovil'
    tweets_df_total.loc[tweets_df_total['username'] == '@yoigo' , 'GRUPO'] = 'Masmovil'

    value_group=pd.DataFrame(tweets_df_total['GRUPO'].value_counts())
    value_group['Percentage']=value_group['GRUPO']/value_group['GRUPO'].sum()
    value_group.style.format({'Percentage': '{:,.0%}'.format})
    print(f'\n\n{value_group}')

    tweets_df_total['API'] = ''

    tweets_df_total.loc[tweets_df_total['username'] == '@vodafone_es' , 'API'] = 'api'
    tweets_df_total.loc[tweets_df_total['username'] == '@Lowi_es' , 'API'] = 'api3'
    tweets_df_total.loc[tweets_df_total['username'] == '@vodafoneyu' , 'API'] = 'api'
    tweets_df_total.loc[tweets_df_total['username'] == '@movistar_es' , 'API'] = 'api3'
    tweets_df_total.loc[tweets_df_total['username'] == '@TuentiES' , 'API'] = 'api3'
    tweets_df_total.loc[tweets_df_total['username'] == '@o2es' , 'API'] = 'api2'
    tweets_df_total.loc[tweets_df_total['username'] == '@orange_es' , 'API'] = 'api3'
    tweets_df_total.loc[tweets_df_total['username'] == '@jazztel_es' , 'API'] = 'api3'
    tweets_df_total.loc[tweets_df_total['username'] == '@Amena' , 'API'] = 'api2'
    tweets_df_total.loc[tweets_df_total['username'] == '@simyo_es' , 'API'] = 'api'
    tweets_df_total.loc[tweets_df_total['username'] == '@masmovil' , 'API'] = 'api2'
    tweets_df_total.loc[tweets_df_total['username'] == '@pepephone' , 'API'] = 'api'
    tweets_df_total.loc[tweets_df_total['username'] == '@yoigo' , 'API'] = 'api2'

    value_API=pd.DataFrame(tweets_df_total['API'].value_counts())
    value_API['Percentage']=value_API['API']/value_API['API'].sum()
    value_API.style.format({'Percentage': '{:,.0%}'.format})
    print(f'\n\n{value_API}')

    # desired_width = 320
    # pd.set_option('display.width' , desired_width)
    # pd.set_option('display.max_columns' , 14)
    print(tweets_df_total['tweet_id'])
    print(tweets_df_total['reply_user_id'])
    print(tweets_df_total['reply_status_id'])
    print(tweets_df_total.info(memory_usage='deep'))

    tweets_df_total['reply_user_id'].fillna('no', inplace=True)
    tweets_df_total['reply_status_id'].fillna('no' , inplace=True)

    tweets_df_total['tweet_id'] = tweets_df_total['tweet_id'].astype('str')
    tweets_df_total['user_id'] = tweets_df_total['user_id'].astype('str')
    tweets_df_total['reply_user_id'] = tweets_df_total['reply_user_id'].astype('str')
    tweets_df_total['reply_status_id'] = tweets_df_total['reply_status_id'].astype('str')

    tweets_df_total['user_location'] = tweets_df_total['user_location'].astype('str')
    tweets_df_total['source'] = tweets_df_total['source'].astype('str')
    tweets_df_total['user_followers'] = tweets_df_total['user_followers'].astype('int64')
    tweets_df_total['Tweet_Number_of_Likes'] = tweets_df_total['Tweet_Number_of_Likes'].astype('int64')
    tweets_df_total['Tweet_Number_of_Retweets'] = tweets_df_total['Tweet_Number_of_Retweets'].astype('int64')
    tweets_df_total['Tweet_Content'] = tweets_df_total['Tweet_Content'].astype('str')
    tweets_df_total['name'] = tweets_df_total['name'].astype('str')
    tweets_df_total['entities'] = tweets_df_total['entities'].astype('str')
    tweets_df_total['username'] = tweets_df_total['username'].astype('str')
    tweets_df_total['GRUPO'] = tweets_df_total['GRUPO'].astype('str')
    tweets_df_total['API'] = tweets_df_total['API'].astype('str')

    print(tweets_df_total['tweet_id'])
    print(tweets_df_total['reply_user_id'])
    print(tweets_df_total['reply_status_id'])
    print(tweets_df_total.info(memory_usage='deep'))


    # sqlitedb_path = '/home/carpiero/ir/Database/twitter.db'
    # engine = create_engine(f'sqlite:///{sqlitedb_path}' , echo=True)

    user = cfg['ssh']['username']
    passw = cfg['ssh']['password']
    engine = create_engine(f'postgresql://{user}:{passw}@localhost/carpiero' , echo=True)
    postgresql_connection = engine.connect()

    postgresql_table = "twitter_operators"
    tweets_df_total.to_sql(postgresql_table, postgresql_connection, if_exists='append',index=False,
               # dtype={'tweet_id': sqlalchemy.types.VARCHAR(length=255),'user_id': sqlalchemy.types.VARCHAR(length=255)}
                           )


    # tweets_df_total.to_csv(f'./Row_data/tweets_df_total.csv')


    df_postgresql = pd.read_sql_query("SELECT * FROM twitter_operators", engine, coerce_float=True, parse_dates=['created_at'])
    dias=df_postgresql[['created_at']].resample('D', on='created_at').count()
    print(f'\n\n{dias}')

    print(f'\n\nFinish Update Day: {since}\n\n{datetime.date.today()} - {datetime.datetime.now().strftime("%H:%M:%S")}\n\n')


if __name__ == "__main__":
    update_twitter_database()





