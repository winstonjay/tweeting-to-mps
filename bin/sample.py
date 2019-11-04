import json

def main():
    for line in load_sample('data/mp/mp_list.json'):
        print(line)

def load_sample(filename: str, max_size=400) -> set:
    'load sample of mp screen names from json file'
    with open(filename, encoding='utf-8') as fp:
        data = json.load(fp)
    sample = sample_most_followers(data, max_size)
    return set(mp['screen_name'] for mp in sample)

def sample_most_followers(data: list, n: int) -> list:
    'return top n mps by most followers'
    def followers(mp):
        return mp['followers']
    return sorted(data, key=followers, reverse=True)[:n]

if __name__ == '__main__':
    main()