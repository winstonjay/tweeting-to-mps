'''
listen.py :

listens for tweets mentioning the 300 most followed mps
and writes each tweet as a line in a file in blocks of 5000.
'''
import os
import json
import random
from datetime import datetime

import tweepy

# load env variables — make sure they are set!
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')


def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    terms = format_query(load_sample('data/mp/mp_list.json'))
    stream = tweepy.Stream(auth=api.auth, listener=StreamListener())
    stream.filter(track=[terms])


class StreamListener(tweepy.StreamListener):

    def __init__(self, root='data/', epoch=5000):
        super(StreamListener, self).__init__()
        self.i = 0
        self.fp = None
        self.root = root
        self.epoch = epoch
        self.next_epoch()

    def on_status(self, status):
        if self.i >= self.epoch:
            self.next_epoch()
        if status.retweeted or 'RT @' in status.text:
            return
        print(json.dumps(status._json), file=self.fp)
        self.i += 1

    def on_error(self, status_code):
        if status_code in (420, 413):
            # returning False in on_error disconnects the stream
            return False

    def next_epoch(self):
        if self.fp is not None:
            self.fp.close()
        self.i = 0
        self.fp = self.new_file()

    def new_file(self):
        dt = datetime.now().strftime('%Y-%m-%dT%H%M.ndjson')
        path = os.path.join(self.root, dt)
        return open(path, 'w+')


def format_query(screen_names):
    names = ','.join(name[1:] for name in screen_names)
    return f'{names} -filter:retweets'

def load_sample(filename, max_size=400):
    with open(filename) as fp:
        data = json.load(fp)
    sample = sample_most_followers(data, max_size)
    return [mp['screen_name'] for mp in sample]

def sample_random(data, n):
    return random.sample(data, n)

def sample_most_followers(data, n):
    def followers(mp):
        return mp['followers']
    return sorted(data, key=followers, reverse=True)[:n]


if __name__ == '__main__':
    main()