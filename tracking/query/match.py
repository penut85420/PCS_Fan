import re
import os
import string
import argparse
from ..utils import load
from ..riots import get_match

def main(name, show_only=False, server='euw1'):
    _load = lambda f: load(os.path.join('data', f))
    idx_rn2sn = _load('rn2sn.json')
    idx_sn2rn = _load('sn2rn.json')
    champs = _load('champs.json')
    players = _load('players.json')
    team_short = _load('short.json')
    role_map = _load('role_map.json')

    summoner_names = idx_rn2sn[name]
    for sn in summoner_names:
        match = get_match(sn, server=server)
        if match is None:
            print(f'{name} ({sn}) not fount or not in game')
            continue

        team_side = {100: [], 200: []}
        for participant in match['participants']:
            summoner_names = participant['summonerName']
            if summoner_names in idx_sn2rn:
                champ_id = str(participant['championId'])
                realname = idx_sn2rn[summoner_names]
                player_info = players[realname.lower()]
                team, role = player_info['team'], player_info['role']
                team = team_short.get(team, team)
                if len(team) > 5:
                    team = short_team_fn(team)
                role = role_map.get(role, role)

                if show_only:
                    info_str = f'{team} {realname} ({champs[champ_id]})'.strip()
                else:
                    info_str = f'{team} {realname} ({role}) - {champs[champ_id]}'.strip()
                team_side[participant['teamId']].append(info_str)

        if show_only:
            _join = lambda x: ' & '.join(x)
            blue = _join(team_side[100]) if team_side[100] else ''
            red = _join(team_side[200]) if team_side[200] else ''

            if blue and red:
                blue = f'[藍] {blue}'
                red = f'[紅] {red}'

            show_info = f'{blue} {red}'.strip()
            print(show_info)
        else:
            template = open('data/players.html.template', 'r', encoding='UTF-8').read()
            seg = '\n                '
            front_blue = '<tr><td class="squad blue">'
            front_red = '<tr><td class="squad red">'
            end = '</td></tr>'
            blue = [f'{front_blue}{p}{end}' for p in team_side[100]]
            red = [f'{front_red}{p}{end}' for p in team_side[200]]
            all_players = seg.join(blue + red)
            html = template.replace('[@@PLAYERS@@]', all_players)
            open('obs/players.html', 'w', encoding='UTF-8').write(html)
            print(f'Match of {name} Done!')

def short_team_fn(team):
    ucase = set(string.ascii_uppercase)
    team_set = set(team)
    if ucase - team_set == ucase:
        team = team.title()
    return ''.join(re.findall('[A-Z0-9]', team))[:3]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--display', '-d', action='store_true')
    parser.add_argument('name')
    parser.add_argument('--server', '-s', required=False, default='euw1')
    args = parser.parse_args()

    main(args.name, args.display, args.server)
