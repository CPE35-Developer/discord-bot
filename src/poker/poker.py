from typing import List, Tuple
from random import sample, shuffle
from .CheckPriority import winner

from src.poker.user_action import loop_pass_bet_fold
from src.poker.utils import show_middle_card
from src.utils.party import get_players

from .utils import DECKS_OF_CARDS


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


async def who_win(middle_card: List[int], ctx, player_cards: List[Tuple[int, int]], players: List[str], player_status: List[str]) -> List[List[str]]:
    deck = DECKS_OF_CARDS
    all_card_and_name = []
    middle = []

    dic = {
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
        card = ' '
        msg += str(win[i][4]) + ' โดยถือไพ่\n'
        for j in range(len(win[i][2])):
            card += str(dic[win[i][2][j]])+' '+str(win[i][3][j]) + '   '
        msg += card
        msg += '\nคือระดับ ' + win[i][1] + ','
    msg = msg[0:-1]
    await ctx.channel.send(msg)
    return win
    # [[PriorityValue, CardPower, CardInHand, PlayerName, CardFlower],[PriorityValue, CardPower, CardInHand, PlayerName, CardFlower],[PriorityValue, CardPower, CardInHand, PlayerName, CardFlower],...]
    # len() is how many player tie


async def poker_play(bot, ctx):
    players = await get_players(bot, ctx)
    if players is None:
        return
    player_cards, middle_cards = get_random_cards(players)
    print(middle_cards)
    print(player_cards)
    await send_card_msg(players, player_cards)
    await show_middle_card(middle_cards, ctx, False, False)
    players_status = await loop_pass_bet_fold(
        players, player_cards, middle_cards, bot, ctx
    )
    winner = await who_win(
        middle_cards, ctx, player_cards, players, players_status
    )
