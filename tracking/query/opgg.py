import re
import requests
import datetime as dt
from ..utils import get_txt

def main():
    game_names = [
        'ShirakamiFubukii',
        'Icelandboy',
        'Full+C0unter',
        'Iceland+18Y',
        'Iceland+H2OMan',
        'Lucky+Heroz'
    ]

    player_id = [
        '　　上路 Hanabi',
        '　　打野 River',
        '　　中路 Maple',
        '　　下路 Doggo',
        '　　輔助 Kaiwing',
        '替補上路 Kartis'
    ]

    rank_trans = {
        'Challenger': '菁英',
        'Grandmaster': '宗師',
        'Master': '大師',
        'Diamond 1': '鑽 I',
        'LP': '分'
    }

    html = []
    for name, player in zip(game_names, player_id):
        url = f'https://euw.op.gg/summoner/userName={name}'
        txt = get_txt(url)

        m = re.search('<div class=\"TierRank\">([\w ]+)</div>', txt)
        rank = m.group(1)

        m = re.search('<span class=\"LeaguePoints\">([\w\s]+)</span>', txt, re.M)
        points = m.group(1).strip()

        row_html = (
            f'<tr><td>{player}</td>'
            f'<td>{rank}</td>'
            f'<td style="text-align: right">{points}</td></tr>'
        )

        for s in rank_trans:
            row_html = row_html.replace(s, rank_trans[s])
        html.append(row_html)

    splitter = '\n                    '
    template = open('data/rank.html.template', 'r', encoding='UTF-8').read()
    html = template.replace('[@@RANK@@]', splitter.join(html))
    original = open('obs/rank.html', 'r', encoding='UTF-8').read()

    if html != original:
        print('Rank Updated!')

    with open('obs/rank.html', 'w', encoding='UTF-8') as f:
        f.write(html)

    ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'Rank Checked: {ts}')

if __name__ == '__main__':
    main()
