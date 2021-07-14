import os
import sys
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
from Commands import runCommands
from src.utils.config import Prefix

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix=Prefix,
                   intents=discord.Intents.all(),
                   case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)

sys.path.insert(0, os.path.abspath("src/utils/"))


@bot.event
async def on_ready():
    await runCommands(bot, slash)
bot.run(TOKEN)
