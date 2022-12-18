import discord
import discord_slash
from discord.activity import Game
from typing import List
from src.utils.party import get_players
from src.utils.member import getNick
from random import shuffle, choice
from itertools import chain

BOT = None


class Rock:
    emoji = '✊'
    name = 'rock'


class Paper:

    emoji = '✋'
    name = 'paper'


class Scissors:

    emoji = '✌️'
    name = 'scissors'


class Timeout:
    emoji = '⏰'
    name = 'timeout'


class BotPlayer:

    def __init__(self):
        self.member = BOT.user
        self.name = self.nick = BOT.user.name
        self.bot = True

    def getChoice(self):
        self.choice = choice([Rock, Paper, Scissors])


class Player:

    def __init__(self, player: discord.Member = None):
        self.member = player
        self.name = player.name
        self.nick = getNick(player)
        self.bot = False

    async def getChoice(self, mode: str = 'mp', ctx: discord_slash.SlashContext = None) -> discord.Message:

        if mode == 'mp':
            message = await self.member.send('Rock, Paper or Scissors?')
        elif mode == 'sp' and ctx is not None:
            message = await ctx.channel.send('Rock, Paper or Scissors?')
        elif mode == 'sp' and ctx is None:
            raise SyntaxError("Please specify the parameter named 'ctx'.")

        await message.add_reaction(Rock.emoji)
        await message.add_reaction(Paper.emoji)
        await message.add_reaction(Scissors.emoji)

        def check(reaction, user):
            return not user.bot and str(
                reaction.emoji) in [Rock.emoji, Paper.emoji, Scissors.emoji]

        while True:
            try:
                reaction, reaction_user = await BOT.wait_for("reaction_add", timeout=15.0, check=check)

                if mode == 'sp' and reaction_user != self.member:
                    await ctx.channel.send(f"yar suek {reaction_user.mention}", tts=True, delete_after=5)
                    continue

                if str(reaction.emoji) == Rock.emoji:
                    self.choice = Rock
                    break

                if str(reaction.emoji) == Paper.emoji:
                    self.choice = Paper
                    break

                if str(reaction.emoji) == Scissors.emoji:
                    self.choice = Scissors
                    break
            except:
                await message.delete()
                message = await self.member.send('TIMEOUT SAD')
                self.choice = Timeout
                break
        return message


def getWinner(p1=Player, p2=Player) -> Player:

    if p1.choice == p2.choice:
        winner = None
    elif p1.choice == Rock and p2.choice == Scissors:
        winner = p1
    elif p1.choice == Paper and p2.choice == Rock:
        winner = p1
    elif p1.choice == Scissors and p2.choice == Paper:
        winner = p1
    else:
        winner = p2

    return winner


def embedTornament(matches: List[List[Player]], round: int) -> discord.Embed:

    embed_tornament = discord.Embed(
        title=f"เป่ายิ่งฉุบ Tornament Round #{round}")

    for ind, match in enumerate(matches):

        try:
            p1, p2 = match
            embed_tornament.add_field(
                name=f"Match #{str(ind+1)}", value=f"{p1.nick} vs {p2.nick}", inline=False)

        except:
            player = match[0]
            embed_tornament.add_field(
                name="Excess player", value=player.nick, inline=False)

    return embed_tornament


def embedMatch(p1: Player, p2: Player, match_num: int = None, winner=None, timeout=None) -> discord.Embed:

    if match_num is not None:
        em_match = discord.Embed(title=f"Match #{match_num}")
    else:
        em_match = discord.Embed(title=f"{p1.nick} vs {p2.nick}")

    if timeout is not None:
        if timeout == p1:
            em_match.add_field(name=p1.nick, value=p1.choice.emoji)
            em_match.add_field(name=p2.nick, value='-')
            em_match.add_field(
                name="Result", value=f"{winner.nick} is the winner!")

        elif timeout == p2:
            em_match.add_field(name=p1.nick, value='-')
            em_match.add_field(name=p2.nick, value=p2.choice.emoji)
            em_match.add_field(
                name="Result", value=f"{winner.nick} is the winner!")

        return em_match

    try:
        em_match.add_field(name=p1.nick, value=p1.choice.emoji)
        em_match.add_field(name=p2.nick, value=p2.choice.emoji)
        em_match.add_field(
            name="Result", value=f"{winner.nick} is the winner!" if winner is not None else "Tie")

    except:
        em_match.add_field(name=p1.nick, value='-')
        em_match.add_field(name=p2.nick, value='-')

    return em_match


class RockPaperScissors:

    async def PlaySP(bot: discord.Client, ctx: discord_slash.SlashContext):
        global BOT
        BOT = bot

        player = Player(ctx.author)
        opponent = BotPlayer()

        winner = None
        msg_match = await ctx.send(embed=embedMatch(player, opponent))
        while winner is None:

            choice_msg = await player.getChoice('sp', ctx)

            if player.choice == Timeout:
                winner = opponent
                await msg_match.edit(embed=embedMatch(player, opponent, winner=winner, timeout=player))
                await choice_msg.delete()
                break

            opponent.getChoice()

            winner = getWinner(player, opponent)

            await msg_match.edit(embed=embedMatch(player, opponent, winner=winner))

            await choice_msg.delete()

    async def PlayMP(bot: discord.Client, ctx: discord_slash.SlashContext) -> None:

        def getMatches(players: List[Player]) -> List[List[Player]]:
            shuffle(players)
            return [players[i*2:(i+1)*2] for i in range(0, -(-len(players)//2))]

        global BOT
        BOT = bot

        players = [Player(member) for member in await get_players(BOT, ctx)]

        matches = getMatches(players)

        round = 1
        endround = len(matches)+1
        while round != endround:

            matches = getMatches(list(chain(*matches)))

            await ctx.channel.send(embed=embedTornament(matches, round))
            for player in players:
                await player.member.send(embed=embedTornament(matches, round))

            for ind, match in enumerate(matches):
                winner = None

                if len(match) == 2:

                    p1, p2 = match

                    msg_match = [await ctx.channel.send(embed=embedMatch(p1, p2, ind+1)),
                                 await p1.member.send(embed=embedMatch(p1, p2, ind+1)),
                                 await p2.member.send(embed=embedMatch(p1, p2, ind+1))]

                    while winner is None:

                        msg_turn = await ctx.channel.send(content=f"It's {p1.member.mention} turn. Check your PM! {p1.nick}")

                        p1_msg = await p1.getChoice()
                        if p1.choice == Timeout:
                            winner = p2
                            for msg in msg_match:
                                await msg.edit(embed=embedMatch(p1, p2, ind+1, winner, timeout=p1))
                            await msg_turn.delete()
                            break

                        await msg_turn.edit(content=f"It's {p2.member.mention} turn. Check your PM {p2.nick}!")
                        p2_msg = await p2.getChoice()
                        if p2.choice == Timeout:
                            winner = p1
                            for msg in msg_match:
                                await msg.edit(embed=embedMatch(p1, p2, ind+1, winner, timeout=p2))
                            await msg_turn.delete()
                            break

                        if winner is None:
                            winner = getWinner(p1, p2)
                            for msg in msg_match:
                                await msg.edit(embed=embedMatch(p1, p2, ind+1, winner))
                            await msg_turn.delete()

                        for choice_msg in [p1_msg, p2_msg]:
                            await choice_msg.delete()

                        if p1.choice == Timeout and p2.choice == Timeout:
                            await msg_turn.delete()
                            break

                    if winner is not None:
                        winner.choice = None
                        matches[ind] = [winner]
                    else:
                        matches[ind] = []

            round += 1
