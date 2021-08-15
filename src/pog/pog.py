from typing import List, Tuple
from random import sample, shuffle


from src.utils.party import get_players

from .utils import DECKS_OF_CARDS


def get_random_cards(players) -> Tuple[List[Tuple[int, int]], List[int]]:
    
    number_to_gen = len(players)*3
    range_cards = list(range(0, len(DECKS_OF_CARDS)))
    shuffle(range_cards)
    random_numbers = sample(range_cards, number_to_gen)
    player_cards = random_numbers

    player_triple_cards = []
    for idx in range(0, len(player_cards), 3):
        triple_cards = tuple((player_cards[idx], player_cards[idx+1],player_cards[idx+2]))
        player_triple_cards.append(triple_cards)

    return (player_triple_cards)


async def send_card_msg(players, player_cards: List[Tuple[int, int]]):
    for idx, player in enumerate(players):
        first_card = DECKS_OF_CARDS[player_cards[idx][0]]
        second_card = DECKS_OF_CARDS[player_cards[idx][1]]
        third_card = DECKS_OF_CARDS[player_cards[idx][2]]
        msg = f'*#*#*#*#\n\nคุณได้ไพ่\n {first_card}   {second_card}'

        await player.send(msg)

async def get_head_players(bot, ctx, players):
    
    async def print_players_list(players):
        for i, item in enumerate(players, start=0):
            await ctx.channel.send(f"{i}:{item}")

    intro_str = 'พิมพ์หมายเลขของคนที่ต้องการเป็นเจ้ามือ'
    # ให้ bot ส่งคำแนะนำเข้า text channel
    await print_players_list(players)
    await ctx.channel.send(intro_str)

    def check(msg):
        return msg.channel == ctx.channel and \
            msg.content in listword
    while True:
        listword=[]
        for i in range(len(players)):listword.append(str(i))
        msg =await  bot.wait_for("message", check=check)
        if (msg.content in listword):
            index_of_bighand=msg.content
            await ctx.channel.send(f"เจ้ามือคือ {str(players[int(msg.content)])} ถูกมั้ย (y=ใช่,n=เปลี่ยนเจ้ามือ)")

            while True:
                listword=["y","n","Y","N"]
                chk_msg = await bot.wait_for("message", check=check)
                if (chk_msg.content.lower() == 'y'):
                    return index_of_bighand
                elif (chk_msg.content.lower() == 'n'):
                    await print_players_list(players)
                    await ctx.channel.send(intro_str)
                    break

async def call_card(bot, ctx, players,player_cards,index_of_bighand):
    
    await ctx.channel.send('เข้าสู่ขั้นตอนการเรียก\nพิม P หรือ p เพื่อผ่าน\nC หรือ c เพื่อเรียกไพ่เพิ่ม')
    def check_cc(msg):
        return msg.author == player and msg.channel == ctx.channel and \
            msg.content.lower() in ["c", "p"]
    player_status = []
    for i in range(len(players)):
        player=players[i]
        if i==int(index_of_bighand) : continue
        await ctx.channel.send(f'คุณ {str(player)} โปรดเลือก P/C')
        msg = await bot.wait_for('message', check=check_cc)
        msg_content = msg.content.lower()
        third_card = DECKS_OF_CARDS[player_cards[i][2]]
        if msg_content == 'p':  

            player_status.append('p')
            await ctx.channel.send(f'{str(player)} ผ่าน')


        elif msg_content == 'c':
            player_status.append('c')
            msg = f'คุณได้ไพ่\n {third_card}'

            await ctx.channel.send(f'{str(player)} เรียก')
            await player.send(msg)
    player=players[int(index_of_bighand)]
    await ctx.channel.send(f'เจ้ามือ {str(player)} โปรดเลือก P/C')
    msg = await bot.wait_for('message', check=check_cc)
    msg_content = msg.content.lower()
    third_card = DECKS_OF_CARDS[player_cards[i][2]]
    if msg_content == 'p':  

        player_status.insert(int(index_of_bighand),'p')
        await ctx.channel.send(f'{str(player)} ผ่าน')


    elif msg_content == 'c':
        player_status.insert(int(index_of_bighand),'c')
        msg = f'คุณได้ไพ่\n {third_card}'

        await ctx.channel.send(f'{str(player)} เรียก')
        await player.send(msg)
    return player_status




