from discord.ext.commands import MemberConverter
from random import randint

# i try but sometime we can't send user=bot but sometime we can i don't know why ;-;
# I fixed it |  @phusitsom
async def random_travel(ctx, user):

    if (user == ctx.message.author) | (not user):
        user = ctx.message.author
        if not user.voice:
            return await ctx.send(f'คุณ {str(ctx.message.author)} จะไปเที่ยวก็เข้ามาก่อนสิครับ')
            
    else:
        if user.bot: #bot check
            await ctx.send("ไม่ไปอ่ะ")
            return

        if not user.voice:
            await ctx.send(f'คุณ {str(ctx.message.author)} ต้องใช้กับคนที่อยู่ใน Voice Channel นะไอเวน')
            return

    voice_channel_list = ctx.guild.voice_channels
    if user is not None:
        first_channel = user.voice.channel
        await ctx.send(f'ไปเที่ยวกันเถอะคุณ {str(user)} ')
        for i in range(10):
            if(i==9):
                await user.move_to(first_channel)
            else:
                rand=randint(0,len(voice_channel_list)-1)
                await user.move_to(voice_channel_list[rand])

    else:
        first_channel = ctx.author.voice.channel
        await ctx.send(f'ไปเที่ยวกันเถอะคุณ {str(ctx.author)} ')

        for i in range(10):
            if(i==9):
                await user.move_to(first_channel)
            else:
                rand=randint(0,len(voice_channel_list)-1)
                await user.move_to(voice_channel_list[rand])