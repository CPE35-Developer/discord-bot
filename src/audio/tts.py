from gtts import gTTS
from discord import FFmpegPCMAudio
from src.utils.vc import get_PATH_ffmpeg
import googletrans

PATH_ffmpeg = get_PATH_ffmpeg()


async def repeat(vc, text: str = None, lang: str = None):
    if lang is not None:
        tts = gTTS(text=text, lang=lang)
    else:
        try:
            trans = googletrans.Translator()
            tts = gTTS(text=text, lang = trans.detect(text).lang)
        except:
            tts = gTTS(text=text, lang='en')

    print(f'Saying {text}')
    tts.save("text.mp3")
    vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg, source='text.mp3'))
