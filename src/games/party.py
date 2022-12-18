async def get_players(bot, ctx):
    players = []
    intro_str = 'พิมพ์ **y** เพื่อเข้าร่วมปาร์ตี้\nพิมพ์ **n** เพื่อออกจากปาร์ตี้\nพิมพ์ **done** เพื่อยืนยันปาร์ตี้\nพิมพ์ **cancel** เพื่อยกเลิกการสร้างปาร์นี้'

    await ctx.send(intro_str)

    def check(msg):
        return msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n", "done", "cancel"]

    while True:
        msg = await bot.wait_for("message", check=check)

        if (msg.content.lower() == "y") & (msg.author not in players):
            players.append(msg.author)
            players = list(set(players))
            await ctx.channel.send(f"ตอนนี้มี {' '.join([str(member) for member in players])} เป็นผู้เล่น ({len(players)} คน)")

        elif (msg.content.lower() == "y") & (msg.author in players):
            await ctx.channel.send(f"เองอยู่ในเกมแล้วไอเปรด {msg.author}")

        elif (msg.content.lower() == "n") & (msg.author in players):
            players.remove(msg.author)
            if len(players) == 0:
                await ctx.channel.send(f'อ้าวไม่มีคนเล่นละ :( ({len(players)} คน)')
            else:
                await msg.author.send("ชิ่วๆ")
                await ctx.send(f"ตอนนี้เหลือ {' '.join([str(member) for member in players])} ({len(players)} คน); ไปไป๊ {msg.author}")

        elif (msg.content.lower() == "n") & (msg.author not in players):
            await ctx.channel.send(f"เข้าเกมมาก่อนดิค่อยออก {msg.author}")

        elif (msg.content.lower() == 'cancel'):
            await ctx.channel.send('k**y เสียเวลาฉิบหาย')
            return None

        elif (msg.content.lower() == "done") and (len(players) == 0):
            await ctx.channel.send(f"ยังไม่มีใครอยู่ในปาร์ตี้เลยนิ")

        elif (msg.content.lower() == "done") and (len(players) == 1):
            await ctx.channel.send(f"ผมไม่ให้คุณเล่นคนเดียวหรอก")

        elif (msg.content.lower() == "done") or (len(players) == 9):
            await ctx.channel.send(f"ผู้เล่นทั้งหมดคือ {' '.join([str(member) for member in players])} ถูกมั้ย (y=ใช่,n=แก้ไขจำนวนคนต่อ)")

            while True:
                chk_msg = await bot.wait_for("message", check=check)
                if (chk_msg.content.lower() == 'y'):
                    return players
                elif (chk_msg.content.lower() == 'n'):
                    await ctx.channel.send(intro_str)
                    break
