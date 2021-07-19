import os
import discord
import discord_slash
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
from discord.ext import commands
from src.utils.utils import commandSuggestFromError
from src.utils.codechannel import *
from src.utils.kick import random_kick
from src.utils.travel import random_travel
from src.utils.change import change_last_message
from src.utils.config import Prefix
from src.utils.command import SlashChoice
from src.poker.poker import poker_play
from src.audio.audio import voice, say, play, disconnect
from discord_slash.utils.manage_commands import create_option
from src.format.code import formatCode
from dotenv import load_dotenv

import platform
import pkg_resources
pkg_resources.require("googletrans>=4.0.0-rc.1")

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=Prefix,
                   intents=discord.Intents.all(),
                   case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)

GUILD_IDS = None    

@bot.event
async def on_ready():
    global GUILD_IDS
    GUILD_IDS = [guild.id for guild in bot.guilds]
    GUILD_NAMES = [guild.name for guild in bot.guilds]
    
    print(GUILD_NAMES)
    me = await bot.fetch_user(186315352026644480)
    await me.send(f'Running {bot.user.name} on\n{platform.uname()}')

@bot.event
async def on_message(msg:discord.Message):
    if msg.author.bot or msg.content[0] in ['_', '*']:
        return
    
    
    if msg.guild.id not in GuildIDs:
        global GUILD_IDS
        GUILD_IDS.append(msg.guild.id)
        addGuild(msg.guild.id)
        
    channel = msg.channel
    guildCodeChannels = GuildData(msg.guild.id).codechannels
    
    if channel.id in guildCodeChannels:
        language = GuildData(msg.guild.id).channeldata[channel.id]['lang']
        await channel.send(formatCode(msg, language, msg.content))
        await msg.delete()
        return

@bot.command(name="hello", aliases=['hi', 'hoi'])
async def nine_nine(ctx):
    print(type(ctx))
    await ctx.send("HI :flushed:")


@bot.command(name="poker")
async def poker(ctx):
    await poker_play(bot, ctx)


@bot.command(name='voice', aliases=['v', 'vc'])
async def audio_voice(ctx, *, message=None):
    await voice(bot, ctx, message)


@bot.command(name='disconnect',  aliases=['exit', 'dc'])
async def audio_disconnect(ctx):
    await disconnect(bot, ctx)


@bot.command(name='snap')
async def snap_kick(ctx, user: discord.Member = None):
    await random_kick(bot, ctx, user)


@bot.command(name='travel')
async def travel_chanel(ctx, user: discord.Member = None):
    await random_travel(ctx, user)


@bot.command(name='change')
async def change_message(ctx):
    await change_last_message(ctx)
    

@bot.command(name='code', aliases=['c','format','f'])
async def formatSourceCode(ctx, *, sourcecode):
    print(f'{str(ctx.author)} used {ctx.command}')
    await ctx.send(formatCode(ctx, 'py', sourcecode))
    await ctx.message.delete()



@bot.event
async def on_command_error(ctx, error):
    await commandSuggestFromError(ctx, bot, error)


@slash.slash(name="hello", description="Say hi to the bot. Most used to check if bot is ready.", guild_ids=GUILD_IDS)
async def nine_nine(ctx:discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await ctx.send("HI :flushed:")

@slash.slash(name='invitebot',description='I will send you the authorization link, see you in your server.', guild_ids=GUILD_IDS)
async def send_botinvitelink(ctx:discord_slash.SlashContext):
    await ctx.send('https://tinyurl.com/blackhole112')

@slash.slash(name="poker", description="Play poker.", guild_ids=GUILD_IDS)
async def poker(ctx:discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await poker_play(bot, ctx)


@slash.slash(name="voice", description="Play an audio or say some thing(Text to speech)", guild_ids=GUILD_IDS,
             options=[create_option(name='message', description='The sound to play or the text for TTS',
                                    option_type=SlashCommandOptionType.STRING,
                                    required=True),

                      create_option(name='language', description='The language you want TTS to speak',
                                    option_type=SlashCommandOptionType.STRING, required=False,
                                    choices=SlashChoice.choiceVoiceLang)])
async def audio_voice(ctx:discord_slash.SlashContext, message, language=None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await voice(bot, ctx, message, language)


@slash.slash(name="say", description="Say some thing(Text to speech)", guild_ids=GUILD_IDS,
             options=[create_option(name='message',
                                    description='The sound to play or the text for TTS',
                                    option_type=SlashCommandOptionType.STRING, required=True),

                      create_option(name='language',
                                    description='The language you want TTS to speak',
                                    option_type=SlashCommandOptionType.STRING, required=False,
                                    choices=SlashChoice.choiceVoiceLang)])
async def audio_say(ctx:discord_slash.SlashContext, message, language=None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await say(bot, ctx, message, language)


@slash.slash(name="play", description="Play a sound", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='Choose a sound to play.',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceSound)])
async def audio_play(ctx:discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound)


@slash.slash(name="tu", description="ตู่", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceTuVoice)])
async def audio_play(ctx:discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)

