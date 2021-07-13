from typing import List, Tuple
from random import sample, shuffle
from .CheckPriority import winner

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
        second_card = DECKS_OF_CARDS[player_cards[idx][1]]
        msg = f'คุณได้ไพ่\n {first_card}   {second_card}'

        await player.send(msg)


async def show_middle_card(middle_cards: List[int], ctx, show_four: bool, show_five: bool):
    first_card_msg = DECKS_OF_CARDS[middle_cards[0]]
    second_card_msg = DECKS_OF_CARDS[middle_cards[1]]
    third_card_msg = DECKS_OF_CARDS[middle_cards[2]]

    msg = f'เปิดไพ่\n {first_card_msg}   {second_card_msg}   {third_card_msg}'

    if show_four:
        four_card_msg = DECKS_OF_CARDS[middle_cards[3]]
        msg += '   ' + four_card_msg
    if show_five:
        five_card_msg = DECKS_OF_CARDS[middle_cards[4]]
        msg += '   ' + five_card_msg

    await ctx.send(msg)


async def who_win(middle_card: List[int], ctx, player_cards: List[Tuple[int, int]], players: List[str], player_status: List[str]) -> List[List[str]]:
    deck = DECKS_OF_CARDS
    all_card_and_name = []
    middle = []

    dic={
        2: ":two:",
        3: ":three:",
        4: ":four:",
        5: ':five:',
        6: ':six:',
        7: ':seven:',
        8: ':eight:',
        9: ':nine:',
        10: ':one::zero:',
        11: ':regional_indicator_j:',
        12: ':regional_indicator_q:',
        13: ':regional_indicator_k:',
        14: ':a:'
    }

    for i in middle_card:
        middle.append(deck[i])

    for i in range(len(players)):
        if(player_status[i] != 'f'):
            tmp = middle.copy()
            tmp.append(deck[player_cards[i][0]])
            tmp.append(deck[player_cards[i][1]])
            tmp.append(players[i])
            all_card_and_name.append(tmp)

    win = winner(all_card_and_name)
    print(win)

    msg = f'\nผู้ชนะมี {len(win)} คน คือ '
    for i in range(len(win)):
        card=' '
        msg += str(win[i][4]) + ' โดยถือไพ่\n' 
        for j in range(len(win[i][2])):
            card += str(dic[win[i][2][j]])+' '+str(win[i][3][j]) + '   '
        msg += card
        msg +=  '\nคือระดับ ' + win[i][1] + ','
    msg = msg[0:-1]
    await ctx.send(msg)
    return win
    # [[PriorityValue, CardPower, CardInHand, PlayerName, CardFlower],[PriorityValue, CardPower, CardInHand, PlayerName, CardFlower],[PriorityValue, CardPower, CardInHand, PlayerName, CardFlower],...]
    # len() is how many player tie
