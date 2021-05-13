import re
import json
import string
import urllib.request

def get_txt(url):
    ctx = urllib.request.urlopen(url).read()
    return ctx.decode('UTF-8')

def get_json(url):
    return json.loads(get_txt(url))

def dump(data, path):
    with open(path, 'w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load(path):
    with open(path, 'r', encoding='UTF-8') as f:
        return json.load(f)

def short_team_fn(team):
    ucase = set(string.ascii_uppercase)
    team_set = set(team)

    if ucase - team_set == ucase:
        team = team.title()

    return ''.join(re.findall('[A-Z0-9]', team))[:3]