@slash.slash(name="pom", description="ป้อม", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choicePomVoice)])
async def audio_play(ctx:discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)

@slash.subcommand(base='oneonetwo', name="o", description="112", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceOVoice)])
async def audio_play(ctx:discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)

@slash.subcommand(base='oneonetwo', name="nui", description="112", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceNuiVoice)])
async def audio_play(ctx:discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)
                  
@slash.slash(name="disconnect", description="Disconnect bot from the Voice Channel", guild_ids=GUILD_IDS)
async def audio_disconnect(ctx:discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await disconnect(bot, ctx)


@slash.slash(name="snap", description="Perfectly balanced, as all things should be", guild_ids=GUILD_IDS)
async def snap_kick(ctx:discord_slash.SlashContext, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_kick(bot, ctx, user)


@slash.slash(name="travel", description="Travel to all of the Voice Channel.", guild_ids=GUILD_IDS)
async def travel_chanel(ctx:discord_slash.SlashContext, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_travel(bot, ctx, user)


@slash.slash(name="change", description="Convert the keyboard layout of your last message between en-th.", guild_ids=GUILD_IDS)
async def change_message(ctx:discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await change_last_message(ctx)
  
        
@slash.subcommand(base='codechannel', name='add', description='Add auto text formatting to a text channel.', 
                  options=[create_option(name='channel',description='The channel you want to add text formatting to.',
                                         option_type=SlashCommandOptionType.CHANNEL,required=True),
                           create_option(name='language',description='The programming language for text formatting on this channel.',
                                         option_type=SlashCommandOptionType.STRING,required=True,
                                         choices=SlashChoice.programmingLanguageChoice)])
async def _codechannel_add(ctx:discord_slash.SlashContext, channel:discord.TextChannel, language:str):
    await Add(ctx,channel,language)


@slash.subcommand(base='codechannel', name='remove',description='Add auto text formatting to a text channel.',
                  options = [create_option(name='channel',description='The channel you want to remove text formatting from.',
                                           option_type=SlashCommandOptionType.CHANNEL,required=True,)])
async def _codechannel_remove(ctx:discord_slash.SlashContext, channel:discord.TextChannel):
    await Remove(ctx,channel)
    
@slash.subcommand(base='codechannel', name='check',description='Check code channel in this server.')
async def _codechannel_check(ctx:discord_slash.SlashContext):
    await Check(ctx)
    

@slash.subcommand(base='codechannel', subcommand_group='permission', name='managemessage',description='Set Manage Messages permission of a/all code channel(s).',
                  options = [create_option(name='manageable',description='manageable or not.',
                                           option_type=SlashCommandOptionType.BOOLEAN,required=True),
                             create_option(name='channel',description='Choose a code channel| All code channels.',
                                           option_type=SlashCommandOptionType.CHANNEL,required=False)])
async def _codechannel_permission_managemessage(ctx:discord_slash.SlashContext, manageable:bool, channel:discord.TextChannel=None):
    await Permission.ManageMessage(ctx,manageable,channel)
    

    


    
bot.run(TOKEN)
