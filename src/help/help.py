from os import name
from discord_slash import SlashContext
from discord import Embed
from src.utils.member import getNick


class SlashHelp:
    async def codechannel(ctx: SlashContext):
        embed = Embed(title="Information about code channel", color=0x14b897)
        # embed.set_author(name=str(ctx.author), url=f'https://discord.com/users/{ctx.author.id}', icon_url=ctx.author.avatar_url)
        embed.add_field(name='การใช้งาน', value="Code channel จะเป็น channel สำหรับให้ bot auto-format ข้อความที่คุณส่งไว้ใน channel นั้น ให้เป็น code block ของภาษาที่คุณตั้งไว้ตอนเพิ่ม code channel\n\nหมายความว่าถ้าคุณส่งข้อความไปใน code channel จากที่เป็นข้อความธรรมดา, bot จะลบข้อความคุณและส่งข้อความของคุณในรุปแบบ code block แทน", inline=False)
        embed.add_field(name='/codechannel check',
                        value="เป็นคำสั่งสำหรับการตรวจสอบว่ามี code channel ใน server ของคุณหรือเปล่า\n", inline=False)
        embed.add_field(name='/codechannel add',
                        value="เป็นคำสั่งสำหรับการเพิ่ม code channel ใน server ของคุณ\nArguments: [channel, language]\n", inline=False)
        embed.add_field(name='/codechannel remove',
                        value="เป็นคำสั่งสำหรับการลบ code channel ใน server ของคุณ\nArguments: [channel]\n", inline=False)
        embed.add_field(name='/codechannel permission',
                        value="เป็นคำสั่งสำหรับการแก้ไข permission ใน code channel ของคุณ\n**managemessage**: การลบ/ปักหมุด ข้อความ\nArguments: [channel, managable:bool]\n", inline=False)
        embed.add_field(name='อื่นๆ', value="หากมี _ หรือ *  อยู่ข้างหน้าข้อความ bot จะไม่ทำการ format ให้\n\nหากต้องการ Embed ให้เติม `-e` ไว้ข้างหน้าข้อความของคุณ โดยไม่ต้องเว้นวรรคหรือขึ้นบรรทัดใหม้", inline=False)
        await ctx.send(embed=embed)

        examplecode = "print('Hello World')"

        await ctx.channel.send(f"`{examplecode}`\n```py\n{examplecode}\n```")

        await ctx.channel.send(f"`-e{examplecode}`")
        embed = Embed()
        pfp = ctx.author.avatar_url
        embed.set_thumbnail(url=pfp)
        embed.add_field(
            name='Code', value=f"""By {getNick(ctx.author)}```py\n{examplecode}\n```""")
        await ctx.channel.send(embed=embed)
