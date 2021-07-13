import os
import sys
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

from src.utils.party import get_players
from src.utils.utils import guess_command
from src.utils.kick import random_kick
from src.utils.travel import random_travel
from src.utils.change import change_last_message
from src.utils.utils import config

from src.poker.poker import get_random_cards, send_card_msg
from src.poker.poker import show_middle_card
from src.poker.poker import who_win
from src.poker.user_action import loop_pass_bet_fold

from src.audio.audio import voice, disconnect

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=config.prefix,
                   intents=discord.Intents.all(),
                   case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)
guild_ids = config.GUILD_IDS

sys.path.insert(0, os.path.abspath("src/utils/"))


@slash.slash(name="hello", description="Say hi to the bot. Most used to check if bot is working.", guild_ids=guild_ids)
# @bot.command(name="hello", aliases=['hi', 'hoi'])
async def nine_nine(ctx):
    channel = bot.get_channel(ctx.channel.id)
    message_id = channel.last_message_id
    await ctx.send("HI :flushed:")


@slash.slash(name="poker", description="Play poker.", guild_ids=guild_ids)
# @bot.command(name="poker")
async def poker(ctx):
    players = await get_players(bot, ctx)
    if players is None:
        return
    player_cards, middle_cards = get_random_cards(players)
    print(middle_cards)
    print(player_cards)
    await send_card_msg(players, player_cards)
    await show_middle_card(middle_cards, ctx, False, False)
    players_status = await loop_pass_bet_fold(
        players, player_cards, middle_cards, bot, ctx
    )
    winner = await who_win(
        middle_cards, ctx, player_cards, players, players_status
    )


@slash.slash(name="voice", description="Play an audio(listed in $help voice) or say some thing(Text to speech)", guild_ids=guild_ids)
# @bot.command(name='voice', aliases=['v', 'vc'])
async def audio_say(ctx, *, sound=None):
    await voice(bot, ctx, sound)


@slash.slash(name="disconnect", description="Disconnect bot from the Voice Channel", guild_ids=guild_ids)
# @bot.command(name='disconnect',  aliases=['exit', 'dc'])
async def audio_disconnect(ctx):
    await disconnect(ctx)


@slash.slash(name="snap", description="Perfectly balanced, as all things should be", guild_ids=guild_ids)
# @bot.command(name='snap')
async def snap_kick(ctx, user: discord.Member = None):
    await random_kick(bot, ctx, user)


@slash.slash(name="travel", description="Travel to all of the Voice Channel.", guild_ids=guild_ids)
# @bot.command(name='travel')
async def travel_chanel(ctx, user: discord.Member = None):
    await random_travel(ctx, user)


@slash.slash(name="change", description="Convert the keyboard layout of your last message between en-th..", guild_ids=guild_ids)
# @bot.command(name='change', aliases=['c'])
async def change_message(ctx):
    await change_last_message(ctx)

bot.run(TOKEN)
