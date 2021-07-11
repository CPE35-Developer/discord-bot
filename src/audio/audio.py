from discord import FFmpegPCMAudio
from discord.utils import get

from asyncio import TimeoutError

from gtts import gTTS

import os
sound_list = [file.replace(".mp3", "") for file in os.listdir("src/audio/mp3")]

async def join_channel(bot, ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("คุณไม่ได้อยู่ใน Channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        return voice
    

async def voice(bot, ctx, sound):
    voice = await join_channel(bot, ctx)

    def check(msg):
        return msg.channel == ctx.channel and \
            msg.content.lower() in sound_list

    if sound == None:
        await ctx.send(f"กรุณาเลือกเสียง {' '.join(sound_list)}\nหรือ พิมพ์เพื่อ Text to speech")
        try:
            msg = await bot.wait_for("message", check=check, timeout=20)
            sound = msg.content
        except TimeoutError:
            await ctx.send('หมดเวลาในการเลือก')
    

    print(f'Playing {sound}')
    voice.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe", source=f"src/audio/mp3/{sound}.mp3"))

async def disconnect(ctx):
    voice = ctx.voice_client
    if not voice:
        await ctx.send("จะให้ออกไปไหนนิ")
        return

    await voice.disconnect()
    await ctx.send("ออกละ")
