import os

from discord.ext import commands
from dotenv import load_dotenv

from src.utils.party import get_players
from src.utils.utils import guess_command

from src.poker.poker import get_random_cards, send_card_msg
from src.poker.poker import show_middle_card
from src.poker.user_action import loop_pass_bet_fold

from src.audio.audio import say

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="$")


@bot.command(name="hello")
async def nine_nine(ctx):
    channel = bot.get_channel(ctx.channel.id)
    message_id = channel.last_message_id
    await ctx.send("HI :heart:")


@bot.command(name="poker")
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


@bot.command(name='say')
async def say_sound(ctx, sound):
    await say(bot, ctx, sound)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await guess_command(bot, message)

bot.run(TOKEN)
