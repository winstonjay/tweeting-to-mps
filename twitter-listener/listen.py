'''
listen.py :

listens for tweets mentioning the 300 most followed mps
and writes each tweet as a line in a file in blocks of 5000.
'''
import os
import json
import random
import argparse
from datetime import datetime
from typing import io

import tweepy

# load env variables — make sure they are set!
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

def main():
    args = parse_args()
    # setup api and auth
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    # load sample and init listener
    sample = set(args.mp_file.read().split())
    listener = StreamListener(sample, args.epoch, args.out)
    # init stream with our initialized listener
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    terms = format_query(sample)
    stream.filter(track=[terms])


class StreamListener(tweepy.StreamListener):
    'overide tweepy.StreamListener to run custom stream actions'

    def __init__(self, sample, epoch=5000, root='data/'):
        super(StreamListener, self).__init__()
        self.sample = sample
        self.root = root
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        self.epoch = epoch
        self.i = 0
        self.fp = None
        self.next_epoch()
        print(self.sample)

    def on_status(self, status: tweepy.Status):
        'method triggered when we receive a tweet'
        # don't retweets
        if status.retweeted or 'RT @' in status.text:
            return
        # we only want the tweets that are in direct response to an mp
        if status.in_reply_to_screen_name not in self.sample:
            return
        # create new file if epoch limit is reached
        if self.i >= self.epoch:
            self.next_epoch()
        # write tweet as json str to file
        print(json.dumps(status._json), file=self.fp)
        self.i += 1

    def on_error(self, status_code: int):
        'method triggered when we receive an error'
        if status_code in (420, 413):
            # returning False in on_error disconnects the stream
            return False

    def next_epoch(self):
        'change the current file we are writing to'
        if self.fp is not None:
            self.fp.close()
        self.i = 0
        self.fp = self.new_file()

    def new_file(self) -> io:
        'return a new timestamped file to write to'
        dt = datetime.now().strftime('%Y-%m-%dT%H%M.ndjson')
        path = os.path.join(self.root, dt)
        return open(path, 'w+')


def format_query(screen_names: set) -> str:
    'format set of mp screen_names into twitter api query'
    names = ','.join(screen_names)
    return f'{names} -filter:retweets'

def parse_args():
    parser = argparse.ArgumentParser('Twitter Stream Listener')
    # data/mp/mp_list.json or mp_list.json
    parser.add_argument(
        'mp_file',
        type=open,
        help='json file listing all mps')
    parser.add_argument(
        '--epoch',
        '-n',
        type=int,
        help='number of tweets per file',
        default=5000)
    parser.add_argument(
        '--out',
        '-o',
        type=str,
        help='dir to write files to',
        default='data/')
    return parser.parse_args()


if __name__ == '__main__':
    main()