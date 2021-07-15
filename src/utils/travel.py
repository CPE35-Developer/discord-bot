from random import randint
from src.audio.audio import say

async def random_travel(bot, ctx, user):

    if (not user) | (user == ctx.author):
        user = ctx.author
        if not user.voice:
            return await ctx.send(f'คุณ {str(ctx.author)} จะไปเที่ยวก็เข้ามาก่อนสิครับ')

    else:
        if user.bot:  # bot check
            await ctx.send("ไม่ไปอ่ะ")
            return

        if not user.voice:
            await ctx.send(f'คุณ {str(ctx.author)} ต้องใช้กับคนที่อยู่ใน Voice Channel นะไอเวน')
            return

    voice_channel_list = ctx.guild.voice_channels

    first_channel = user.voice.channel
    await ctx.send(f'ไปเที่ยวกันเถอะคุณ {str(user)} ')
    for i in range(10):
        if(i == 9):
            await user.move_to(first_channel)
        else:
            rand = randint(0, len(voice_channel_list)-1)
            await user.move_to(voice_channel_list[rand])
            
    await say(bot, ctx, f'Welcome back {ctx.author.nick if ctx.author.nick is not None else ctx.author.name}', travel=True)
