from difflib import SequenceMatcher

commands = ['$hello', '$poker', '$voice', '$disconnect']

async def guess_command(client, message):
    similar_commands = []
    if (message.content.startswith('$')) & (message.content.split()[0] not in commands):
        print(f'{message.author}: {message.content}')
        for command in commands:
            similar_ratio = SequenceMatcher(
                None, message.content, command).ratio()
            if similar_ratio >= 0.6:
                similar_commands.append([command, similar_ratio])
        similar_commands = sorted(
            similar_commands, key=lambda l: l[1], reverse=True)
        await message.channel.send(f'คุณกำลังจะพิมพ์ {similar_commands[0][0]} หรือเปล่า')
