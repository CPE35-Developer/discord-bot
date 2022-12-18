from typing import List


def best_card_ofone(card: List[str]):
    '''
    from line 8 to 16
    choose 5 from 7 card
    '''
    best = []
    for i in range(len(card)):
        for j in range(len(card)):
            if i < j:
                tem = []
                for z in range(len(card)):
                    if(z != i and z != j):
                        tem.append(card[z])
                best.append(tem)
    '''
    next callulate the best card that u can have
    from any 5 card pattern
    by priority_value
    '''
    val = []
    for i in range(len(best)):
        val.append(value(best[i]))
    val.sort()
    val.reverse()
    #return is priority(int), howwin(str), dataforsort(list), cards in you hand that u shold choose(list), card flower(list)#
    return val[0]


def winner(win: List[List[str]]):
    player = []
    for i in range(len(win)):
        name = win[i][-1]
        win[i].pop(-1)
        tmp = best_card_ofone(win[i])
        tmp.append(name)
        player.append(tmp)
    player.sort()
    player.reverse()
    playerwin = []
    for i in range(len(player)):
        if(player[0][3] == player[i][3]):
            playerwin.append(player[i])

    # delete some data for sort that not necessary
    for i in range(len(playerwin)):
        playerwin[i].pop(2)

    # return naame,howwin and card that use
    # return [player[0][1],player[0][0][1],player[0][0][3]]
    return playerwin


'''
value(args)  args is set of cards (5card only)
return priotity, typeofwin and somedata when tie
high priority mean good
'''


def value(use: List[str]):
    '''
    code that change card(str) -> card(int)
    and check it flower because only flush, straight flush and royal straight flush that use flower
    '''
    dic = {  # change str to int easily
        ":a:": 14,
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

    temp = []
    flowers = 0
    flushed = 1
    if(len(use) > 0):
        trash, flowers = use[0].split()
    for i in use:
        number, flower = i.split()
        if(flower != flowers):  # check flush here for flush and straight flush
            flushed = 0
        temp.append([dic[number], flower])  # change str to int

    temp.sort()
    use = []
    card_flower = []

    for i in range(len(temp)):
        use.append(temp[i][0])
        card_flower.append(temp[i][1])

    highcard = 0  # 1
    onepair = 0  # 100
    twopair = []  # problem_here #1000
    threeofkind = 0  # 10000
    straight = 0  # 100000
    fullhouse = 0  # 1000000
    flush = 0  # 10000000
    fourofkind = 0  # 100000000
    straightflush = 0  # 1000000000
    royal = 0  # 0
    royaleSF = 0  # 10000000000
    '''
    priority is card number(Ps.(1)=14) plus with number after that line
    callulate priority in line 166 to 222
    '''

    # highcard
    for j in range(len(use)):
        highcard = max(highcard, use[j])

    # Duplicate_Card
    # onepair
    # twopair
    # threeofkind

    # fourofkind

    dupcard2 = []
    skip = 0
    for j in range(len(use)):
        if(skip != 0):
            skip -= 1
            continue
        # fourofkind
        if(j+3 < len(use) and use[j] == use[j+1] == use[j+2] == use[j+3]):
            fourofkind = use[j]
            skip += 3
        # threeofkind
        elif(j+2 < len(use) and use[j] == use[j+1] == use[j+2]):
            threeofkind = use[j]
            skip += 2
        #twopair and onepair
        elif(j+1 < len(use) and use[j] == use[j+1]):
            dupcard2.append(use[j])
            skip += 1

    if(len(dupcard2) == 2):
        twopair.append(dupcard2[0])
        twopair.append(dupcard2[1])
    elif(len(dupcard2) == 1):
        onepair = dupcard2[0]

    # flush
    if(flushed == 1):
        for j in range(len(use)):
            flush = max(flush, use[j])

    # fullhouse
    if(threeofkind != 0 and onepair != 0):
        fullhouse = threeofkind

    # staright
    if(len(use) == 5 and use[0] == use[1]-1 and use[1] == use[2]-1 and use[2] == use[3]-1 and use[3] == use[4]-1):
        straight = use[4]
    elif(len(use) == 5 and use[0] == 10 and use[1] == 11 and use[2] == 12 and use[3] == 13 and use[4] == 14):
        straight = 1
        royal = 1

    if(flush != 0 and straight != 0):
        if(royal == 1):
            royalSF = 1  # royalstrightflush
        else:
            straightflush = straight  # rstrightflush

    # highcard=0 #1
    # onepair=0 #1e2
    # twopair=0 #1e3
    # threeofkind=0 #1e4
    # straight=0 #1e5
    # flush=0 #1e6
    # fullhouse=0 #1e7
    # fourofkind=0 #1e8
    # straightflush=0 #1e9
    # royale=0 #0
    # royaleSF=0 #1e10

    #for return is priority(int), howwin(str), dataforsort(list), cards in you hand that u shold choose(list)#
    if(royaleSF != 0):
        return [1e10, 'royaleSF', [0], use, card_flower]
        # pass
    elif(straightflush != 0):
        if(straight == 1):
            straight = 14
        return [1e9+straightflush, 'straightflush', [0], use, card_flower]
        # pass
    elif(fourofkind != 0):
        if(fourofkind == 1):
            fourofkind = 14
        return [1e8+fourofkind, 'fourofkind', [0], use, card_flower]
        # pass
    elif(fullhouse != 0):
        if(fullhouse == 1):
            fullhouse = 14
        return [1e7+fullhouse, 'fullhouse', [0], use, card_flower]
        # pass
    elif(flush != 0):
        if(flush == 1):
            flush = 14
        return [1e6+flush, 'flush', use, use, card_flower]
        # tie pass
    elif(straight != 0):
        if(straight == 1):
            straight = 14
        return [1e5+straight, 'straight', [0], use, card_flower]
        # pass
    elif(threeofkind != 0):
        if(threeofkind == 1):
            threeofkind = 14
        return [1e4+threeofkind, 'threeofkind', [0], use, card_flower]
        # pass
    elif(len(twopair) != 0):
        left = sum(use)-2*(twopair[0]+twopair[1])
        if(twopair[0] == 1):
            twopair[0] = 14
        return [1e3+twopair[0]+twopair[1]*100, 'twopair', [left], use, card_flower]
        # tie  pass
    elif(onepair != 0):
        tmp = use.copy()
        if(onepair == 1):
            onepair = 14
        for j in range(len(use)):
            if(j+1 < len(use) and use[j] == use[j+1]):
                use.pop(j)
                use.pop(j)
                break
        return [1e2+onepair, 'onepair', use, tmp, card_flower]
        # tie pass
    elif(highcard != 0):
        if(highcard == 1):
            highcard = 14
        return [highcard, 'highcard', use, use, card_flower]
        # tie pass


'''
winner([[CardInHand1,name1],[CardInHand2,name2],[CardInHand3,name3],[CardInHand4,name4],...])
print(winner([[":two: 0",":two: 0",":two: 0",":three: 0",":three: 0",":three: 0",":eight: 0","ixq1"],[":two: 0",":three: 0",":four: 1",":five: 0",":six: 0",":seven: 0",":eight: 0","ixq2"],[":two: 0",":three: 0",":four: 1",":five: 0",":six: 0",":seven: 0",":eight: 0","ixq3"]]))
print -> [[10000003.0, 'fullhouse', [2, 2, 3, 3, 3], 'ixq1']]
'''
