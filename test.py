import os, sys
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='$')

sys.path.insert(0, os.path.abspath("src/utils/"))

@bot.command(name='travel')
async def travel_chanel(ctx , user: discord.Member = None):
    print(type(user), user)
    print(type(user.voice), user.voice)

bot.run(TOKEN)
