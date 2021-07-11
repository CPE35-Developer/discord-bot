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
        msg = f'คุณได้ไพ่\n {first_card}   {second_card}'

        await player.send(msg)


async def three_middle_card_msg(middle_cards: List[int], ctx):
    first_card_msg = DECKS_OF_CARDS[middle_cards[0]]
    second_card_msg = DECKS_OF_CARDS[middle_cards[1]]
    third_card_msg = DECKS_OF_CARDS[middle_cards[2]]

    msg = f'เปิดไพ่\n {first_card_msg}   {second_card_msg}   {third_card_msg}'

    await ctx.send(msg)


async def loop_pass_bet_fold(players, player_cards: List[Tuple[int, int]], client, ctx):
    players_left = players.copy()
    players_card_left = player_cards.copy()
    max_current_bet = -1

    def check_pbf(msg):
        return msg.author == player and msg.channel == ctx.channel and \
            msg.content.lower() in ["p", "b", "f"]

    def check_bet(msg_bet):
        return msg_bet.author == msg_author and msg_bet.author in players_left

    players_status = []
    await ctx.send('เข้าสู่ขั้นตอนการ bet\nพิม P หรือ p เพื่อผ่าน\nB หรือ b เพื่อลงแต้มเพิ่ม\nF หรือ f เพื่อหมอบ')

    for play_time in range(2, 5):
        global player
        for idx_player, player in enumerate(players_left):
            global msg_author
            await ctx.send(f'คุณ {str(player)} โปรดเลือก P/B/F')
            msg = await client.wait_for('message', check=check_pbf)
            msg_content = msg.content.lower()
            msg_author = msg.author

            if msg_content == 'f':  # หมอบ
                players_left.pop(idx_player)
                players_card_left.pop(idx_player)

                # I DONT KNOW
                # if len(players_status) < idx_player:
                # players_status.pop(idx_player)

            elif msg_content == 'p':
                players_status[idx_player] = 'p'

            elif msg_content == 'b':
                while True:
                    await ctx.send(f'คุณ {str(player)} โปรดเดิมพัน')

                    msg_bet = await client.wait_for('message', check=check_bet)

                    msg_bet_content = msg_bet.content

                    if not msg_bet_content.isnumeric():
                        await ctx.send(f'โปรดใช้ตัวเลข')
                        continue
                    if int(msg_bet_content) < max_current_bet:
                        await ctx.send(f'โปรดเดิมพันให้สูงกว่า {max_current_bet}')
                        continue

                    max_current_bet = int(msg_bet_content)
                    await ctx.send(f'คุณ {str(msg_bet.author)} ได้เดิมพันเพิ่มเป็น {max_current_bet}')
                    print('hello world')
                    break

    return players_left, players_card_left


def change_cardsidx_to_str(middle_card: List[int],player_cards: List[Tuple[int,int]],player: List[str]):
    deck=DECKS_OF_CARDS
    all_card_and_name=[]
    middle=[]

    for i in middle_card:
        middle.append(deck[i])

    for i in range(len(player)):
        tem=middle
        tem.append(deck[player_cards[i][0]])
        tem.append(deck[player_cards[i][1]])
        tem.append(player[i])
        all_card_and_name.append(tem)

    return all_card_and_name