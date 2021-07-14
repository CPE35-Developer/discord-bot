from src.utils.config import CONFIG
from discord.ext.commands import MemberConverter
from random import sample, random


async def kick_person(user):
    await user.move_to(None)


async def random_kick(bot, ctx, user):
    prob = random()
    if user is not None:
        if prob <= 0.5:
            await ctx.send(f'โชคร้ายหน่อยนะ {str(user)} บายย')
            await user.move_to(None)
        else:
            # choose only 1 line between 18 or 19 or keep both?
            await ctx.send(f'โชคดีไป {str(user)}')

            if user != ctx.author:
                await ctx.send(f'มึงโดนแทนละกั้น {str(ctx.author)}')
                await ctx.author.move_to(None)

    else:
        snap_emoji = CONFIG.EMOJI_ID.thanos_snap
        bot_id = CONFIG.BOT_ID
        await ctx.send(snap_emoji)

        general_channel = ctx.author.voice.channel
        member_ids = list(general_channel.voice_states.keys())

        random_member_ids = sample(member_ids, len(member_ids)//2)

        for member_id in random_member_ids:

            if bot_id == member_id:
                continue

            player = await MemberConverter().convert(ctx, str(member_id))
            print(str(player))

            await player.move_to(None)
        await ctx.send(f'Perfectly balanced, as all things should be')
