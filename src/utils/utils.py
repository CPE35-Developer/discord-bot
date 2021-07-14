from difflib import SequenceMatcher
from src.utils.config import Prefix
async def guess_command(bot, message, commands):
    similar_commands = []
    if message.startswith(Prefix):
        for command in commands:
            similar_ratio = SequenceMatcher(
                None, message, command).ratio()
            if similar_ratio >= 0.6:
                similar_commands.append([command, similar_ratio])
        similar_commands = sorted(
            similar_commands, key=lambda l: l[1], reverse=True)
    if similar_commands == []:
        desc = '\n'.join(commands)
        return f"คำสั่งที่เรามีคือ\n {desc}"
    else:
        return f"คุณกำลังจะพิมพ์ {Prefix}{similar_commands[0][0]} หรือเปล่า"