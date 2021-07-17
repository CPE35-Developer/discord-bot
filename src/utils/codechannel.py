import discord, discord_slash
from discord.utils import get
from discord.ext.commands import context
import json, os

from discord_slash.utils import manage_commands

PATH_GUILDDATA = 'src/utils/guild.json'
allGuildData = None

def getallGuildData(option='r+'):
    with open(PATH_GUILDDATA, option) as f:
        global allGuildData
        allGuildData = json.load(f)

def getcodeChannels(GUILD_ID:int):
        return allGuildData[str(GUILD_ID)]['codechannels']

def updateallGuildDataJSON():
        os.remove(PATH_GUILDDATA)
        with open(PATH_GUILDDATA, 'w') as f:
            json.dump(allGuildData, f, indent=4)

            
async def Check(ctx:discord_slash.SlashContext):
    getallGuildData()
    
    codeChannels = getcodeChannels(ctx.guild_id)
    
    if codeChannels == {}:
        em = discord.Embed(title=f"This server doesn't have any code channel yet", description=f"Add code channel by using /set codechannel set [channel] [language]", color=0x3d5bc7)
    else:
        em = discord.Embed(title=f"Code Channel(s) in {ctx.guild.name}", color=0x3d5bc7)
        for codechannelID in codeChannels:
            channel = discord.utils.get(ctx.guild.channels, id=int(codechannelID))
            channelName = channel.name
            em.add_field(name=channelName, value=codeChannels[codechannelID]['lang'], inline=True)
    
    await ctx.send(embed=em)


async def Add(ctx:discord_slash.SlashContext, channel:discord.TextChannel, language:str):
    getallGuildData()
        
    GUILD_ID = str(ctx.guild_id)
    CHANNEL_ID = str(channel.id)
    
    codeChannels = getcodeChannels(ctx.guild_id)        
    if CHANNEL_ID in codeChannels:
        codeChannel = codeChannels[CHANNEL_ID]
        if codeChannel['lang'] == language:
            await ctx.send(f"{channel.mention} เป็น Code Channel ภาษา {language} อยู่แล้ว")
        else:
            botmsg = await channel.fetch_message(codeChannels[CHANNEL_ID]['botmsgID'])
            await botmsg.delete()
            

            em = discord.Embed(title=f'{channel.name}')
            em.add_field(name="Programming Language:", value=f"{language}")
            botmsg = await channel.send(embed=em)
            await botmsg.pin()
            
            codeChannel['lang'], codeChannel['botmsgID'] = language, botmsg.id
            codeChannels[CHANNEL_ID] = codeChannel
            allGuildData[str(ctx.guild_id)]['codechannels'] = codeChannels
            
            await ctx.send(f"แก้ไขให้ {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")

    else:
        em = discord.Embed(title=f'{channel.name}')
        em.add_field(name="Programming Language:", value=f"{language}")
        botmsg = await channel.send(embed=em)
        
        await botmsg.pin()
        codeChannels.update({CHANNEL_ID:{'lang' :language,
                                            'botmsgID':botmsg.id}})
        allGuildData[GUILD_ID]['codechannels'] = codeChannels
        await channel.set_permissions(ctx.guild.default_role, manage_messages=True)

        await ctx.send(f"เพิ่ม {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")
    
    updateallGuildDataJSON()
    
    
async def Remove(ctx:discord_slash.SlashContext, channel:discord.TextChannel):
    getallGuildData()
        
    GUILD_ID = str(ctx.guild_id)
    CHANNEL_ID = str(channel.id)
    
    codeChannels = getcodeChannels(ctx.guild_id)
    
    if CHANNEL_ID in codeChannels:
        botmsg = await channel.fetch_message(codeChannels[CHANNEL_ID]['botmsgID'])
        await botmsg.delete()
        codeChannels.pop(CHANNEL_ID)
        allGuildData[str(GUILD_ID)]['codechannels'] = codeChannels
        await channel.set_permissions(ctx.guild.default_role, manage_messages=False)
        await ctx.send(f"ลบ {channel.mention} จาก Code Channels แล้ว")

    else:
        await ctx.send(f"{channel.mention} ไม่ได้เป็น Code Channel อยู่แล้ว")
        
    updateallGuildDataJSON()
        
        
class Permission:
    async def ManageMessage(ctx:discord_slash.SlashContext, manageable:bool ,channel:discord.TextChannel=None):
        codeChannels = getcodeChannels(ctx.guild_id)
        if str(channel.id) not in codeChannels:
            return ctx.send(f"{channel.mention} ไม่ใช่ Code Channel")
        if channel is None:
            getallGuildData()
            codeChannels = getcodeChannels(ctx.guild_id)
            for codechannelID in codeChannels:
                channel = discord.utils.get(ctx.guild.channels, id=int(codechannelID))
                if manageable:
                    await channel.set_permissions(ctx.guild.default_role, manage_messages=True)
                    await channel.send(f"สามารถลบข้อความใน Code channels ได้แล้ว")

                else:
                    await channel.set_permissions(ctx.guild.default_role, manage_messages=False)
                    await channel.send(f"ไม่สามารถลบข้อความใน Code channels ได้แล้ว")


        else: 
            if manageable:
                await channel.set_permissions(ctx.guild.default_role, manage_messages=True)
                await channel.send(f"สามารถลบข้อความใน {channel.name} ได้แล้ว")
            else:
                await channel.set_permissions(ctx.guild.default_role, manage_messages=False)
                await channel.send(f"ไม่สามารถลบข้อความใน {channel.name} ได้แล้ว")


    