from src.utils.config import Prefix
from Commands import runCommands
from dotenv import load_dotenv
from discord_slash import SlashCommand
from discord.ext import commands
import discord
import os

import sys
sys.path.insert(0, os.path.abspath("src/utils/"))


load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=Prefix,
                   intents=discord.Intents.all(),
                   case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    global GUILD_IDS
    print(datetime.now())
    GUILD_IDS = [guild.id for guild in bot.guilds]
    GUILD_NAMES = [guild.name for guild in bot.guilds]
    print(GUILD_NAMES)
    me = await bot.fetch_user(ADMIN_ID)
    await me.send(f"Running {bot.user.name} on\n{platform.uname()}")

@bot.event
async def on_ready():
    await runCommands(bot, slash)
bot.run(TOKEN)