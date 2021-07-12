from difflib import SequenceMatcher

import json
class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)


with open('config.json', 'r') as f:
    config = obj(json.load(f))

prefix = config.prefix

async def guess_command(client, message, commands):
    similar_commands = []
    if (message.content.startswith(prefix)) & (message.content.split()[0].replace(prefix,'') not in commands):
        print(f'{message.author}: {message.content}')
        for command in commands:
            similar_ratio = SequenceMatcher(
                None, message.content, command).ratio()
            if similar_ratio >= 0.6:
                similar_commands.append([command, similar_ratio])
        similar_commands = sorted(
            similar_commands, key=lambda l: l[1], reverse=True)
        await message.channel.send(f'คุณกำลังจะพิมพ์ {prefix}{similar_commands[0][0]} หรือเปล่า')
