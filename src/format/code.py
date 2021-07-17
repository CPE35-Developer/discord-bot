from src.utils.member import getNick
import discord
def formatCode(msg:discord.Message, language:str, sourcecode:str):
    return f"""By {getNick(msg.author)}```{language}\n{sourcecode}\n```"""