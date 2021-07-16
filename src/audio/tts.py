from gtts import gTTS
from discord import FFmpegPCMAudio
from src.utils.vc import get_PATH_ffmpeg
from src.utils.config import CONFIG
import googletrans

PATH_ffmpeg = get_PATH_ffmpeg()


async def repeat(vc, text: str, lang: str = None):
    trans = googletrans.Translator()
    if lang is not None:
        tts = gTTS(text=text, lang=lang)
    else:
        try:
            tts = gTTS(text=text, lang = trans.detect(text).lang)
        except:
            tts = gTTS(text=text, lang='en')

    print(f'Saying {text}')
    try:
        tts.save("text.mp3")
        vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg, source='text.mp3'))
    except:
        tts.save("C:/text.mp3")
        vc.play(FFmpegPCMAudio(executable=CONFIG.audio.PATH_ffmpeg_windows, source='C:/text.mp3'))

        
