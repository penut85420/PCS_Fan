import os
import urllib.parse
from .utils import get_json

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
