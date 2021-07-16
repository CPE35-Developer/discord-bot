import os
import discord
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
from discord.ext import commands
from src.utils.utils import commandSuggestFromError
from src.utils.kick import random_kick
from src.utils.travel import random_travel
from src.utils.change import change_last_message
from src.utils.config import Prefix
from src.utils.command import SlashChoice
from src.poker.poker import poker_play
from src.audio.audio import voice, say, play, disconnect
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv


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
    print(GUILD_IDS)


@bot.command(name="hello", aliases=['hi', 'hoi'])
async def nine_nine(ctx):
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


@bot.command(name='change', aliases=['c'])
async def change_message(ctx):
    await change_last_message(ctx)


@bot.event
async def on_command_error(ctx, error):
    await commandSuggestFromError(ctx, bot, error)


@slash.slash(name="hello", description="Say hi to the bot. Most used to check if bot is ready.", guild_ids=GUILD_IDS)
async def nine_nine(ctx):
    print(f'{str(ctx.author)} used {ctx.name}')
    await ctx.send("HI :flushed:")


@slash.slash(name="poker", description="Play poker.", guild_ids=GUILD_IDS)
async def poker(ctx):
    print(f'{str(ctx.author)} used {ctx.name}')
    await poker_play(bot, ctx)


@slash.slash(name="voice", description="Play an audio or say some thing(Text to speech)", guild_ids=GUILD_IDS,
             options=[create_option(name='message', description='The sound to play or the text for TTS',
                                    option_type=SlashCommandOptionType.STRING,
                                    required=True),

                      create_option(name='language', description='The language you want TTS to speak',
                                    option_type=SlashCommandOptionType.STRING, required=False,
                                    choices=SlashChoice.voiceLangChoice)])
async def audio_voice(ctx, message, language=None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await voice(bot, ctx, message, language)


@slash.slash(name="say", description="Say some thing(Text to speech)", guild_ids=GUILD_IDS,
             options=[create_option(name='message',
                                    description='The sound to play or the text for TTS',
                                    option_type=SlashCommandOptionType.STRING, required=True),

                      create_option(name='language',
                                    description='The language you want TTS to speak',
                                    option_type=SlashCommandOptionType.STRING, required=False,
                                    choices=SlashChoice.voiceLangChoice)])
async def audio_say(ctx, message, language=None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await say(bot, ctx, message, language)


@slash.slash(name="play", description="Play a sound", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='Choose a sound to play.',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.voiceSoundChoice)])
async def audio_play(ctx, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound)


@slash.slash(name="tu", description="ตู่", guild_ids=GUILD_IDS,
             options=[create_option(name='tusound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.voiceTuSoundChoice)])
async def audio_play(ctx, tusound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, tusound, tu=True)
    
@slash.slash(name="o", description="112", guild_ids=GUILD_IDS,
             options=[create_option(name='osound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.voiceOSoundChoice)])
async def audio_play(ctx, osound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, osound, tu=True)

@slash.slash(name="disconnect", description="Disconnect bot from the Voice Channel", guild_ids=GUILD_IDS)
async def audio_disconnect(ctx):
    print(f'{str(ctx.author)} used {ctx.name}')
    await disconnect(bot, ctx)


@slash.slash(name="snap", description="Perfectly balanced, as all things should be", guild_ids=GUILD_IDS)
async def snap_kick(ctx, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_kick(bot, ctx, user)


@slash.slash(name="travel", description="Travel to all of the Voice Channel.", guild_ids=GUILD_IDS)
async def travel_chanel(ctx, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_travel(bot, ctx, user)


@slash.slash(name="change", description="Convert the keyboard layout of your last message between en-th.", guild_ids=GUILD_IDS)
async def change_message(ctx):
    print(f'{str(ctx.author)} used {ctx.name}')
    await change_last_message(ctx)

bot.run(TOKEN)
