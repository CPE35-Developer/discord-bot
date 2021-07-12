from discord.ext.commands import MemberConverter
from discord.ext.commands import EmojiConverter
from random import sample, random

BOT_ID = 863101912730959894
THANOS_EMOJI_ID = 864186153033007125

async def kick_person(user):
  await user.move_to(None)

async def random_kick(bot, ctx, user):
  prob = random()
  if user is not None:
    if prob <= 0.5:
      await ctx.send(f'โชคร้ายหน่อยนะ {str(user)} บายย')
      await user.move_to(None)
    else:
      await ctx.send(f'โชคดีไป {str(user)}') #choose only 1 line between 18 or 19 or keep both?
      
      if user != ctx.author:
        await ctx.send(f'มึงโดนแทนละกั้น {str(ctx.author)}')
        await ctx.author.move_to(None)

  else:
    emoji = bot.get_emoji(THANOS_EMOJI_ID)
    await ctx.send(emoji)

    general_channel = ctx.author.voice.channel
    member_ids = list(general_channel.voice_states.keys())
      
    random_member_ids = sample(member_ids, len(member_ids)//2)
    
    for member_id in random_member_ids:

      if BOT_ID == member_id:
        continue

      player = await MemberConverter().convert(ctx, str(member_id))
      print(str(player))

      await player.move_to(None)
    await ctx.send(f'Perfectly balanced, as all things should be')
