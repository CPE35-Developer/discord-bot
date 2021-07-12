from termios import INLCR
from discord.ext.commands import MemberConverter
from random import sample, random

BOT_ID = 863101912730959894
GENERAL_VOICE_ID = 847172394316464184

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
      await ctx.send(f'มึงโดนแทนละกั้น {str(ctx.author)}')
      await ctx.author.move_to(None)

  else:
    general_channel = bot.get_channel(GENERAL_VOICE_ID)  
    member_ids = list(general_channel.voice_states.keys())
      
    random_member_ids = sample(member_ids, (len(member_ids)//2)+1)
    
    for member_id in random_member_ids:

      if BOT_ID == member_id:
        continue

      player = await MemberConverter().convert(ctx, str(member_id))
      print(str(player))

      await player.move_to(None)
