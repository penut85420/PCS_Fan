import os
import urllib.parse
from .utils import get_json, load, short_team_fn

def get_match(name, server='euw1'):
    # Get Summonor Info
    name = urllib.parse.quote(name)
    api_key = os.getenv('RIOT_API_KEY')

    url = (
        f'https://{server}.api.riotgames.com/'
        f'lol/summoner/v4/summoners/by-name/'
        f'{name}?api_key={api_key}'
    )

    try:
        result = get_json(url)
    except:
        return None

    uuid = result['id']

    # Get Match Info
    url = (
        f'https://{server}.api.riotgames.com/'
        f'lol/spectator/v4/active-games/by-summoner/'
        f'{uuid}?api_key={api_key}'
    )

    try:
        return get_json(url)
    except:
        return None

def get_match_by_match_id(match_id, server='euw1'):
    api_key = os.getenv('RIOT_API_KEY')
    url = (
        f'https://{server}.api.riotgames.com/'
        f'lol/match/v4/matches/'
        f'{match_id}?api_key={api_key}'
    )

    try:
        match = get_json(url)
    except:
        return None

    for p1, p2 in zip(match['participantIdentities'], match['participants']):
        p2['summonerName'] = p1['player']['summonerName']

    return match

def get_pros_match(name, server='euw1'):
    name = name.lower()
    players = load('data/players.json')
    player_info = players.get(name, None)

    if player_info is None:
        return False, name, 1, 'No Player'

    name = player_info['name']
    rn2sn = load('data/rn2sn.json')

    for sn in rn2sn[name]:
        match = get_match(sn, server)

        if match is None:
            continue

        team_side = get_pros_match_team(match)

        return True, name, 0, team_side

    return False, name, 2, 'No Match'

def get_pros_match_team(match):
    players = load('data/players.json')
    sn2rn = load('data/sn2rn.json')
    team_short = load('data/short.json')
    role_map = load('data/role_map.json')
    champs = load('data/champs.json')

    team_side = {100: [], 200: []}
    for participant in match['participants']:
        summoner_names = participant['summonerName']
        if summoner_names in sn2rn:
            champ_id = str(participant['championId'])
            realname = sn2rn[summoner_names]
            player_info = players[realname.lower()]
            team, role = player_info['team'], player_info['role']
            _team = team_short.get(team, team)
            team = team if _team == '' else _team
            if len(team) > 5:
                team = short_team_fn(team)
            role = role_map.get(role, role)

            info_str = f'{team} {realname} ({champs[champ_id]})'.strip()
            team_side[participant['teamId']].append(info_str)

    team_side[100].sort()
    team_side[200].sort()

    return team_side
