from typing import List, Tuple


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

    await ctx.channel.send(msg)
