import os
import json
import random

import tweepy

# load env variables — make sure they are set!
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# SCREEN_NAMES = load_sample('data/mp/mp_list.json')

def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    terms = format_query(load_sample('data/mp/mp_list.json'))
    stream = tweepy.Stream(auth=api.auth, listener=StreamListener())
    stream.filter(track=[terms])


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted or 'RT @' in status.text:
            return
        print(json.dumps(status._json))

    def on_error(self, status_code):
        if status_code in (420, 413):
            # returning False in on_error disconnects the stream
            return False


def format_query(screen_names):
    names = ','.join(name[1:] for name in screen_names)
    return f'{names} -filter:retweets'

def load_sample(filename, max_sample_size=400):
    with open(filename) as fp:
        data = random.sample(json.load(fp), max_sample_size)
    return set(mp['screen_name'] for mp in data)

if __name__ == '__main__':
    main()