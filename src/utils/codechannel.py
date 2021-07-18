import discord
import discord_slash
from discord.utils import get
import os
import boto3
from dotenv import load_dotenv
load_dotenv()
AWS_ACCCESSKEY = os.getenv('AWS_ACCCESSKEY')
AWS_SECRETKEY = os.getenv('AWS_SECRETKEY')
AWS_REGION = os.getenv('AWS_REGION')
session = boto3.Session(aws_access_key_id=AWS_ACCCESSKEY,
                        aws_secret_access_key=AWS_SECRETKEY, region_name=AWS_REGION)
dynamodb = session.resource('dynamodb')


class table:
    Guilds = dynamodb.Table('guilds')



GuildsData = table.Guilds.scan()['Items']
isUpdated = False

def updateTable(table_name:table, item:dict):
    global isUpdated
    isUpdated = True
    
    table_name.put_item(Item=item)

class GuildData:
    def __init__(self, GUILD_ID):
        
        global isUpdated
        global GuildsData
        
        if isUpdated:
            isUpdated = False
            GuildsData = table.Guilds.scan()['Items']
        GUILD_DATA = next((item for item in GuildsData if item['guildID'] == GUILD_ID), None)
                
        self.data =  GUILD_DATA
        self.id = int(self.data['guildID'])
        self.codechannels = self.data['codechannels']
        self.codechannel_ids = [channel['channelID'] for channel in self.data['codechannels']]
        
    def channeldata(self,CHANNEL_ID):
        return [channel for channel in self.codechannels if channel['channelID'] == CHANNEL_ID][0]
            
            

async def Check(ctx: discord_slash.SlashContext):

    guilddata = GuildData(ctx.guild_id)

    if guilddata.codechannels == []:
        em = discord.Embed(title=f"This server doesn't have any code channel yet",
                           description=f"Add code channel by using /set codechannel set [channel] [language]", color=0x3d5bc7)
    else:
        em = discord.Embed(
            title=f"Code Channel(s) in {ctx.guild.name}", color=0x3d5bc7)
        for channelID in guilddata.codechannel_ids:
            channel = discord.utils.get(ctx.guild.channels, id=int(channelID))
            channelName = channel.name
            em.add_field(name=channelName, value=guilddata.channeldata(
                channelID)['lang'], inline=True)

    await ctx.send(embed=em)


async def Add(ctx: discord_slash.SlashContext, channel: discord.TextChannel, language: str):
    guilddata = GuildData(ctx.guild_id)

    CHANNEL_ID = channel.id

    if CHANNEL_ID in guilddata.codechannel_ids:
        codeChannel = guilddata.channeldata(CHANNEL_ID)
        if codeChannel['lang'] == language:
            await ctx.send(f"{channel.mention} เป็น Code Channel ภาษา {language} อยู่แล้ว")
        else:
            botmsg = await channel.fetch_message(codeChannel['botmsgID'])
            await botmsg.delete()

            em = discord.Embed(title=f'{channel.name}')
            em.add_field(name="Programming Language:", value=f"{language}")
            botmsg = await channel.send(embed=em)
            await botmsg.pin()

            codeChannel['lang'], codeChannel['botmsgID'] = language, botmsg.id
            guilddata.updatecodechannels(guilddata.channeldata(CHANNEL_ID))
            

            
            await ctx.send(f"แก้ไขให้ {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")

    else:
        em = discord.Embed(title=f'{channel.name}')
        em.add_field(name="Programming Language:", value=f"{language}")
        botmsg = await channel.send(embed=em)

        await botmsg.pin()
        guilddata.codechannels.append({{'lang': language,
                                        'channelID': channel.id,
                                        'botmsgID': botmsg.id}})
        
        guilddata.data['codechannels'] = guilddata.codechannels

        await channel.set_permissions(ctx.guild.default_role, manage_messages=True)

        await ctx.send(f"เพิ่ม {channel.mention} เป็น Code Channel ภาษา {language} แล้ว")

    updateTable(table.Guilds, guilddata.data)


async def Remove(ctx: discord_slash.SlashContext, channel: discord.TextChannel):
    guilddata = GuildData(ctx.guild_id)

    CHANNEL_ID = channel.id


    if CHANNEL_ID in guilddata.codechannel_ids:
        
        try:
            botmsg = await channel.fetch_message(guilddata.channeldata(CHANNEL_ID)['botmsgID'])
            await botmsg.delete()
        except: print("Bot couldn't find the Bot's pinned message")
        
        guilddata.codechannels = [x for x in guilddata.codechannels if not (CHANNEL_ID == x.get('channelID'))]
        guilddata.data['codechannels'] = guilddata.codechannels
        
        await channel.set_permissions(ctx.guild.default_role, manage_messages=False)
        await ctx.send(f"ลบ {channel.mention} จาก Code Channels แล้ว")

    else:
        await ctx.send(f"{channel.mention} ไม่ได้เป็น Code Channel อยู่แล้ว")

    updateTable(table.Guilds, guilddata.data)


class Permission:
    async def ManageMessage(ctx: discord_slash.SlashContext, manageable: bool, channel: discord.TextChannel = None):
        guilddata = GuildData(ctx.guild_id)
        
        if channel.id not in guilddata.codechannel_ids:
            return ctx.send(f"{channel.mention} ไม่ใช่ Code Channel")
        if channel is None:
            for codechannelID in guilddata.codechannel_ids:
                channel = discord.utils.get(
                    ctx.guild.channels, id=int(codechannelID))
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
