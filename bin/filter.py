import zipfile
import argparse
import json
import csv

def process(args):
    process.total = 0
    process.direct = 0
    process.sample = set(args.sample.read().split())
    process.csv = open('data/twitter/tweets.csv', 'w+')
    fieldnames = ['id_str', 'reply_to', 'text']
    process.writer = csv.DictWriter(process.csv, fieldnames=fieldnames)
    process.writer.writeheader()
    with zipfile.ZipFile(args.file) as z:
        for name in z.namelist()[1:]:
            process_file(z, name)
    print('total', process.total)
    print('direct', process.direct)
    process.csv.close()

def process_file(z, name):
    with z.open(name) as fp:
        for line in fp:
            process_line(line)

def process_line(line):
    tweet = json.loads(line)
    process.total += 1
    reply_to = tweet.get('in_reply_to_screen_name', None)
    if reply_to not in process.sample:
        return
    process.direct += 1
    id_str = tweet['id_str']
    if 'extended_tweet' in tweet:
        text = repr(tweet['extended_tweet']['full_text'])[1:-1]
    else:
        text = repr(tweet['text'])[1:-1]
    row = dict(id_str=id_str, reply_to=reply_to, text=text)
    process.writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="input filename")
    parser.add_argument('sample', type=open, help='screen_name samples file')
    args = parser.parse_args()
    process(args)



