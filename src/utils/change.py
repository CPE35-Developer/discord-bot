
async def change_last_message(ctx):
    channel = ctx.channel
    print(channel.history())
    fetchMessage = await channel.history().find(lambda m: m.author.id == ctx.author.id)
    if fetchMessage is None:
        print("-"*20)
    else:
        print(fetchMessage)
        await ctx.send(f'{fetchMessage.content}')