from gtts import gTTS
from discord import FFmpegPCMAudio
from langdetect import detect
from src.utils.vc import get_PATH_ffmpeg
from src.utils.utils import config

PATH_ffmpeg =  get_PATH_ffmpeg()

async def repeat(vc, text=None):
    try:
        language = detect(text)
    except:
        language = 'en'

    tts = gTTS(text=text, lang=language)
    try:
        tts.save("text.mp3")
        vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg, source='text.mp3'))
    except:
        tts.save("C:/text.mp3")
        vc.play(FFmpegPCMAudio(executable=config.audio.PATH_ffmpeg_windows, source='C:/text.mp3'))