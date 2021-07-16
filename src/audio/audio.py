from discord import FFmpegPCMAudio, Embed
from src.utils.vc import joinVoiceChannel, leaveVoiceChannel, get_PATH_ffmpeg
from src.utils.member import getNick
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
        returnMessage = f'{getNick(ctx.author)} เล่น **{msg}**.mp3'
    else:
        await repeat(vc, text=msg, lang=language)
        returnMessage = f'{getNick(ctx.author)}: {msg}'

    return await ctx.send(returnMessage)


async def say(bot, ctx, msg, language=None, travel=False):
    
    try: isBotCommand = ctx.message.startswith('$')
    except: isBotCommand = False

    if (language is None) & (isBotCommand):
        msg, args = fetchArguments(msg)
        if args is not None:
            for arg in args:
                if arg.startswith('l'):
                    language = arg[2:]

    vc = await joinVoiceChannel(bot, ctx)

    if vc == None:
        return
 
    await repeat(vc, text=msg, lang=language)
    
    if travel is True:
        return 
    
    returnMessage = f'{getNick(ctx.author)}: {msg}'

    return await ctx.send(returnMessage)


async def play(bot, ctx, sound, political=False):

    vc = await joinVoiceChannel(bot, ctx)

    if vc == None:
        return
    
    vc.play(FFmpegPCMAudio(executable=PATH_ffmpeg,
            source=f"{CONFIG.audio.PATH_mp3}{sound}.mp3"))
        
    if not political:
        returnMessage = f'{getNick(ctx.author)} เล่น **{sound}**.mp3'
        return await ctx.send(returnMessage)
    else:
        returnMessage = f'||`ข้อความนี้ถูกลบโดยรัฐบาลไทย`||'
        return await ctx.send(returnMessage, delete_after=5)

    

async def disconnect(bot, ctx):
    await leaveVoiceChannel(bot, ctx)