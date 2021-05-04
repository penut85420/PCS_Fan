import re
import sys
import json
import time
import shutil
import requests
import datetime as dt
from collections import OrderedDict

def main():
    url = 'https://www.trackingthepros.com/d/list_players?filter_online=1'
    r = requests.get(url)
    data = json.loads(r.content)
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

    with open('spec.tmp', 'w', encoding='UTF-8') as f:
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
                f.write(f'{spec(gid)}\n')

    shutil.move('spec.tmp', 'spec.txt')

def spec(gid):
    url = f'https://www.trackingthepros.com/s/spectate_info?id={gid}'
    r = requests.get(url)
    return r.text[45:]

if __name__ == '__main__':
    main()
