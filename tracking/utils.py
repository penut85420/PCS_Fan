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

def mk_players_html(team_side, name):
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

def mk_match_info(team_side):
    _join = lambda x: ' & '.join(x)
    blue = _join(team_side[100]) if team_side[100] else ''
    red = _join(team_side[200]) if team_side[200] else ''

    if blue and red:
        blue = f'[藍] {blue}'
        red = f'[紅] {red}'

    show_info = f'{blue} {red}'.strip()

    return show_info
