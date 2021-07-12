from termios import INLCR
from discord.ext.commands import MemberConverter
from random import sample

async def random_kick(bot, ctx, user):
  general_channel = bot.get_channel(847172394316464184)
  member_ids = general_channel.voice_states.keys()
  random_member_ids = sample(member_ids, len(member_ids)//2)
  
  for member_id in random_member_ids:
    player = await MemberConverter().convert(ctx, str(member_id))
    print(str(player))
  
    await player.move_to(None)
  