from random import randint
from src.audio.audio import say
from src.utils.member import getNick

async def random_travel(bot, ctx, user):

    if (not user) | (user == ctx.author):
        user = ctx.author
        if not user.voice:
            return await ctx.send(f'คุณ {getNick(ctx.author)} จะไปเที่ยวก็เข้ามาก่อนสิครับ')

    else:
        if user.bot:  # bot check
            await ctx.send("ไม่ไปอ่ะ")
            return

        if not user.voice:
            await ctx.send(f'คุณ {getNick(ctx.author)} ต้องใช้กับคนที่อยู่ใน Voice Channel นะไอเวน')
            return

    voice_channel_list = ctx.guild.voice_channels

    first_channel = user.voice.channel
    await ctx.send(f'ไปเที่ยวกันเถอะคุณ {getNick(user)} ')
    for i in range(10):
        if(i == 9):
            await user.move_to(first_channel)
        else:
            rand = randint(0, len(voice_channel_list)-1)
            await user.move_to(voice_channel_list[rand])
            
    await say(bot, ctx, f'Welcome back {getNick(user).lower()}','en', travel=True)
