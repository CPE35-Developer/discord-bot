from src.utils.member import getNick
import discord


def formatCode_emb(msg: discord.Message, language: str, sourcecode: str):
    if len(sourcecode) >= 1021:
        SCsplit = sourcecode.split('\n')
        SCsplitratio = -(-len(sourcecode)//1024)+1
        SCsplitind = len(SCsplit)//SCsplitratio
        SClist = []
        for i in range(1, SCsplitratio+1):
            print(i-1, i)
            SClist.append(SCsplit[SCsplitind*(i-1):SCsplitind*(i)])
        return SClist

    else:
        pfp = msg.author.avatar_url
        embed = discord.Embed('')
        embed.set_thumbnail(url=pfp)
        embed.add_field(
            name='Code', value=f"""By {getNick(msg.author)}```{language}\n{sourcecode}\n```""")
        return embed


def formatCode(msg: discord.Message, language: str, sourcecode: str):
    if len(sourcecode) >= 2000:
        SCsplit = sourcecode.split('\n')
        SCsplitratio = -(-len(sourcecode)//2000)
        SCsplitind = len(SCsplit)//SCsplitratio
        SClist = []
        for i in range(1, SCsplitratio+1):
            SClist.append(SCsplit[SCsplitind*(i-1):SCsplitind*(i)])
        return SClist

    else:
        return f"""By {getNick(msg.author)}```{language}\n{sourcecode}\n```"""
