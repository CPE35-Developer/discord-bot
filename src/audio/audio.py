from discord import FFmpegPCMAudio, Embed, Colour
from src.utils.vc import joinVoiceChannel, get_PATH_ffmpeg
from src.utils.config import CONFIG, MP3_files
from src.audio.tts import repeat
from src.utils.command import fetchArguments
PATH_ffmpeg = get_PATH_ffmpeg()


async def voice(bot, ctx, msg, language=None, ):
    
    if not language:
        msg, args = fetchArguments(msg)
        ttsLang = None
        if (args != None) & (ttsLang == None):
            for arg in args:
                if arg.startswith('l'):
                    language = arg[2:]

    vc = await joinVoiceChannel(bot, ctx)

    if vc == None:
        return

    if (msg in MP3_files) & (not language):
        vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,
                source=f"{CONFIG.audio.PATH_mp3}{msg}.mp3"))
        returnMessage = f'{ctx.author.nick if ctx.author.nick is not None else ctx.author.name} เล่น **{msg}**.mp3'
    else:
        await repeat(ctx, vc, text=msg, lang=language)
        returnMessage = f'{ctx.author.nick if ctx.author.nick is not None else ctx.author.name}: {msg}'

    return await ctx.send(returnMessage)


async def say(bot, ctx, msg, language=None, travel=False):
    
  

    if not language:
        msg, args = fetchArguments(msg)
        ttsLang = None
        if (args != None) & (ttsLang == None):
            for arg in args:
                if arg.startswith('l'):
                    language = arg[2:]

    vc = await joinVoiceChannel(bot, ctx)

    if vc == None:
        return
 
    await repeat(ctx, vc, text=msg, lang=language)
    
    if travel is True:
        return 
    
    returnMessage = f'{ctx.author.nick if ctx.author.nick is not None else ctx.author.name}: {msg}'

    return await ctx.send(returnMessage)


async def play(bot, ctx, sound):

    vc = await joinVoiceChannel(bot, ctx)

    if vc == None:
        return

    vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,
            source=f"{CONFIG.audio.PATH_mp3}{sound}.mp3"))
    returnMessage = f'{ctx.author.nick if ctx.author.nick is not None else ctx.author.name} เล่น **{sound}**.mp3'

    return await ctx.send(returnMessage)

#VVV ERROR
async def disconnect(ctx):
    print(ctx.guild.voice_client.channel.name)
    if ctx.guild.voice_client is not None:
        await ctx.send(f'ออกจาก {ctx.guild.voice_client.channel.mention} ละ')
        await ctx.guild.voice_client.disconnect()
        return
    else:
        embed = Embed(title=f'Command Error', color = 0xc11515)
        embed.add_field(name=f"{ctx.name}", value="บอทควรอยู่ใน Voice Channel ก่อน\nหรือควรทำคำสั่งเกี่ยวกับเสียงก่อน", inline=False)
        await ctx.channel.send(embed = embed)
        return
