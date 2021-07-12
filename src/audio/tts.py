from gtts import gTTS
from discord import FFmpegPCMAudio
from langdetect import detect


async def repeat(vc, text=None):
    try:
        language = detect(text)
    except:
        language = 'en'
    tts = gTTS(text=text, lang=language)
    try: 
        tts.save("./text.mp3")
        vc.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe",source='./text.mp3'))
    except: 
        tts.save("C:/text.mp3")
        vc.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe",source='C:/text.mp3'))