async def score_cards(players,player_status,player_cards):
    
    score =[[0,0,0,0]]* len(players)#score=[ป็อก,ความพิเศษ,แต้ม,เด้ง,id]
    dic = { ":a:": 1,
        ":two:": 2,
        ":three:": 3,
        ":four:": 4,
        ":five:": 5,
        ":six:": 6,
        ":seven:": 7,
        ":eight:": 8,
        ":nine:": 9,
        ":one::zero:": 10,
        ":regional_indicator_j:": 110,
        ":regional_indicator_q:": 120,
        ":regional_indicator_k:": 130,

    }
    dic2 = { ":a:": 14,
        ":two:": 2,
        ":three:": 3,
        ":four:": 4,
        ":five:": 5,
        ":six:": 6,
        ":seven:": 7,
        ":eight:": 8,
        ":nine:": 9,
        ":one::zero:": 10,
        ":regional_indicator_j:": 11,
        ":regional_indicator_q:": 12,
        ":regional_indicator_k:": 13,

    }

    listscore=[]
    for i in range(len(players)):
       
        sumofnum=0
        
        if player_status[i] =='p':
            cards=[]
            cards.append(DECKS_OF_CARDS[int(player_cards[i][0])].split())
            cards.append(DECKS_OF_CARDS[int(player_cards[i][1])].split())
            sumofnum=(int(dic[cards[0][0]])+int(dic[cards[1][0]]))
            score[i][2]=sumofnum%10
            if score[i][2]== 8 or score[i][2] == 9 : score[i][0]=score[i][2]
            if cards[0][1]==cards[1][1]: score[i][3]=2
            if cards[0][0]==cards[1][0]: score[i][3]=2
            listscore.append(score[i].copy())
            print(score[i])
            
        else:
            cards=[]
            cards.append(DECKS_OF_CARDS[int(player_cards[i][0])].split())
            cards.append(DECKS_OF_CARDS[int(player_cards[i][1])].split())
            cards.append(DECKS_OF_CARDS[int(player_cards[i][2])].split())
            sumofnum=(int(dic[cards[0][0]]))+int(dic[(cards[1][0])])+int(dic[(cards[2][0])])
            score[i][2]=sumofnum%10
            sortcard=sorted(list((dic2[cards[0][0]],dic2[cards[1][0]],dic2[cards[2][0]])))
            if [cards[0][0],cards[1][0],cards[2][0]] in [":regional_indicator_j:",":regional_indicator_q:",":regional_indicator_k:"]:score[i][1]=3
            elif (sortcard[2]-sortcard[0]==2 and sortcard[0]!= sortcard[1] !=sortcard[2]):score[i][1]=3
            if cards[0][0]==cards[1][0]==cards[2][0] :score[i][1]=5
            listscore.append(score[i].copy())
            print(score[i])
    
    print ("listscore = ",listscore)
    return listscore


'''
2  ได้สองเด้ง หมายถึงไพ่ทั้งหมดในมือมีสองใบ โดยที่ สองใบนั้นเป็นไพ่ดอกเดียวกันหรือตัวเลขเหมือนกัน ถ้าแต้มชนะ จะ ได้เดิมพันเป็นสองเท่า
3  ได้สามเด้ง หมายถึงไพ่ทั้งหมดในมือมีสามใบ โดยที่ สามใบนั้นเป็นไพ่ดอกเดียวกัน ถ้าแต้มชนะ จะ ได้เดิมพันเป็นสามเท่า
สามเหลืองหรือกระเบื้อง หมายถึงไพ่สามใบเป็นไพ่ในกลุ่ม J Q K ทั้งสามใบ ถือว่ามีแต้มเหนือ เก้า (ที่ไม่ใช่ป๊อกเก้า) ถ้าชนะ จะ ได้เดิมพันเป็นสามเท่า
ตอง หมายถึง ไพ่สามใบในมือ เป็นเลขเดียวกันทั้งสามใบ ถือว่ามีแต้มเหนือ เก้า (ที่ไม่ใช่ป๊อกเก้า) และสามเหลือง ถ้าชนะ จะ ได้เดิมพันเป็นห้าเท่า
########3 เรียง หมายถึง ไพ่สามใบในมือมีแต้มเรียงกัน เช่นไพ่สามใบคือ 2 3 4 หรือ 5 6 7 หรือ Q K A ( ถ้า K A 2 หรือ A 2 3 ถือว่าไม่เรียงเพราะถือว่า 2 มีค่าต่ำสุด และ A มีค่าสูงสุด ดังนั้นจะเรียงวกกลับมาไม่ได้) ถ้าชนะ จะได้เดิมพันเป็นสามเท่า
'''

