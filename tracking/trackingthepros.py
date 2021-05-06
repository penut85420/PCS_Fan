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

def get_spec_list():
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

    with open('data/spec.tmp', 'w', encoding='UTF-8') as f:
        ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'Last Updated: {ts}\n')
        print(f'Last Updated: {ts}')
        for gid in group:
            players_str = ', '.join(sorted(group[gid]['players']))
            f.write(f' {gid} {group[gid]["online"]:3d}m {players_str}\n')
            players_str = players_str.lower()
            flag = False
            for name in sys.argv[1:]:
                if name.lower() in players_str:
                    print(f'Found {name}!')
                    flag = True
            if flag:
                f.write(f'{get_spec_cmd(gid)}\n')

    shutil.move('data/spec.tmp', 'data/spec.txt')

def get_spec_cmd(gid):
    url = f'https://www.trackingthepros.com/s/spectate_info?id={gid}'
    r = requests.get(url)
    return r.text[45:]
