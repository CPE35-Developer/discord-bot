# https://discord.com/api/oauth2/authorize?client_id=864797655443308564&permissions=8&scope=applications.commands%20bot
from bot import TuanAraiMaiRoo

import discord
import discord_slash
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
from src.utils.guilddata import *
from src.utils.kick import random_kick
from src.utils.travel import random_travel
from src.utils.command import SlashChoice from src.format.code import send_fmc # from src.server.Server import ku_verify, ku_info
from src.poker.poker import poker_play
from src.pog.pog import pog_play
from src.games import rockpaperscissors
from src.maths.maths import solve_eq
from src.audio.audio import say, play, disconnect
from discord_slash.utils.manage_commands import create_option, create_choice
from src.utils.member import getNick
from src.utils.env import vars
import pkg_resources

import platform
from datetime import datetime

pkg_resources.require("googletrans>=4.0.0-rc.1")

bot = TuanAraiMaiRoo()
slash = SlashCommand(bot, sync_commands=True)


ADMIN_ID = 186315352026644480
GUILD_IDS = None


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
async def on_guild_join(guild):
    global GuildData
    global GuildIDs
    if guild.id not in GuildIDs:
        addGuild(guild.id)
        print(f'added {guild.id} to guild db')
        from src.utils.guilddata import GuildData, GuildIDs


@bot.event
async def on_message(msg: discord.Message):
    global GuildData, GuildIDs
    if msg.author.bot:
        return
    try:
        if msg.guild.id not in GuildIDs:
            addGuild(msg.guild.id)
            print(f'added {msg.guild.id} to guild db')
            from src.utils.guilddata import GuildData, GuildIDs

        channel = msg.channel
        guilddata = GuildData(msg.guild.id)

        if channel.id in guilddata.codechannel_ids:
            language = guilddata.channeldata(channel.id)['lang']

            if msg.content[0] in ['_', '*', '`', ' ']:
                return

            await send_fmc(msg, language)

            await msg.delete()
            return
        elif msg.content in guilddata.return_msg:
            await channel.send(guilddata.return_msg[msg.content])
            return
    except:
        pass


