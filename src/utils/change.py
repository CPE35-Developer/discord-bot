import json
with open('lang_switch.json', 'rb') as f:
    lang_switch = json.load(f)


async def change_last_message(ctx):

    channel = ctx.channel
    fetchMessage = await channel.history().flatten()
    for i in range(1, len(fetchMessage)):
        if (fetchMessage[i].author == ctx.author) & (not fetchMessage[i].content.startswith('$')):
            message = fetchMessage[i].content
            answer = ''
            for i in range(len(message)):

                try:
                    answer += lang_switch['en-th'][message[i]]
                except KeyError:
                    answer += lang_switch['th-en'][message[i]]

            await ctx.send(f"> {answer}\n`โดย {ctx.author}`")
            break
    if fetchMessage[i].content == None:
        await ctx.send(f'{ctx.author} พิมพ์มาก่อนดิวะไม่พิมพ์มาผมจะแก้อะไรล่ะะ')
