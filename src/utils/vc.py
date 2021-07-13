from discord.utils import get
from src.utils.utils import config
import os, sys

def get_PATH_ffmpeg():
    if 'win' in sys.platform:
        PATH_ffmpeg = config.audio.PATH_ffmpeg_windows
        if not os.path.isfile(PATH_ffmpeg):
            from google_drive_downloader import GoogleDriveDownloader as gdd
            gdd.download_file_from_google_drive(file_id='1iK5q7--S6AY88hap32JhSN77gV-MB188',
                                            dest_path='src/audio/ffmpeg.exe')
    else: 
        PATH_ffmpeg = config.audio.PATH_ffmpeg
    return PATH_ffmpeg


async def get_vc(ctx):

    try: 
        voice_state = ctx.member.voice
    except AttributeError:
        voice_state = ctx.author.voice
        
    if not voice_state:
        await ctx.send('เข้า Voice Channel ก่อนสิคุณ')
        return 
    else: 
        return voice_state.channel


async def join_vc(bot, ctx):
    channel = await get_vc(ctx)
    vc = get(bot.voice_clients, guild=ctx.guild)
    if vc and vc.is_connected():
        await vc.move_to(channel)
    else:
        vc = await channel.connect()
    return vc