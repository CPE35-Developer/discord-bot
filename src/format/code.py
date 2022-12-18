from src.utils.member import getNick
import discord


def formatCode_emb(msg: discord.Message, language: str, sourcecode: str):
    if len(sourcecode) >= 1021:
        SCsplit = sourcecode.split('\n')
        SCsplitratio = -(-len(sourcecode)//1024)+1
        SCsplitind = len(SCsplit)//SCsplitratio
        SClist = []
        for i in range(1, SCsplitratio+1):
            SClist.append(SCsplit[SCsplitind*(i-1):SCsplitind*(i)])
        return SClist

    else:
        pfp = msg.author.avatar_url
        embed = discord.Embed()
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


async def send_fmc(msg: discord.Message, language: str):
    if msg.content[:2] in '-e':
        fmc = formatCode_emb(msg, language, msg.content[2:])
        if type(fmc) == list:
            SCfst = '\n'.join(fmc[0])
            pfp = msg.author.avatar_url
            embed = discord.Embed()
            embed.set_thumbnail(url=pfp)
            embed.add_field(
                name='Code', value=f"""By {getNick(msg.author)}```{language}\n{SCfst}\n```""")
            for count, code in enumerate(fmc[1:], start=1):
                SCrest = '\n'.join(code)
                embed.add_field(
                    name=f'#continue {count}', value=f"""```{language}\n{SCrest}\n```""", inline=False)
            await msg.channel.send(embed=embed)
        else:
            await msg.channel.send(embed=fmc)
    else:
        fmc = formatCode(msg, language, msg.content)
        if type(fmc) == list:
            SCfst = '\n'.join(fmc[0])
            await msg.channel.send(f"""By {getNick(msg.author)}```{language}\n{SCfst}\n```""")
            for code in fmc[1:]:
                SCline = '\n'.join(code)
                await msg.channel.send(f"""```{language}\n{SCline}\n```""")
        else:
            await msg.channel.send(formatCode(msg, language, msg.content))
