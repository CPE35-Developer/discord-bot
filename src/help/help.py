from discord_slash import SlashContext
from discord import Embed
class SlashHelp:
    async def codechannel(ctx:SlashContext):
        embed=Embed(title="Information about code channel", color=0x4cd6c6)
        # embed.set_author(name=str(ctx.author), url=f'https://discord.com/users/{ctx.author.id}', icon_url=ctx.author.avatar_url)
        embed.add_field(name='การใช้งาน', value="Code channel จะเป็น channel สำหรับให้ bot auto-format ข้อความที่คุณส่งไว้ใน channel นั้น ให้เป็น code block ของภาษาที่คุณตั้งไว้ตอนเพิ่ม code channel\n\nหมายความว่าถ้าคุณส่งข้อความไปใน code channel จากที่เป็นข้อความธรรมดา, bot จะลบข้อความคุณและส่งข้อความของคุณในรุปแบบ code block แทน", inline=False)
        embed.add_field(name='/codechannel check', value="เป็นคำสั่งสำหรับการตรวจสอบว่ามี code channel ใน server ของคุณหรือเปล่า\n", inline=False)
        embed.add_field(name='/codechannel add', value="เป็นคำสั่งสำหรับการเพิ่ม code channel ใน server ของคุณ\nArguments: [channel, language]\n", inline=False)
        embed.add_field(name='/codechannel remove', value="เป็นคำสั่งสำหรับการลบ code channel ใน server ของคุณ\nArguments: [channel]\n", inline=False)
        embed.add_field(name='/codechannel permission', value="เป็นคำสั่งสำหรับการแก้ไข permission ใน code channel ของคุณ\n**managemessage**: การลบ/ปักหมุด ข้อความ\nArguments: [channel, managable:bool]\n", inline=False)


        await ctx.send(embed=embed)
        
        