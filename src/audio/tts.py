from gtts import gTTS
from discord import FFmpegPCMAudio
from discord.utils import get
from src.audio.audio import join_channel

async def repeat(bot, ctx, *, text=None):

    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')

    if not text:
        await ctx.send(f"Hey {ctx.author.mention}, I need to know what to say please.")
        return

    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("คุณไม่ได้อยู่ใน Channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    # Lets prepare our text, and then save the audio file
    tts = gTTS(text=text, lang_check=True)
    tts.save("text.mp3")

    try:
        # Lets play that mp3 file in the voice channel
        voice.play(FFmpegPCMAudio(executable="src/audio/ffmpeg.exe",source='text.mp3'), after=lambda e: print(f"Finished playing: {e}"))

        # Lets set the volume to 1
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1

    # Handle the exceptions that can occur
    except ClientException as e:
        await ctx.send(f"A client exception occured:\n`{e}`")
    except TypeError as e:
        await ctx.send(f"TypeError exception:\n`{e}`")
    except OpusNotLoaded as e:
        await ctx.send(f"OpusNotLoaded exception: \n'{e}'")