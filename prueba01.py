import tweepy
import pandas as pd
import numpy as np
import datetime
import configparser

from ast import literal_eval
import json
import re
#
# def hashtags(x):
#     return x['hashtags']
#
# def urls(x):
#     if len(x['urls'])>0:
#         return x['urls'][0]['url']
#     else:
#         return 'no url'
#
# def rem_stars(x):
#     m=re.sub('stars|star','',x)
#     return int(m)

def update_twitter_database():
    # cfg = configparser.RawConfigParser()
    # cfg.read('/home/carpiero/ir/pass_projects/pass.ini')

    CK= 'PGgm3YAUdzOdxhCtbgY8EvEiJ'
    CS= 'bw6ABYOaWSycv93R8DSTUvcSzGJMm0mr1iCW6xTBzaYbgXnCE4'
    AT= '302782694-rjDqqWGeejA5FRX7lANQlDUSyuj2V7zMEIbchx9Y'
    AS= 'xUtocRo69ShN6DM97isC5PP3s2uUlOCM4NQ5O0vJtytDu'

    CONSUMER_KEY = CK
    CONSUMER_SECRET = CS
    ACCESS_TOKEN = AT
    ACCESS_SECRET = AS

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=5,retry_delay=5)

    apis_username = {api: ['@vodafone_es' , '@vodafoneyu' , '@simyo_es' , '@pepephone','@yoigo' , '@o2es' , '@masmovil' , '@Amena','@orange_es' , '@movistar_es' , '@Lowi_es' , '@TuentiES' , '@jazztel_es'] ,
                     # api2: ['@yoigo' , '@o2es' , '@masmovil' , '@Amena'] ,
                     # api3: ['@orange_es' , '@movistar_es' , '@Lowi_es' , '@TuentiES' , '@jazztel_es'],
                     }

    count = 2

    today = datetime.date.today()
    yest = today - datetime.timedelta(days=1)
    since=yest
    until=today
    print(f'Until: {until}')
    print(f'Since: {since}')

    tweets_df_total = pd.DataFrame()

    for k , v in apis_username.items():
        for x in range(len(v)):

            # for x in username:
            # Creation of query method using parameters
            #     tweets = tweepy.Cursor(api.user_timeline,id=username, since=date_since, until=date_until).items(count)

            tweets = tweepy.Cursor(k.search, q=v[x], since=since, until=until, result_type='recent').items(count)
            print(v[x])
            print(tweets)

            # tweets_list = [[tweet.created_at, tweet.id_str, tweet.text, tweet.user.name, tweet.user.id_str,
            #                 tweet.user.followers_count,
            #                 tweet.user.location, tweet.source, tweet.entities,
            #                 tweet.in_reply_to_user_id_str, tweet.in_reply_to_status_id_str,
            #                 tweet.favorite_count, tweet.retweet_count] for tweet in tweets]

            try:
                for tweet in tweets:
                    print(tweet)
            except tweepy.TweepError as e:
                print(f"Error al obtener tweets: {e}")

            tweets_list = []

            # for tweet in tweets:
            #     print(tweet)
                # try:
                #     tweet_data = [
                #         tweet.created_at,
                #         tweet.id_str,
                #         tweet.text,
                #         tweet.user.name,
                #         tweet.user.id_str,
                #         tweet.user.followers_count,
                #         tweet.user.location,
                #         tweet.source,
                #         tweet.entities,
                #         tweet.in_reply_to_user_id_str,
                #         tweet.in_reply_to_status_id_str,
                #         tweet.favorite_count,
                #         tweet.retweet_count
                #     ]
                #     tweets_list.append(tweet_data)
                #     print(len(tweets_list))
                # except tweepy.TweepError as e:
                #     print(f"Error with tweet ID {tweet.id_str}: {e}")

            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet information
        #     tweets_df = pd.DataFrame(tweets_list)
        #
        #     if len(tweets_df) == 0:
        #         pass
        #     else:
        #         tweets_df['username'] = v[x]
        #
        #     tweets_df_total = pd.concat([tweets_df_total, tweets_df], axis=0)
        #     print(
        #         f'Api: {k} , {v[x]}: {datetime.date.today()} - {datetime.datetime.now().strftime("%H:%M:%S")}  Nº tweets: {tweets_df.shape[0]}')
        #
        # tweets_df_total.columns = ['created_at', 'tweet_id', 'Tweet_Content', 'name', 'user_id', 'user_followers',
        #                            'user_location', 'source', 'entities', 'reply_user_id', 'reply_status_id',
        #                            'Tweet_Number_of_Likes', 'Tweet_Number_of_Retweets', 'username']
        #
        # sum = tweets_df_total['username'].value_counts().sum()
        # print(f'\n\n Total tweets: {sum}')




if __name__ == "__main__":
    update_twitter_database()