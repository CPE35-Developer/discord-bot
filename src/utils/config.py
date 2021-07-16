import os
import json


class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(
                    x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)


with open('config.json', 'r') as f:
    CONFIG = obj(json.load(f))

Prefix = CONFIG.prefix
PATH_mp3 = CONFIG.audio.PATH_mp3
MP3_files = [file.replace(".mp3", "") for file in os.listdir(PATH_mp3)]
