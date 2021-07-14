import json
with open('lang_switch.json', 'rb') as f:
    lang_switch = json.load(f)


async def change_last_message(ctx):

    channel = ctx.channel
    fetchMessage = await channel.history().flatten()
    for i in range(1, len(fetchMessage)):
        if (fetchMessage[i].author == ctx.author) & (not fetchMessage[i].content.startswith('$')):
            message = fetchMessage[i]
            answer = ''
            for j in range(len(message.content)):
                try:
                    answer += lang_switch['en-th'][message.content[j]]
                except KeyError:
                    answer += lang_switch['th-en'][message.content[j]]
            await message.reply(f" {answer}")
            break

    if message.content == None:
        await ctx.send(f'{ctx.author} พิมพ์มาก่อนดิวะไม่พิมพ์มาผมจะแก้อะไรล่ะะ')
