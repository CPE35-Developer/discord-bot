import discord, discord_slash
import json, os

PATH_GUILDDATA = 'src/utils/guild.json'

async def codeChannelCheck(ctx:discord_slash.SlashContext):
    with open(PATH_GUILDDATA, 'r+') as f:
        allGuildData = json.load(f)
        
    GUILD_ID = str(ctx.guild_id)
    codeChannels = allGuildData[GUILD_ID]['codechannels']
    
    if codeChannels == []:
        em = discord.Embed(title=f"This server doesn't have any code channel yet", description=f"Add code channel by using /set codechannel set [channel] [language]", color=0x3d5bc7)
    else:
        em = discord.Embed(title=f"Code Channel(s) in {ctx.guild.name}", color=0x3d5bc7)
        for codechannel in codeChannels:
            channel = discord.utils.get(ctx.guild.channels, id=codechannel[0])
            channelName = channel.name
            em.add_field(name=channelName, value=codechannel[1], inline=True)
    
    return await ctx.send(embed=em)
 
 
async def codeChannelAdd(ctx:discord_slash.SlashContext, channel:discord.TextChannel, language:str):
    with open(PATH_GUILDDATA, 'r+') as f:
        allGuildData = json.load(f)
        
    GUILD_ID = str(ctx.guild_id)
    CHANNEL_ID = channel.id
    
    codeChannels = allGuildData[GUILD_ID]['codechannels']
    
    if CHANNEL_ID in [a[0] for a in codeChannels]:
        codeChannel = codeChannels[[a[0] for a in codeChannels].index(channel.id)]
        if codeChannel[1] == language:
            await ctx.send(f"{channel.mention} เป็น Code Channel ภาษา {language} อยู่แล้ว")
        else:
            botmsg = await channel.fetch_message(codeChannels[[a[0] for a in codeChannels].index(channel.id)][2])
            await botmsg.delete()
            

            em = discord.Embed(title=f'{channel.name}')
            em.add_field(name="Programming Language:", value=f"{language}")
            botmsg = await channel.send(embed=em)
            await botmsg.pin()
            
            codeChannels[[a[0] for a in codeChannels].index(channel.id)][1] = language
            codeChannels[[a[0] for a in codeChannels].index(channel.id)][2] = botmsg.id
            allGuildData[str(ctx.guild_id)]['codechannels'] = codeChannels
            
            await ctx.send(f"แก้ไขให้ {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")
 
    else:
        em = discord.Embed(title=f'{channel.name}')
        em.add_field(name="Programming Language:", value=f"{language}")
        botmsg = await channel.send(embed=em)
        await botmsg.pin()
        
        codeChannels.append([CHANNEL_ID, language, botmsg.id])
        allGuildData[GUILD_ID]['codechannels'] = codeChannels
        await ctx.send(f"เพิ่ม {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")
    
    os.remove(PATH_GUILDDATA)
    with open(PATH_GUILDDATA, 'w') as f:
        json.dump(allGuildData, f, indent=4)
    
    
async def codeChannelRemove(ctx:discord_slash.SlashContext, channel:discord.TextChannel):
    with open('src/utils/guild.json', 'r+') as f:
        allGuildData = json.load(f)
        
    GUILD_ID = str(ctx.guild_id)
    CHANNEL_ID = channel.id
    codeChannels = allGuildData[GUILD_ID]['codechannels']
    if CHANNEL_ID in [a[0] for a in codeChannels]:
        codeChannels = allGuildData[str(GUILD_ID)]['codechannels']
        codeChannels.pop([a[0] for a in codeChannels].index(CHANNEL_ID))
        allGuildData[str(GUILD_ID)]['codechannels'] = codeChannels
        await ctx.send(f"ลบ {channel.mention} จาก Code Channels แล้ว")
    else:
        await ctx.send(f"{channel.mention} ไม่ได้เป็น Code Channel อยู่แล้ว")
        
    os.remove(PATH_GUILDDATA)
    with open(PATH_GUILDDATA, 'w') as f:
        json.dump(allGuildData, f, indent=4)