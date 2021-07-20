from src.utils.member import getNick
import discord
async def formatCode_emb(msg:discord.Message, language:str, sourcecode:str):
    if len(sourcecode) >= 1021:
        SCsplit = sourcecode.split('\n')
        SCsplitratio = -(-len(sourcecode)//1024)+1
        SCsplitind = len(SCsplit)//SCsplitratio
        SClist = []
        for i in range(1,SCsplitratio+1):
            print(i-1, i)
            SClist.append(SCsplit[SCsplitind*(i-1):SCsplitind*(i)])
        SCfst = '\n'.join(SClist[0])
        pfp = msg.author.avatar_url
        embed=discord.Embed()
        embed.set_thumbnail(url=pfp)
        embed.add_field(name='Code', value=f"""By {getNick(msg.author)}```{language}\n{SCfst}\n```""")
        await msg.channel.send(embed=embed)
        for count, code in enumerate(SClist[1:],start=1):
            SCrest = '\n'.join(code)
            embed=discord.Embed()
            embed.add_field(name = f'#continue {count}', value=f"""```{language}\n{SCrest}\n```""")
            await msg.channel.send(embed=embed)
              
    else:
        pfp = msg.author.avatar_url
        embed=discord.Embed()
        embed.set_thumbnail(url=pfp)
        embed.add_field(name='Code', value=f"""By {getNick(msg.author)}```{language}\n{sourcecode}\n```""")
        await msg.channel.send(embed=embed)
        

async def formatCode(msg:discord.Message, language:str, sourcecode:str):
    await msg.channel.send(f"""By {getNick(msg.author)}```{language}\n{sourcecode}\n```""")