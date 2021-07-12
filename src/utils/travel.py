from discord.ext.commands import MemberConverter
from random import randint

# i try but sometime we can't send user=bot but sometime we can i don't know why ;-;
async def random_travel(bot, ctx, user):
    '''
    P.S. i don't know how to check (is_user_join_voice_chanel) if they don't join 
            below code make  AttributeError:
    if(ctx.author.voice.channel == None):
        await ctx.send(f'คุณ {str(user)} ต้องอยู่ใน voice_chanel ก่อนน้า')
        return 0
    '''

    '''
    print(bot)
    print(user)
    if(bot==user):
        return 0
    '''

    voice_channel_list = ctx.guild.voice_channels
    if user is not None:
        '''
        P.S. i don't know how to check (is_user_join_voice_chanel) if they don't join 
            below code make  AttributeError:
        if(user.voice.channel == None):
            await ctx.send(f'คุณ {str(user)} ต้องใช้กับคนที่อยู่ใน voice_chanel นะไอเวน')
            return 0
        '''
        first_chanel = user.voice.channel
        await ctx.send(f'ไปเที่ยวกันเถอะคุณ {str(user)} ')
        for i in range(10):
            if(i==9):
                await user.move_to(first_chanel)
            else:
                rand=randint(0,len(voice_channel_list)-1)
                await user.move_to(voice_channel_list[rand])

    else:
        first_chanel = ctx.author.voice.channel
        await ctx.send(f'ไปเที่ยวกันเถอะคุณ {str(ctx.author)} ')

        for i in range(10):
            if(i==9):
                await user.move_to(first_chanel)
            else:
                rand=randint(0,len(voice_channel_list)-1)
                await user.move_to(voice_channel_list[rand])