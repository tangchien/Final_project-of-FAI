import random
import agents.tbe as tbe
royal_flush = 13*9
straight_flush = 13*8
four_a_kind = 13*7
full_house = 13*6
flush = 13*5
straight = 13*4
three_a_kind = 13*3
two_pair = 13*2
one_pair = 13
woolong = 0

# final score = (type) + (max card)
eng2num = {'A':12, '2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11}

def generate_a_card():
    total_card = []
    #generate total card
    flower = ['S', 'H', 'D', 'C']
    nbs = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    for i in range(4):
        for j in range(13):
            total_card.append((flower[i]+nbs[j]))
    # random.shuffle(total_card)
    return total_card

def combination(n: int, m: int) -> int:
    if (m > (n//2)):
        m = n-m
    top = 1 ; bot = 1
    for i in range(m):
        top *= (n-i)
        bot *= (m-i)
    return top//bot
    
def classify(finalcards : list) -> int:
    spade = [] ; heart = [] ; diamond = [] ; club = []
    exist_num = []
    for i in finalcards:        #   parser
        #   flower count
        if (i[0] == 'S'):   
           spade.append(eng2num[i[1]]) 
        elif (i[0] == 'H'):   
            heart.append(eng2num[i[1]])
        elif (i[0] == 'D'):
            diamond.append(eng2num[i[1]])
        else              :
            club.append(eng2num[i[1]])
        exist_num.append(eng2num[i[1]])
    
    spade.sort() ; heart.sort() ; diamond.sort() ; club.sort() ; exist_num.sort()
    
    #   royal flush
    if ('S10' in finalcards and 'SJ' in finalcards and 'SQ' in finalcards and 'SK' in finalcards and 'SA' in finalcards):
        return royal_flush
    elif ('H10' in finalcards and 'HJ' in finalcards and 'HQ' in finalcards and 'HK' in finalcards and 'HA' in finalcards):
        return royal_flush
    elif ('D10' in finalcards and 'DJ' in finalcards and 'DQ' in finalcards and 'DK' in finalcards and 'DA' in finalcards):
        return royal_flush
    elif ('C10' in finalcards and 'CJ' in finalcards and 'CQ' in finalcards and 'CK' in finalcards and 'CA' in finalcards):
        return royal_flush
    else : pass

    #   straight flush 
    if (len(spade) >= 5):
        cnt = 1
        for i in range(len(spade)-1):
            if (spade[i+1]-spade[i] != 1):
                if (cnt >= 5):
                    return straight_flush+spade[i]
                cnt = 1
            else:
                cnt += 1
                if (i == len(spade)-2 and cnt >= 5):
                    return straight_flush+spade[-1]
    elif (len(heart) >= 5):
        cnt = 1
        for i in range(len(heart)-1):
            if (heart[i+1]-heart[i] != 1):
                if (cnt >= 5):
                    return straight_flush+heart[i]
                cnt = 1
            else:
                cnt += 1
                if (i == len(heart)-2 and cnt >= 5):
                    return straight_flush+heart[-1]
    elif (len(diamond) >= 5):
        cnt = 1
        for i in range(len(diamond)-1):
            if (diamond[i+1]-diamond[i] != 1):
                if (cnt >= 5):
                    return straight_flush+diamond[i]
                cnt = 1
            else:
                cnt += 1
                if (i == len(diamond)-2 and cnt >= 5):
                    return straight_flush+diamond[-1]
                
    elif (len(club) >= 5):
        cnt = 1
        for i in range(len(club)-1):
            if (club[i+1]-club[i] != 1):
                if (cnt >= 5):
                    return straight_flush+club[i]
                cnt = 1
            else:
                cnt += 1
                if (i == len(club)-2 and cnt >= 5):
                    return straight_flush+club[-1]
    else:
        pass
    
    #   count pair
    pair_count = []         #   (amount, number)
    max_samekind = 1 ; temp_samekind = 1
    for i in range(1, len(exist_num)):
        if (exist_num[i] == exist_num[i-1]):
            temp_samekind += 1
            if (temp_samekind > max_samekind):
                max_samekind = temp_samekind
        else:
            pair_count.append((temp_samekind, exist_num[i-1]))
            temp_samekind = 1
    pair_count.append((temp_samekind, exist_num[-1]))
    pair_count.sort()
    pair_count.reverse()

    #   four a kind 
    if (pair_count[0][0] == 4):
        return four_a_kind+pair_count[0][1]

    #   full house
    if (pair_count[0][0] == 3 and pair_count[1][0] >= 2):
        return full_house+pair_count[0][1]

    #   flush
    if (len(spade) >= 5):   return flush+spade[-1]
    if (len(heart) >= 5):   return flush+heart[-1]
    if (len(diamond) >= 5): return flush+diamond[-1]
    if (len(club) >= 5):    return flush+club[-1]

    #   straight
    cnt = 1
    for i in range(len(exist_num)-1):
        if (exist_num[i+1]-exist_num[i] != 1):
            if (cnt >= 5):
                return straight+exist_num[i]
            cnt = 1
        else:
            cnt += 1
            if (i == len(exist_num)-2 and cnt >= 5):
                return straight+exist_num[-1]
    
    #   three a kind
    if (pair_count[0][0] == 3):
        return three_a_kind+pair_count[0][1]
    
    #   two pair
    if (pair_count[0][0] == 2 and pair_count[1][0] == 2):
        return two_pair+pair_count[0][1]
    
    #   pair
    if (pair_count[0][0] == 2):
        return one_pair+pair_count[0][1]
    
    #   woolon
    return exist_num[-1]

def evaluate_win_rate(hold_cards : list, times : int) -> None:
    cards = generate_a_card()
    for c in hold_cards:
        cards.remove(c)
    f3 = 0 ; f4 = 0 ; f5 = 0
    for step in range(times):
        random.shuffle(cards)
        three = 0 ; four = 0 ; five = 0
        for j in range(10000):
            #   two card + three community card
            # my_score1 = classify(hold_cards+cards[:3]) 
            # opponent1 = classify(cards[:5])
            # if (my_score1 > opponent1):
            #     three += 1

            # #   two cards + four community card
            # my_score2 = classify(hold_cards+cards[:4])
            # opponent2 = classify(cards[:6])
            # if (my_score2 > opponent2):
            #     four += 1

            #   two cards + five community card
            my_score3 = classify(hold_cards+cards[:5])
            opponent3 = classify(cards[:7])
            if (my_score3 > opponent3):
                five += 1
        # f3 += three/10000
        # f4 += four/10000
        f5 += five/10000
    # print("2+3 win rate = ", f3/times)
    # print("2+4 win rate = ", f4/times)
    print(hold_cards, " win rate  = ", f5/times)

def find_type(holds_cards : list) -> float:
    #   pair
    if (holds_cards[0][1] == holds_cards[1][1]):
        return tbe.pr[holds_cards[0][1]]
    #   flush
    if (holds_cards[0][0] == holds_cards[1][0]):
        if (holds_cards[0][1] == 'A'):
            return tbe.flh[(holds_cards[0][1], holds_cards[1][1])]
        elif (holds_cards[1][1] == 'A'):
            return tbe.flh[(holds_cards[1][1], holds_cards[0][1])]
        elif (eng2num[holds_cards[1][1]] > eng2num[holds_cards[0][1]]):
            return tbe.flh[(holds_cards[0][1], holds_cards[1][1])]
        else:
            return tbe.flh[(holds_cards[1][1], holds_cards[0][1])]
    #   able to be straight
    if ((abs(eng2num[holds_cards[0][1]]-eng2num[holds_cards[1][1]]) < 5) or (abs(eng2num[holds_cards[0][1]]-eng2num[holds_cards[1][1]]) > 8 and (eng2num[holds_cards[0][1]] == 12 or eng2num[holds_cards[1][1]] == 12))):
        if (holds_cards[0][1] == 'A' and eng2num[holds_cards[1][1]] < 4):
            return tbe.stt[(holds_cards[0][1], holds_cards[1][1])]
        elif (holds_cards[1][1] == 'A' and eng2num[holds_cards[0][1]] < 4):
            return tbe.stt[(holds_cards[1][1], holds_cards[0][1])]
        elif (eng2num[holds_cards[0][1]] > eng2num[holds_cards[1][1]]):
            return tbe.stt[(holds_cards[1][1], holds_cards[0][1])]
        else:
            return tbe.stt[(holds_cards[0][1], holds_cards[1][1])]
    else:
        if (holds_cards[0][1] == 'A'):
            return tbe.wlg[(holds_cards[0][1], holds_cards[1][1])]
        elif (holds_cards[1][1] == 'A'):
            return tbe.wlg[(holds_cards[1][1], holds_cards[0][1])]
        elif (eng2num[holds_cards[0][1]] > eng2num[holds_cards[1][1]]):
            return tbe.wlg[(holds_cards[1][1], holds_cards[0][1])]
        else:
            return tbe.wlg[(holds_cards[0][1], holds_cards[1][1])]

def evl_rate(mc : list, com : list) -> float:
    if (len(com) == 0):
        return find_type(mc)
    cards = generate_a_card()
    cards.remove(mc[0])
    cards.remove(mc[1])
    for i in com:
        cards.remove(i)
    ret_val = 0
    for i in range(7):
        win = 0
        for j in range(10000):
            random.shuffle(cards)
            if (classify(mc+com) > classify(com+cards[:2])):
                win += 1
        ret_val += (win/10000)
    return (ret_val/7)
        
my_cards = [
    #   pair
    ['SA', 'HA'], ['S2', 'H2'], ['S3', 'H3'], ['S4', 'H4'], ['S5', 'H5'], ['S6', 'H6'], ['S7', 'H7'], ['S8', 'H8'], ['S9', 'H9'],
    ['S10', 'H10'], ['SJ', 'HJ'], ['SQ', 'HQ'], ['SK', 'HK'],
    #   flush
    ['SA', 'S2'], ['SA', 'S3'], ['SA', 'S4'], ['SA', 'S5'], ['SA', 'S6'], ['SA', 'S7'], ['SA', 'S8'], ['SA', 'S9'], ['SA', 'S10'], ['SA', 'SJ'], ['SA', 'SQ'], ['SA', 'SK'], ['S2', 'S3'], ['S2', 'S4'], ['S2', 'S5'], ['S2', 'S6'], ['S2', 'S7'], ['S2', 'S8'], ['S2', 'S9'], ['S2', 'S10'], ['S2', 'SJ'], ['S2', 'SQ'], ['S2', 'SK'], ['S3', 'S4'], ['S3', 'S5'], ['S3', 'S6'], ['S3', 'S7'], ['S3', 'S8'], ['S3', 'S9'], ['S3', 'S10'], ['S3', 'SJ'], ['S3', 'SQ'], ['S3', 'SK'], ['S4', 'S5'], ['S4', 'S6'], ['S4', 'S7'], ['S4', 'S8'], ['S4', 'S9'], ['S4', 'S10'], ['S4', 'SJ'], ['S4', 'SQ'], ['S4', 'SK'], ['S5', 'S6'], ['S5', 'S7'], ['S5', 'S8'], ['S5', 'S9'], ['S5', 'S10'], ['S5', 'SJ'], ['S5', 'SQ'], ['S5', 'SK'], ['S6', 'S7'], ['S6', 'S8'], ['S6', 'S9'], ['S6', 'S10'], ['S6', 'SJ'], ['S6', 'SQ'], ['S6', 'SK'], 
['S7', 'S8'], ['S7', 'S9'], ['S7', 'S10'], ['S7', 'SJ'], ['S7', 'SQ'], ['S7', 'SK'], ['S8', 'S9'], ['S8', 'S10'], ['S8', 'SJ'], ['S8', 'SQ'], ['S8', 'SK'], ['S9', 'S10'], ['S9', 'SJ'], ['S9', 'SQ'], ['S9', 'SK'], ['S10', 'SJ'], ['S10', 'SQ'], ['S10', 'SK'], ['SJ', 'SQ'], ['SJ', 'SK'], ['SQ', 'SK'],
    #   able to be straight
    ['SA', 'H2'], ['SA', 'H3'], ['SA', 'H4'], ['SA', 'H5'], ['S2', 'H3'], ['S2', 'H4'], ['S2', 'H5'], ['S2', 'H6'], ['S3', 'H4'], ['S3', 'H5'], ['S3', 'H6'], ['S3', 'H7'], ['S4', 'H5'], ['S4', 'H6'], ['S4', 'H7'], ['S4', 'H8'], ['S5', 'H6'], ['S5', 'H7'], ['S5', 'H8'], ['S5', 'H9'], ['S6', 'H7'], ['S6', 'H8'], ['S6', 'H9'], ['S6', 'H10'], ['S7', 
'H8'], ['S7', 'H9'], ['S7', 'H10'], ['S7', 'HJ'], ['S8', 'H9'], ['S8', 'H10'], ['S8', 'HJ'], ['S8', 'HQ'], ['S9', 'H10'], ['S9', 'HJ'], ['S9', 'HQ'], ['S9', 'HK'], ['S10', 'HJ'], ['S10', 'HQ'], ['S10', 'HK'], ['S10', 'DA'],

    #   unable to be straight -> very likely to be woolon 
    ['SA', 'H6'], ['SA', 'H7'], ['SA', 'H8'], ['SA', 'H9'], ['SA', 'H10'], ['SA', 'HJ'], ['SA', 'HQ'], ['SA', 'HK'], ['S2', 'H7'], ['S2', 'H8'], ['S2', 'H9'], ['S2', 'H10'], ['S2', 'HJ'], ['S2', 'HQ'], ['S2', 'HK'], ['S3', 'H8'], ['S3', 'H9'], ['S3', 'H10'], ['S3', 'HJ'], ['S3', 'HQ'], ['S3', 'HK'], ['S4', 'H9'], ['S4', 'H10'], ['S4', 'HJ'], ['S4', 'HQ'], ['S4', 'HK'], ['S5', 'H10'], ['S5', 'HJ'], ['S5', 'HQ'], ['S5', 'HK'], ['S6', 'HJ'], ['S6', 'HQ'], ['S6', 'HK'], ['S7', 'HQ'], ['S7', 'HK'], ['S8', 'HK'] 
]

    

