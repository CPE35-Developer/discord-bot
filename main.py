import os
import sys
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from src.utils.utils import guess_command
from src.utils.kick import random_kick
from src.utils.travel import random_travel
from src.utils.change import change_last_message
from src.utils.config import Config

from src.poker.poker import poker_play


from src.audio.audio import voice, disconnect

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=Config.prefix,
                   intents=discord.Intents.all(),
                   case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)
guild_ids = Config.GUILD_IDS

sys.path.insert(0, os.path.abspath("src/utils/"))


@slash.slash(name="hello", description="Say hi to the bot. Most used to check if bot is working.", guild_ids=guild_ids)
async def nine_nine(ctx):
    await ctx.send("HI :flushed:")


@slash.slash(name="poker", description="Play poker.", guild_ids=guild_ids)
async def poker(ctx):
    await poker_play(bot, ctx)


@slash.slash(name="voice", description="Play an audio(listed in $help voice) or say some thing(Text to speech)", guild_ids=guild_ids)
async def audio_say(ctx, *, sound=None):
    await voice(bot, ctx, sound)


@slash.slash(name="disconnect", description="Disconnect bot from the Voice Channel", guild_ids=guild_ids)
async def audio_disconnect(ctx):
    await disconnect(ctx)


@slash.slash(name="snap", description="Perfectly balanced, as all things should be", guild_ids=guild_ids)
async def snap_kick(ctx, user: discord.Member = None):
    await random_kick(bot, ctx, user)


@slash.slash(name="travel", description="Travel to all of the Voice Channel.", guild_ids=guild_ids)
async def travel_chanel(ctx, user: discord.Member = None):
    await random_travel(ctx, user)


@slash.slash(name="change", description="Convert the keyboard layout of your last message between en-th..", guild_ids=guild_ids)
async def change_message(ctx):
    await change_last_message(ctx)

@bot.command(name="hello", aliases=['hi', 'hoi'])
async def nine_nine(ctx):
    await ctx.send("HI :flushed:")

@bot.command(name="poker")
async def poker(ctx):
    await poker_play(bot, ctx)

@bot.command(name='voice', aliases=['v', 'vc'])
async def audio_say(ctx, *, sound=None):
    await voice(bot, ctx, sound)

@bot.command(name='disconnect',  aliases=['exit', 'dc'])
async def audio_disconnect(ctx):
    await disconnect(ctx)

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
    print(error)
    if isinstance(error, commands.CommandNotFound):
        msg = ctx.message.content.split()[0]
        em = discord.Embed( title=f"ไม่พบคำสั่งที่ชื่อว่า {msg}",
                            description= await guess_command(bot, msg,
                                                             bot.all_commands),
                            color=ctx.author.color) 
        await ctx.send(embed=em)
bot.run(TOKEN)