@slash.slash(name="hello", description="Say hi to the bot. Mo  used to check if bot is ready.", guild_ids=GUILD_IDS)
async def nine_nine(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await ctx.send("HI :flushed:")


@slash.slash(name='invitebot', description='I will send you the authorization link, see you in your server.', guild_ids=GUILD_IDS)
async def send_botinvitelink(ctx: discord_slash.SlashContext):
    await ctx.send('https://tinyurl.com/blackhole112')


@slash.subcommand(base='game', name="poker", description="Plays Poker.", guild_ids=GUILD_IDS)
async def _poker(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await poker_play(bot, ctx)


@slash.subcommand(base='game', name="pokdeng", description="Plays Pok Deng.", guild_ids=GUILD_IDS)
async def _pog(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await pog_play(bot, ctx)


@slash.subcommand(base='game', subcommand_group='rockpaperscissors', name='singleplayer',
                  description='Play Rock Paper Scissors with bot.', guild_ids=GUILD_IDS)
async def _rockpaperscissors(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await rockpaperscissors.RockPaperScissors.PlaySP(bot, ctx)


@slash.subcommand(base='game', subcommand_group='rockpaperscissors', name='multiplayer',
                  description='Play Rock Paper Scissors with friends.', guild_ids=GUILD_IDS)
async def _rockpaperscissors(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await rockpaperscissors.RockPaperScissors.PlayMP(bot, ctx)


@slash.slash(name="say", description="Say some thing(Text to speech)", guild_ids=GUILD_IDS,
             options=[create_option(name='message',
                                    description='The sound to play or the text for TTS',
                                    option_type=SlashCommandOptionType.STRING, required=True),

                      create_option(name='language',
                                    description='The language you want TTS to speak',
                                    option_type=SlashCommandOptionType.STRING, required=False,
                                    choices=SlashChoice.choiceVoiceLang)])
async def audio_say(ctx: discord_slash.SlashContext, message, language=None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await say(bot, ctx, message, language)


@slash.slash(name="play", description="Play a sound", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='Choose a sound to play.',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceSound)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound)


@slash.slash(name="tu", description="ตู่", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceTuVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.slash(name="pom", description="ป้อม", guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choicePomVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.subcommand(base='oneonetwo', name="o", description="112", guild_ids=GUILD_IDS,
                  options=[create_option(name='sound',
                                         description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                         option_type=SlashCommandOptionType.STRING, required=True,
                                         choices=SlashChoice.choiceOVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.subcommand(base='oneonetwo', name="nui", description="112", guild_ids=GUILD_IDS,
                  options=[create_option(name='sound',
                                         description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                         option_type=SlashCommandOptionType.STRING, required=True,
                                         choices=SlashChoice.choiceNuiVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.subcommand(base='oneonetwo', name="pui", description="112", guild_ids=GUILD_IDS,
                  options=[create_option(name='sound',
                                         description='[รายละเอียดถูกลบโดยรัฐบาลไทย]',
                                         option_type=SlashCommandOptionType.STRING, required=True,
                                         choices=SlashChoice.choicePuiVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound, political=True)


@slash.slash(name='n', description='Play N Sound for user [Warning! This sound can hurt your ears].', guild_ids=GUILD_IDS,
             options=[create_option(name='sound',
                                    description='Select Sound To play',
                                    option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=SlashChoice.choiceNVoice)])
async def audio_play(ctx: discord_slash.SlashContext, sound: str):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, sound)


@slash.slash(name='slap', description='Slap.', guild_ids=GUILD_IDS)
async def audio_play(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await play(bot, ctx, 'slap')


@slash.slash(name="disconnect", description="Disconnect bot from the Voice Channel", guild_ids=GUILD_IDS)
async def audio_disconnect(ctx: discord_slash.SlashContext):
    print(f'{str(ctx.author)} used {ctx.name}')
    await disconnect(bot, ctx)


@slash.slash(name="snap", description="Perfectly balanced, as all things should be", guild_ids=GUILD_IDS)
async def snap_kick(ctx: discord_slash.SlashContext, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_kick(bot, ctx, user)


@slash.slash(name='travel', description="Travel to all of the Voice Channel.", guild_ids=GUILD_IDS)
async def travel_chanel(ctx: discord_slash.SlashContext, user: discord.Member = None):
    print(f'{str(ctx.author)} used {ctx.name}')
    await random_travel(bot, ctx, user)


@slash.subcommand(base='codechannel', name='add', description='Add auto text formatting to a text channel.', guild_ids=GUILD_IDS,
                  options=[create_option(name='channel', description='The channel you want to add text formatting to.',
                                         option_type=SlashCommandOptionType.CHANNEL, required=True),
                           create_option(name='language', description='The programming language for text formatting on this channel.',
                                         option_type=SlashCommandOptionType.STRING, required=True,
                                         choices=SlashChoice.programmingLanguageChoice)])
async def _codechannel_add(ctx: discord_slash.SlashContext, channel: discord.TextChannel, language: str):
    await AddCodeChannel(ctx, channel, language)


@slash.subcommand(base='codechannel', name='remove', description='Add auto text formatting to a text channel.', guild_ids=GUILD_IDS,
                  options=[create_option(name='channel', description='The channel you want to remove text formatting from.',
                                           option_type=SlashCommandOptionType.CHANNEL, required=True,)])
async def _codechannel_remove(ctx: discord_slash.SlashContext, channel: discord.TextChannel):
    await RemoveCodeChannel(ctx, channel)


@slash.subcommand(base='codechannel', name='list', description='list all code channel in this server.', guild_ids=GUILD_IDS)
async def _codechannel_check(ctx: discord_slash.SlashContext):
    await ListCodeChannel(ctx)


@slash.subcommand(base='codechannel', subcommand_group='permission', name='managemessage', description='Set Manage Messages permission of a/all code channel(s).', guild_ids=GUILD_IDS,
                  options=[create_option(name='channel', description='Choose a code channel| All code channels.',
                                         option_type=SlashCommandOptionType.CHANNEL, required=True),
                           create_option(name='manageable', description='manageable or not.',
                                         option_type=SlashCommandOptionType.BOOLEAN, required=True)])
async def _codechannel_permission_managemessage(ctx: discord_slash.SlashContext, channel: discord.TextChannel, manageable: bool):
    await Permission.ManageMessage(ctx, manageable, channel)


@slash.subcommand(base='return', name='add', description='Add return messages. (Teach the bot.)', guild_ids=GUILD_IDS,
                  options=[create_option(name='message', description='-',
                                         option_type=SlashCommandOptionType.STRING, required=True),
                           create_option(name='return_message', description='The message that you want the bot to say in return.',
                                         option_type=SlashCommandOptionType.STRING, required=True)])
async def _returnmsg_add(ctx: discord_slash.SlashContext, message: str, return_message: str):
    await AddReturnMsg(ctx, message, return_message)


@slash.subcommand(base='return', name='remove', description="Remove return messages. (Delete the bot's memory.)", guild_ids=GUILD_IDS,
                  options=[create_option(name='message', description='The message that you want to delete.',
                                         option_type=SlashCommandOptionType.STRING, required=True)])
async def _returnmsg_add(ctx: discord_slash.SlashContext, message: str):
    await RemoveReturnMsg(ctx, message)


# @slash.slash(name='verify', description='Verifies that you are a true KU student', guild_ids=[847172394316464178, 440532168389689345])
# async def _verify(ctx: discord_slash.SlashContext):
#     await ctx.send(f"Verify is dead.")


# @slash.slash(name='info', description='Shows KU info of a user.', guild_ids=GUILD_IDS)
# async def _info(ctx: discord_slash.SlashContext, user: discord.Member = None):
#     msg = await ctx.send('Processing..')
#     await msg.edit(content="", embed=ku_info(ctx, user))


@slash.subcommand(base='math', name='solve', description='Solve an equation.', guild_ids=GUILD_IDS,
                  options=[create_option(name='equation', description='The equation you want to solve. (If possible, move the expression after (=) aside)',
                                         option_type=SlashCommandOptionType.STRING, required=True),
                           create_option(name='variable', description='The variable you want to solve for.',
                                         option_type=SlashCommandOptionType.STRING, required=False),
                           create_option(name='foregroundcolor', description='Foreground Color.',
                                         option_type=SlashCommandOptionType.STRING, required=False,
                                         choices=[create_choice("White", "White"), create_choice("Black", "Black")])])
async def _math_solve(ctx: discord_slash.SlashContext, equation: str, variable: str = None, color: str = "White"):
    await solve_eq(ctx, equation, variable, color)


bot.run(vars.TOKEN)
