from discord import FFmpegPCMAudio
from discord.utils import get

async def say(bot, ctx, sound):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    print(f'Playing {sound}')
    voice.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe", source=f"src/audio/mp3/{sound}.mp3"))