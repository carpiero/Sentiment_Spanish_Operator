import tweepy

def update_twitter_profile():


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
    api = tweepy.API(auth)

    try:
        user = api.me()
        print(f"Autenticado como: {user.name}")
    except tweepy.TweepError as e:
        print(f"Error: {e}")

    try:
        for tweet in tweepy.Cursor(api.search, q="@vodafone_es", result_type='recent').items(5):
            print(tweet.text)
    except tweepy.TweepError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    update_twitter_profile()