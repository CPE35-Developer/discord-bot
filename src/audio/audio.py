from discord import FFmpegPCMAudio
from discord.utils import get
from asyncio import TimeoutError
import os, sys
from src.utils.vc import join_vc, get_PATH_ffmpeg
from src.utils.config import CONFIG
from src.audio.tts import repeat

PATH_mp3 = CONFIG.audio.PATH_mp3
PATH_ffmpeg = get_PATH_ffmpeg()
sound_list = [file.replace(".mp3", "") for file in os.listdir(PATH_mp3)]



async def voice(bot, ctx, sound):
    vc = await join_vc(bot, ctx)

    if vc == None: 
        return

    def check(msg):
        return ctx.author == msg.author

    if sound == None:
        
        await ctx.send(f"กรุณาเลือกเสียง [{', '.join(sound_list)}]\nหรือ พิมพ์อย่างอื่นเพื่อ Text to speech")
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=20)
            if msg.content.lower() in sound_list:
                sound = msg.content.lower()
            else:
                print(msg.content)
                sound = msg.content
                print(sound)
                await repeat(vc, text=sound)
                return
                
        except TimeoutError:
            await ctx.send('หมดเวลาในการเลือก')
            return

    if sound in sound_list:
        print(f'Playing {sound}')
        vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,source=f"{PATH_mp3}{sound}.mp3"))
    else:
        await repeat(vc, text=sound)

async def disconnect(ctx):
    vc = ctx.voice_client
    if not vc:
        await ctx.send("จะให้ออกไปไหนนิ")
        return

    await vc.disconnect()
    await ctx.send("ออกละ")
