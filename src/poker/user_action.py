from symbol import comp_iter
from typing import List, Tuple
from .poker import show_middle_card


async def summary_phase(players, play_time, players_status: list[str], ctx):
    msg = ''
    for player, status in zip(players, players_status):
        if status == 'f':
            status_msg = 'หมอบ'
        elif status == 'p':
            status_msg = 'ผ่าน'
        elif status == 'b':
            status_msg = 'เกทับ'

        msg += str(player) + ' ' + status_msg + ' '
    await ctx.send(f'เฟสที่ {play_time+1}/3\nสรุปผล {msg}\n'+'-'*15)


async def pass_bet_fold(players, players_status, count_fold, max_current_bet, ctx, client):
    def check_pbf(msg):
        return msg.author == player and msg.channel == ctx.channel and \
            msg.content.lower() in ["p", "b", "f"]

    global check_bet

    def check_bet(msg_bet):
        return msg_bet.author == msg_author

    for idx_player, player in enumerate(players):
        global msg_author
        print(players_status)
        if players_status[idx_player] == 'f':
            continue

        await ctx.send(f'คุณ {str(player)} โปรดเลือก P/B/F')
        msg = await client.wait_for('message', check=check_pbf)
        msg_content = msg.content.lower()
        msg_author = msg.author

        if msg_content == 'f':  # หมอบ
            count_fold += 1
            idx_player_drop.append(idx_player)
            players_status[idx_player] = 'f'
            await ctx.send(f'{str(player)} หมอบ')

        elif msg_content == 'p':
            players_status[idx_player] = 'p'
            await ctx.send(f'{str(player)} ผ่าน')

        elif msg_content == 'b':
            while True:
                await ctx.send(f'คุณ {str(player)} โปรดเดิมพัน')

                msg_bet = await client.wait_for('message', check=check_bet)
                msg_bet_content = msg_bet.content

                if not msg_bet_content.isnumeric():
                    await ctx.send(f'โปรดใช้ตัวเลข')
                    continue
                print(msg_bet_content, max_current_bet)
                if int(msg_bet_content) < max_current_bet:
                    await ctx.send(f'โปรดเดิมพันให้สูงกว่าหรือเท่ากับ {max_current_bet}')
                    continue

                max_current_bet = int(msg_bet_content)
                await ctx.send(f'คุณ {str(msg_bet.author)} ได้เดิมพันเพิ่มเป็น {max_current_bet}')
                players_status[idx_player] = 'b'

                break

        print(f'{idx_player} COUNT : {count_fold} {len(players)}')
        if count_fold == len(players)-1:
            print(' GAME END PLZ ')
            return True


async def loop_pass_bet_fold(players, player_cards: List[Tuple[int, int]], middle_cards, client, ctx):
    global player, idx_player_drop, max_current_bet, count_fold
    count_fold = 0
    idx_player_drop = []
    max_current_bet = -1

    players_status = ['p'] * len(players)
    await ctx.send('เข้าสู่ขั้นตอนการ bet\nพิม P หรือ p เพื่อผ่าน\nB หรือ b เพื่อลงแต้มเพิ่ม\nF หรือ f เพื่อหมอบ')

    for play_time in range(3):
        await ctx.send(f'เฟสที่ {play_time+1}/3')
        found_winner = await pass_bet_fold(players, players_status, count_fold,
                                           max_current_bet, ctx, client)
        await summary_phase(players, play_time, players_status, ctx)
        if found_winner:
            await show_middle_card(middle_cards, ctx, True, False)
            await show_middle_card(middle_cards, ctx, True, True)
            return players_status

        if play_time == 0:
            await show_middle_card(middle_cards, ctx, True, False)
        elif play_time == 1:
            await show_middle_card(middle_cards, ctx, True, True)

    return players_status
