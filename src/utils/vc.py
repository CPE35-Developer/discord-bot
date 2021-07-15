from discord.utils import get
from src.utils.config import CONFIG
import os
import sys


def get_PATH_ffmpeg():
    if 'win' in sys.platform:
        PATH_ffmpeg = CONFIG.audio.PATH_ffmpeg_windows
        if not os.path.isfile(PATH_ffmpeg):
            from google_drive_downloader import GoogleDriveDownloader as gdd
            gdd.download_file_from_google_drive(file_id='1iK5q7--S6AY88hap32JhSN77gV-MB188',
                                                dest_path='src/audio/ffmpeg.exe')
    else:
        PATH_ffmpeg = CONFIG.audio.PATH_ffmpeg
    return PATH_ffmpeg


async def getUserVoiceState(ctx):

    try:
        voice_state = ctx.member.voice
    except:
        voice_state = ctx.author.voice

    if voice_state == None:
        await ctx.send('เข้า Voice Channel ก่อนสิคุณ')
        return None
    else:
        return voice_state.channel


async def joinVoiceChannel(bot, ctx):
    channel = await getUserVoiceState(ctx)
    vc = get(bot.voice_clients, guild=ctx.guild)
    if vc and vc.is_connected():
        await vc.move_to(channel)
    else:
        try:
            vc = await channel.connect()
        except AttributeError:
            vc = None
    return vc

