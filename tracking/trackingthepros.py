import re
import sys
import shutil
import requests
import datetime as dt
from collections import OrderedDict
from .utils import dump, get_json

def get_rnsn_idx():
    url = 'https://www.trackingthepros.com/d/list_players'
    player_list = get_json(url)

    # rn = Real Name, e.g. Faker
    # sn = Summoner Name, e.g. Hide on bush
    rn2sn, sn2rn = {}, {}
    length = len(player_list['data'])

    for i, data in enumerate(player_list['data']):
        pid, rn = data['DT_RowId'], data['plug']
        print(f'{i + 1}/{length} - {rn:50s}', end='\r')
        url = (
            f'https://www.trackingthepros.com/'
            f'd/pro_feed?player_id={pid}&type[]=soloq'
        )

        card_data = get_json(url)['data']
        s_names = {d['card_data']['account_name'] for d in card_data}
        rn2sn[rn] = list(s_names)
        for s_name in s_names:
            sn2rn[s_name] = rn

    dump(rn2sn, 'data/rn2sn.json')
    dump(sn2rn, 'data/sn2rn.json')

def get_player_list():
    url = 'https://www.trackingthepros.com/d/list_players'
    data = get_json(url)

    def parse(d):
        team = d['team_plug']
        name = d['plug']
        pos = d['role']
        return {
            'team': team,
            'name': name,
            'role': pos,
        }

    data = {d['plug'].lower(): parse(d) for d in data['data']}
    dump(data, 'data/players.json')

def get_spec_list(focus=[], important=[]):
    url = 'https://www.trackingthepros.com/d/list_players?filter_online=1'
    data = get_json(url)
    group = OrderedDict()

    for d in data['data']:
        name = d['name']
        name = re.search('\/\'>(.*)<', name).group(1)
        gid = d['gameID']
        tmp = group.get(gid, {'online': '', 'players': list()})
        tmp['players'].append(name)
        tmp['online'] = d['onlineNum']
        group[gid] = tmp

    group = OrderedDict(sorted(group.items(), key=lambda x: x[1]['online']))

    found = set()
    with open('data/spec.tmp', 'w', encoding='UTF-8') as f:
        ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f' Last Updated: {ts}\n')
        print(f'Last Updated: {ts}')
        ansi = lambda color, s: f'\033[1;{color}m{s}\033[0m'
        for gid in group:
            _gid = gid
            for i, name in enumerate(group[gid]['players']):
                if name in focus:
                    found.add(name)
                    _gid = ansi(33, gid)
                    group[gid]['players'][i] = ansi(33, name)

            for i, name in enumerate(group[gid]['players']):
                if name in important:
                    _gid = ansi(32, gid)
                    group[gid]['players'][i] = ansi(32, name)

            players_str = ', '.join(sorted(group[gid]['players']))
            _gid = ''
            f.write(f' {_gid} {group[gid]["online"]:3d}m {players_str}\n')
            players_str = players_str.lower()

    if found:
        print(f'{", ".join(found)} Found!')
    shutil.move('data/spec.tmp', 'data/spec.txt')

def get_spec_cmd(gid):
    url = f'https://www.trackingthepros.com/s/spectate_info?id={gid}'
    r = requests.get(url)
    return r.text[45:] + ' "-Locale=zh_TW"'

def get_game_id(name):
    _name = name.lower()
    url = 'https://www.trackingthepros.com/d/list_players?filter_online=1'
    data = get_json(url)

    for d in data['data']:
        if d['plug'].lower() == _name:
            return d['gameID']

    print(f'{name} not found')
