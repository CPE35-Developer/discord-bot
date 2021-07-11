import os

from discord.ext import commands
from dotenv import load_dotenv
from poker import get_players, get_random_cards
from poker import send_card_msg, three_middle_card_msg
from bot_help import command_list, guess_command
load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='$')
@bot.command(name='hello')
async def nine_nine(ctx):
    channel = bot.get_channel(ctx.channel.id)
    message_id = channel.last_message_id
    await ctx.send('HI :heart:')

@bot.command(name='poker')
async def poker(ctx):
    players = await get_players(bot, ctx)
    if players is None:
        return
    player_cards, middle_cards = get_random_cards(players)
    print(middle_cards)
    print(player_cards)
    await send_card_msg(players, player_cards)
    await three_middle_card_msg(middle_cards, ctx)

@bot.event
async def on_message(message):
  await bot.process_commands(message)
  await guess_command(bot, message)

bot.run(TOKEN)
