import re
from .utils import dump, get_json, get_txt
from collections import OrderedDict

def get_en_zh_champs():
    p1 = re.compile(r'name:\"([^A-Z]+?)\"')
    p2 = re.compile(r'id:\"([A-Za-z]+?)\"')
    url = 'https://lol.garena.tw/champions'
    txt = get_txt(url)
    result = [f'{b} {a}' for a, b in zip(p1.findall(txt), p2.findall(txt))]

    dump(result, 'data/champions_enzh.json')

def get_id2champs(version='11.9.1', lang = 'zh_TW'):
    url = (
        f'https://ddragon.leagueoflegends.com/'
        f'cdn/{version}/data/{lang}/champion.json'
    )

    data = {int(val['key']): val['name'] for val in get_json(url)['data'].values()}
    data = OrderedDict(sorted(data.items(), key=lambda x: x[0]))

    dump(data, 'data/champs.json')
