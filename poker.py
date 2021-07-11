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
