import os
import json
import csv
import random

directory = './data/tweets/data/'
sample_rate = 0.4

def main():
    path = os.path.join('./data/tweets/tweets.csv')
    with open(path, 'w+', encoding='utf-8') as fp:
        main.writer = csv.DictWriter(fp, fieldnames=fields)
        main.writer.writeheader()
        main.total = 0
        process_dir(directory)
    print(f'total tweets sampled: {main.total}')

def process_dir(directory):
    for filename in os.listdir(directory):
        main.path = os.path.join(directory, filename)
        proccess_file(main.path)

def proccess_file(path):
    with open(path) as fp:
        for line in fp:
            if random.random() > sample_rate:
                continue
            process_line(line)

def process_line(line):
    try:
        raw = json.loads(line.strip())
        data = {key: raw[key] for key in fields if key != 'party'}
        if 'extended_tweet' in raw:
            data['text'] = raw['extended_tweet']['full_text']
        data['text'] = data['text'].replace('\n', ' ')
        data['party'] = party_map[data['in_reply_to_screen_name']]
        main.writer.writerow(data)
        main.total += 1
    except json.decoder.JSONDecodeError:
        print(f"Error in file: {main.path}")
        print(f'\t"{line}"')

def load_party_map():
    with open('./data/mp/mp_list.json') as fp:
        mps = json.load(fp)
    return {mp['screen_name']: mp['party'] for mp in mps}

party_map = load_party_map()

fields = ['id_str', 'created_at', 'party', 'in_reply_to_screen_name', 'text']


if __name__ == '__main__':
    main()
