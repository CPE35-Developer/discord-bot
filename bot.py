import platform
import discord
from discord.ext.commands import Bot
from src.utils.config import Prefix
from datetime import datetime


class TuanAraiMaiRoo(Bot):

    def __init__(self):
        activity = discord.Activity(
            type=discord.ActivityType.competing, name='the universe')
        Bot.__init__(self, command_prefix=Prefix,
                     intents=discord.Intents.all(),
                     case_insensitive=True,
                     activity=activity,
                     status=discord.Status.online)