async def check_winner(ctx, players,player_status,index_of_bighand,listscore,player_cards):
    await ctx.channel.send(':partying_face: \n:partying_face: \n*#*#*#*#  จบตาแล้วงับ ใครชนะใครแพ้มาดูกันเล้ยยย  *#*#*#*#\n:partying_face: \n:partying_face: ')
    if player_status[int(index_of_bighand)]=="p":
        await ctx.channel.send(f"เจ้ามือ{str(players[int(index_of_bighand)])}ถือไพ่ {DECKS_OF_CARDS[player_cards[int(index_of_bighand)][0]]}   {DECKS_OF_CARDS[player_cards[int(index_of_bighand)][1]]}")
    else: await ctx.channel.send(f"เจ้ามือ{str(players[int(index_of_bighand)])}ถือไพ่ {DECKS_OF_CARDS[player_cards[int(index_of_bighand)][0]]}   {DECKS_OF_CARDS[player_cards[int(index_of_bighand)][1]]}   {DECKS_OF_CARDS[player_cards[int(index_of_bighand)][2]]}")
    print(players)
    print(player_status)
    print(listscore)
    print(player_cards)
    print(len(players))
    
    for i in range(len(players)):
        print(i)
        if i == int(index_of_bighand):
            print("continue")
            continue

        if listscore[i]>listscore[int(index_of_bighand)]: 
            print("w")
            if player_status[i]=="p":await ctx.channel.send(f"{str(players[i])}  ชนะเจ้ามือ โดยถือไพ่ {DECKS_OF_CARDS[player_cards[i][0]]}   {DECKS_OF_CARDS[player_cards[i][1]]}")
            elif player_status[i]=="c":await ctx.channel.send(f"{str(players[i])}  ชนะเจ้ามือ โดยถือไพ่ {DECKS_OF_CARDS[player_cards[i][0]]}   {DECKS_OF_CARDS[player_cards[i][1]]}   {DECKS_OF_CARDS[player_cards[i][2]]}")
        elif listscore[i]<listscore[int(index_of_bighand)]: 
            print("l")
            if player_status[i]=="p":await ctx.channel.send(f"{str(players[i])}  แพ้เจ้ามือ โดยถือไพ่ {DECKS_OF_CARDS[player_cards[i][0]]}   {DECKS_OF_CARDS[player_cards[i][1]]}")
            elif player_status[i]=="c":await ctx.channel.send(f"{str(players[i])}  แพ้เจ้ามือ โดยถือไพ่ {DECKS_OF_CARDS[player_cards[i][0]]}   {DECKS_OF_CARDS[player_cards[i][1]]}   {DECKS_OF_CARDS[player_cards[i][2]]}")
        else:
            print("d")
            if player_status[i]=="p":await ctx.channel.send(f"{str(players[i])}  เสมอกับเจ้ามือ โดยถือไพ่ {DECKS_OF_CARDS[player_cards[i][0]]}   {DECKS_OF_CARDS[player_cards[i][1]]}")
            elif player_status[i]=="c":await ctx.channel.send(f"{str(players[i])}  เสมอกับเจ้ามือ โดยถือไพ่ {DECKS_OF_CARDS[player_cards[i][0]]}   {DECKS_OF_CARDS[player_cards[i][1]]}   {DECKS_OF_CARDS[player_cards[i][2]]}")
    

async def replay(bot,ctx, players,player_cards,player_status,index_of_bighand,listscore):
    intro_str = 'ต้องการเล่นอีกรอบปล่าวงับ y/n'
    # ให้ bot ส่งคำแนะนำเข้า text channel
    await ctx.channel.send(intro_str)
    
    def check(chk_msg):
        return chk_msg.channel == ctx.channel and \
            chk_msg.content.lower() in ["y","n"]
    while True:
        chk_msg = await bot.wait_for("message", check=check)
        if (chk_msg.content.lower() == 'y'):
            player_cards= get_random_cards(players)
            print(player_cards)
            await send_card_msg(players, player_cards)
            player_status= await call_card(bot, ctx, players,player_cards,index_of_bighand)
            listscore = await score_cards(players,player_status,player_cards)
            print(listscore)
            await check_winner(ctx, players,player_status,index_of_bighand,listscore,player_cards)
            await replay(bot,ctx, players,player_cards,player_status,index_of_bighand,listscore)

        elif (chk_msg.content.lower() == 'n'):
            return 
                   


async def pog_play(bot, ctx):
    players = await get_players(bot, ctx)
    if players is None:
        return
    index_of_bighand=await get_head_players(bot, ctx, players)
    player_cards= get_random_cards(players)
    print(player_cards)
    await send_card_msg(players, player_cards)
    player_status= await call_card(bot, ctx, players,player_cards,index_of_bighand)
    listscore = await score_cards(players,player_status,player_cards)
    print(listscore)
    await check_winner(ctx, players,player_status,index_of_bighand,listscore,player_cards)
    await replay(bot,ctx, players,player_cards,player_status,index_of_bighand,listscore)
