import json
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
