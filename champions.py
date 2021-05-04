import re
import requests
import penut.io as pio

def main():
    p1 = re.compile(r'name:\"([^A-Z]+?)\"')
    p2 = re.compile(r'id:\"([A-Za-z]+?)\"')
    url = 'https://lol.garena.tw/champions'
    txt = requests.get(url).text
    result = [f'{b} {a}' for a, b in zip(p1.findall(txt), p2.findall(txt))]
    pio.dump(result, 'champions.json')

if __name__ == '__main__':
    main()
