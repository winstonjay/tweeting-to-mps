'''
getlist.py :

throwaway script for scraping mp details and twitter info
from mpsontwitter.co.uk and writing results to a json file.

usage:
    python scripts/getlist.py
'''
import json
import urllib.request

from bs4 import BeautifulSoup

MP_LIST_URL = 'https://www.mpsontwitter.co.uk/list'
MP_LIST_HTML = 'data/mp/mp_list.html'
MP_LIST_JSON = 'data/mp/mp_list.json'

# load file if we have it locally or get it from remote url
# and then save it so we don't bother then too much
try:
    with open(MP_LIST_HTML, encoding='utf-8') as fp:
        html_doc = fp.read()
    print(f'loaded from file: {MP_LIST_HTML}')
except FileNotFoundError:
    with urllib.request.urlopen(MP_LIST_URL) as res:
       html_doc = str(res.read())
    print(f'loaded from file: {MP_LIST_URL}')
    with open(MP_LIST_HTML, 'w+', encoding='utf-8') as fp:
        fp.write(html_doc)
    print(f'wrote to file: {MP_LIST_URL}')


soup = BeautifulSoup(html_doc, 'html.parser')
# --- Example tr (10 elements) ---
# <tr id="Alan Duncan Rutland and Melton" onclick="get_timeline('AlanDuncanMP' , 'Alan Duncan ', 'Rutland and Melton')">
# 	<td class="Conservative"></td>
# 	<td><span class="label label-default">2</span></td>
#   <td>Alan Duncan </td>
#   <td><a href="https://www.mpsontwitter.co.uk/mp/AlanDuncanMP">@AlanDuncanMP</a></td>
#   <td>Rutland and Melton</td>
# 	<td><a href="https://www.mpsontwitter.co.uk/archive/search?party=Conservative"><span class="badge Conservative">Conservative</span></a></td>
# 	<td>26,115</td>
#   <td><span class="tri_down">▼ </span>-6</td>
#   <td><a href="https://twitter.com/@AlanDuncanMP"><i class="fa fa-twitter fa-fw"></i></a></td>
# 	<td class="Conservative"></td>
# </tr>
mp_list = soup.find(id='mp_wrapper').find_all('tr')

data = []
data_keys = ['name', 'screen_name', 'constituency', 'party', 'followers']
for mp_row in mp_list:
    # we only want columns 2-7
    mp_data = mp_row.find_all('td')[2:7]
    mp = {k: v.text.strip() for k, v in zip(data_keys, mp_data)}
    # convert followers to a number not a string
    mp['followers'] = int(mp['followers'].replace(',', ''), base=10)
    mp['screen_name'] = mp['screen_name'][1:]
    data.append(mp)

with open(MP_LIST_JSON, 'w+') as fp:
    json.dump(data, fp, indent=2)
print(f'wrote to file: {MP_LIST_JSON}')