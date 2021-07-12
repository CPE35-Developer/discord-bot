from discord.ext.commands import MemberConverter

async def random_kick(ctx, user):
  print(user)
  my_id = 348459759323709441
  player = await MemberConverter().convert(ctx, str(my_id))
  print(player)
  await player.move_to(None)
  