from discord.ext.commands import Context
from discord import TextChannel
from discord.utils import f
async def deleteMesssage(ctx:Context, channel:TextChannel, id:int):
    msg = channel.fetch_message(id)
    if msg.author == ctx.author:
        msg.delete()
        await ctx.send('Your message was deleted.')
    else:
        await ctx.send("That's not your message.")