from gtts import gTTS
from discord import FFmpegPCMAudio
from langdetect import detect
from src.utils.vc import get_PATH_ffmpeg
from src.utils.utils import config
import sys
PATH_ffmpeg =  get_PATH_ffmpeg()

async def repeat(vc, text=None):
    try:
        language = detect(text)
    except:
        language = 'en'
        
    tts = gTTS(text=text, lang=language)
    
    if 'win' in sys.platform: 
        tts.save("C:/text.mp3")
        vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg, source='C:/text.mp3'))
    
    else:
        tts.save("text.mp3")
        try: 
            vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg, source='text.mp3'))
        except:
            vc.play(FFmpegPCMAudio(executable=config.PATH_ffmpeg_windows, source='text.mp3'))
        
