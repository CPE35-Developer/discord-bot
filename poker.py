from typing import List, Tuple
from random import sample, shuffle

DECKS_OF_CARDS = [
    ':two: :clubs:', ':two: :diamonds:', ':two: :heart:', ':two: :spades:',
    ':three: :clubs:', ':three: :diamonds:', ':three: :heart:', ':three: :spades:',
    ':four: :clubs:', ':four: :diamonds:', ':four: :heart:', ':four: :spades:',
    ':five: :clubs:', ':five: :diamonds:', ':five: :heart:', ':five: :spades:',
    ':six: :clubs:', ':six: :diamonds:', ':six: :heart:', ':six: :spades:',
    ':seven: :clubs:', ':seven: :diamonds:', ':seven: :heart:', ':seven: :spades:',
    ':eight: :clubs:', ':eight: :diamonds:', ':eight: :heart:', ':eight: :spades:',
    ':nine: :clubs:', ':nine: :diamonds:', ':nine: :heart:', ':nine: :spades:',
    ':one::zero: :clubs:', ':one::zero: :diamonds:', ':one::zero: :heart:', ':one::zero: :spades:',
    ':regional_indicator_j: :clubs:', ':regional_indicator_j: :diamonds:', ':regional_indicator_j: :heart:', ':regional_indicator_j: :spades:',
    ':regional_indicator_q: :clubs:', ':regional_indicator_q: :diamonds:', ':regional_indicator_q: :heart:', ':regional_indicator_q: :spades:',
    ':regional_indicator_k: :clubs:', ':regional_indicator_k: :diamonds:', ':regional_indicator_k: :heart:', ':regional_indicator_k: :spades:',
    ':a: :clubs:', ':a: :diamonds:', ':a: :heart:', ':a: :spades:'
]


async def get_players(client, ctx):
    players = []
    intro_str = 'พิมพ์ **y** เพื่อเข้าร่วมปาร์ตี้\nพิมพ์ **n** เพื่อออกจากปาร์ตี้\nพิมพ์ **done** เพื่อยืนยันปาร์ตี้\nพิมพ์ **cancel** เพื่อยกเลิกการสร้างปาร์นี้'
    # ให้ bot ส่งคำแนะนำเข้า text channel
    await ctx.send(intro_str)

    def check(msg):
        return msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n", "done", "cancel"]

    while True:
        msg = await client.wait_for("message", check=check)

        if (msg.content.lower() == "y") & (msg.author not in players):
            players.append(msg.author)
            players = list(set(players))
            await ctx.send(f"ตอนนี้มี {' '.join([str(member) for member in players])} เป็นผู้เล่น ({len(players)} คน)")
            print(players)

        elif (msg.content.lower() == "y") & (msg.author in players):
            await ctx.send(f"เองอยู่ในเกมแล้วไอเปรด {msg.author}")

        elif (msg.content.lower() == "n") & (msg.author in players):
            players.remove(msg.author)
            if len(players) == 0:
                await ctx.send(f'อ้าวไม่มีคนเล่นละ :( ({len(players)} คน)')
            else:
                await msg.author.send("ชิ่วๆ")
                await ctx.send(f"ตอนนี้เหลือ {' '.join([str(member) for member in players])} ({len(players)} คน); ไปไป๊ {msg.author}")

        elif (msg.content.lower() == "n") & (msg.author not in players):
            await ctx.send(f"เข้าเกมมาก่อนดิค่อยออก {msg.author}")

        elif (msg.content.lower() == 'cancel'):
            await ctx.send('k**y เสียเวลาฉิบหาย')
            return None

        elif (msg.content.lower() == "done") or (len(players) == 9):
            await ctx.send(f"ผู้เล่นทั้งหมดคือ {' '.join([str(member) for member in players])} ถูกมั้ย (y=ใช่,n=แก้ไขจำนวนคนต่อ)")

            while True:
                chk_msg = await client.wait_for("message", check=check)
                if (chk_msg.content.lower() == 'y'):
                    return players
                elif (chk_msg.content.lower() == 'n'):
                    await ctx.send(intro_str)
                    break


def get_random_cards(players) -> Tuple[List[Tuple[int, int]], List[int]]:
    number_to_gen = len(players)*2 + 5
    range_cards = list(range(0, len(DECKS_OF_CARDS)))
    shuffle(range_cards)
    random_numbers = sample(range_cards, number_to_gen)
    middle_cards = random_numbers[-5:]
    player_cards = random_numbers[:-5]

    player_pair_cards = []
    for idx in range(0, len(player_cards), 2):
        pair_cards = tuple((player_cards[idx], player_cards[idx+1]))
        player_pair_cards.append(pair_cards)

    return (player_pair_cards, middle_cards)


def get_random_cards(players) -> Tuple[List[Tuple[int, int]], List[int]]:
    number_to_gen = len(players)*2 + 5
    range_cards = list(range(0, len(DECKS_OF_CARDS)))
    shuffle(range_cards)
    random_numbers = sample(range_cards, number_to_gen)
    middle_cards = random_numbers[-5:]
    player_cards = random_numbers[:-5]

    player_pair_cards = []
    for idx in range(0, len(player_cards), 2):
        pair_cards = tuple((player_cards[idx], player_cards[idx+1]))
        player_pair_cards.append(pair_cards)

    return (player_pair_cards, middle_cards)


async def send_card_msg(players, player_cards: List[Tuple[int, int]]):
    for idx, player in enumerate(players):
        first_card = DECKS_OF_CARDS[player_cards[idx][0]]
        first_card_number, first_card_suit = first_card.split(' ')
        second_card = DECKS_OF_CARDS[player_cards[idx][1]]
        second_card_number, second_card_suit = second_card.split(' ')
        msg = f'คุณได้ไพ่\n {first_card}  |  {second_card}'

        await player.send(msg)


async def three_middle_card_msg(middle_cards: List[int], ctx):
    first_card_msg = DECKS_OF_CARDS[middle_cards[0]]
    second_card_msg = DECKS_OF_CARDS[middle_cards[1]]
    third_card_msg = DECKS_OF_CARDS[middle_cards[2]]

    msg = f'เปิดไพ่\n {first_card_msg}  |  {second_card_msg}  |  {third_card_msg}'

    await ctx.send(msg)
