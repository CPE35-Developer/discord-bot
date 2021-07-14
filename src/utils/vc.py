from discord.utils import get
from src.utils.config import CONFIG
import os
import sys
from discord_slash.utils.manage_commands import create_choice


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


async def get_vc(ctx):

    try:
        voice_state = ctx.member.voice
    except:
        voice_state = ctx.author.voice

    if voice_state == None:
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
        try:
            vc = await channel.connect()
        except AttributeError:
            vc = None
    return vc

voiceLangChoice = [{"value": "af", "name": "Afrikaans"},
                   {"value": "ar", "name": "Arabic"},
                   {"value": "de", "name": "German"},
                   {"value": "el", "name": "Greek"},
                   {"value": "en", "name": "English"},
                   {"value": "es", "name": "Spanish"},
                   {"value": "fi", "name": "Finnish"},
                   {"value": "fr", "name": "French"},
                   {"value": "hi", "name": "Hindi"},
                   {"value": "id", "name": "Indonesian"},
                   {"value": "it", "name": "Italian"},
                   {"value": "ja", "name": "Japanese"},
                   {"value": "ko", "name": "Korean"},
                   {"value": "la", "name": "Latin"},
                   {"value": "mk", "name": "Macedonian"},
                   {"value": "my", "name": "Myanmar (Burmese)"},
                   {"value": "nl", "name": "Dutch"},
                   {"value": "pl", "name": "Polish"},
                   {"value": "pt", "name": "Portuguese"},
                   {"value": "ru", "name": "Russian"},
                   {"value": "th", "name": "Thai"},
                   {"value": "tl", "name": "Filipino"},
                   {"value": "tr", "name": "Turkish"},
                   {"value": "vi", "name": "Vietnamese"},
                   {"value": "zh-CN", "name": "Chinese"}]
