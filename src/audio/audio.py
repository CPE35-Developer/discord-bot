from discord import FFmpegPCMAudio
from discord.utils import get

from asyncio import TimeoutError

import os
sound_list = [file.replace(".mp3", "") for file in os.listdir("src/audio/mp3")]

from src.audio.tts import repeat
    

async def voice(bot, ctx, sound):

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

    def check(msg):
        return ctx.author == msg.author

    if sound == None:
        
        await ctx.send(f"กรุณาเลือกเสียง [{', '.join(sound_list)}]\nหรือ พิมพ์อย่างอื่นเพื่อ Text to speech")
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=20)
            if msg.content.lower() in sound_list:
                sound = msg.content.lower()
            else:
                sound = msg.content
                await repeat(bot, ctx, voice, text=sound)
                return
                
        except TimeoutError:
            await ctx.send('หมดเวลาในการเลือก')
            return

    if sound in sound_list:
        print(f'Playing {sound}')
        voice.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe",\
                                    source=f"src/audio/mp3/{sound}.mp3"))
    else:
        await repeat(bot, ctx, voice, text=sound)

async def disconnect(ctx):
    voice = ctx.voice_client
    if not voice:
        await ctx.send("จะให้ออกไปไหนนิ")
        return

    await voice.disconnect()
    await ctx.send("ออกละ")
