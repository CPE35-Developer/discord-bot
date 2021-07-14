from discord import FFmpegPCMAudio
from src.utils.vc import leavevoice, join_vc, get_PATH_ffmpeg
from src.utils.config import CONFIG, MP3_files
from src.audio.tts import repeat
from src.utils.command import fetchArguments
PATH_ffmpeg = get_PATH_ffmpeg()


async def voice(bot, ctx, msg, language=None):

    if not language:
        msg, args = fetchArguments(msg)
        ttsLang = None
        if (args != None) & (ttsLang == None):
            for arg in args:
                if arg.startswith('l'):
                    language = arg[2:]

    vc = await join_vc(bot, ctx)

    if vc == None:
        return

    if (msg in MP3_files) & (not language):
        vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,
                source=f"{CONFIG.audio.PATH_mp3}{msg}.mp3"))
        returnMessage = f'{ctx.author.nick if not ctx.author.nick else ctx.author.name} เล่น **{msg}**.mp3'
    else:
        await repeat(ctx, vc, text=msg, lang=language)
        returnMessage = f'{ctx.author.nick if not ctx.author.nick else ctx.author.name}: {msg}'

    return await ctx.send(returnMessage)


async def say(bot, ctx, msg, language=None):

    if not language:
        msg, args = fetchArguments(msg)
        ttsLang = None
        if (args != None) & (ttsLang == None):
            for arg in args:
                if arg.startswith('l'):
                    language = arg[2:]

    vc = await join_vc(bot, ctx)

    if vc == None:
        return

    await repeat(ctx, vc, text=msg, lang=language)
    returnMessage = f'{ctx.author.mention}: {msg}'

    return await ctx.send(returnMessage)


async def play(bot, ctx, sound):

    vc = await join_vc(bot, ctx)

    if vc == None:
        return

    vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,
            source=f"{CONFIG.audio.PATH_mp3}{sound}.mp3"))
    returnMessage = f'{ctx.author.nick if not ctx.author.nick else ctx.author.name} เล่น **{sound}**.mp3'

    return await ctx.send(returnMessage)

#VVV ERROR
async def disconnect(bot, ctx):
    return await leavevoice(bot,ctx)
