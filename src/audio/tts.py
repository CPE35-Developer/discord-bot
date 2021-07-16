#pip install gtts langdetect
from gtts import gTTS
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.utils import get
import discord
from langdetect import detect


async def repeat(bot, ctx, voice, *, text=None):

    tts = gTTS(text=text, lang=detect(text))
    tts.save("C:/text.mp3")

    voice.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe",source='C:/text.mp3'))