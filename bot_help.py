from difflib import SequenceMatcher

command_list = ['$hello','$poker']

async def guess_command(client, message):
    if message.content.startswith('$'):
        similar_ratio = []
        for command_name in command_list:
            ratio = SequenceMatcher(None, message.content, command_name).ratio()
            if ratio > 0.6: similar_ratio.append([command_name, ratio])
        sorted(similar_ratio, key=lambda l:l[1], reverse=True)
        try: await message.channel.send(f"หมายถึง {similar_ratio[0][0]} หรือเปล่า")
        except: pass