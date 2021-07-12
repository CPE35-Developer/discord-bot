#pip install gtts langdetect
from gtts import gTTS
from discord import FFmpegPCMAudio
from langdetect import detect


async def repeat(voice, text=None):

    try:
        lang = detect(text)
    except:
        lang = 'en'
    tts = gTTS(text=text, lang=detect(lang))
    tts.save("C:/text.mp3")

    voice.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe",source='C:/text.mp3'))