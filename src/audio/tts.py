from gtts import gTTS
from discord import FFmpegPCMAudio
from src.utils.vc import get_PATH_ffmpeg

PATH_ffmpeg = get_PATH_ffmpeg()


async def repeat(ctx, vc, text: str = None, lang: str = None):
    if not lang == None:
        tts = gTTS(text=text, lang=lang)
    else:
        try:
            tts = gTTS(text=text)
        except:
            tts = gTTS(text=text, lang='th')

    print(f'Saying {text}')
    tts.save("text.mp3")
    vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg, source='text.mp3'))
