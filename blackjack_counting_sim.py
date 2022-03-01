import random as r
import numpy as np
import pandas as pd

EXCLUDE = []
NUM_DECKS = 6
SHUFFLE_AFTER = 4
NUM_NORM_CARDS = 4
MAX_SPLIT = 3

                                                        # 2,3,4,5,6,7,8,9,10,J,Q,K,A
NAME_TO_COUNT_VECTOR = {'hi_lo':                      [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0],
                        'hi_opt1':                    [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, 0.0],
                        'hi_opt2':                    [1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.0, 0.0, -2.0, -2.0, -2.0, -2.0, 0.0],
                        'knock_out':                  [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0],
                        'omega2':                     [1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 0.0, -1.0, -2.0, -2.0, -2.0, -2.0, 0.0],
                        'ace_five':                   [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                        'zen_count':                  [1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 0.0, 0.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                        'halves':                     [0.5, 1.0, 1.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -1.0, -1.0, -1.0, -1.0],
                        'kiss':                       [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, 0.0],
                        'wong_halves':                [0.5, 1.0, 1.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -1.0, -1.0, -1.0, -1.0],
                        'j_noir':                     [-2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -2.0, -2.0, -2.0, -2.0, -2.0],
                        'silver_fox':                 [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
                        'unbalanced_zen2':            [1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 0.0, 0.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                        'revere_point_count':         [1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 0.0, 0.0, -2.0, -2.0, -2.0, -2.0, -2.0],
                        'uston_advanced_point_count': [1.0, 2.0, 2.0, 3.0, 2.0, 2.0, 1.0, -1.0, 3.0, 3.0, 3.0, -3.0, 0.0],
                        'canfield_expert':            [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0, 0.0],
                                                        # 2R,2B,3,4,5,6,7,8,9,10,J,Q,K,A
                        'kiss2':                      [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0],
                        'kiss3':                      [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0],
                                                        # 2,3,4,5,6,7R,7B,8,9,10,J,Q,K,A
                        'red_seven':                  [-1.0, -1.0, -1.0, -1.0, -1.0, 1.0, 0.0, 0.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0]}

WINS = 0.0
LOSSES = 0.0
PUSHES = 0.0

#
# Data Columns
# 
# Session Id - + INT, 
# Number of games in session - + INT, 
# Avg Bet (x(Base)) - + FLOAT, 
# Session winrate (W/L x(Base)) - +% FLOAT, 
# Amount won (x(Base)) - + FLOAT, 
# Amount loss (x(Base)) - + FLOAT, 
# Amount push (x(Base)) - + FLOAT,
# Net Gain/Loss (x(Base)) - +/- FLOAT 
#
def main():
    global WINS
    global LOSSES
    global PUSHES
    i = 1
    sessionid = 1
    totalSessions = 1000
    numsim = 10000
    data = {'Session ID':[], 'Games Simulated in Session':[], 'Avg Bet (Xbase)':[], 'Session Winrate (W/L Xbase)': [], 'Amount won (Xbase)':[], 'Amount loss (Xbase)':[], 'Amount push (Xbase)':[], 'Net Gain/Loss (Xbase)': []}
    while (sessionid <= totalSessions):
        while (i <= numsim):
            play_game()
            i += 1
        i = 1
        data['Session ID'].append(sessionid)
        data['Games Simulated in Session'].append(numsim)
        data['Avg Bet (Xbase)'].append((WINS+LOSSES+PUSHES)/float(numsim))
        data['Session Winrate (W/L Xbase)'].append((WINS)/(WINS+LOSSES) * 100.0)
        data['Amount won (Xbase)'].append(WINS)
        data['Amount loss (Xbase)'].append(LOSSES)
        data['Amount push (Xbase)'].append(PUSHES)
        data['Net Gain/Loss (Xbase)'].append(WINS - LOSSES)  
        WINS = 0.0
        LOSSES = 0.0
        PUSHES = 0.0
        sessionid += 1
        print('Percent Done: ', round(float(sessionid)/float(totalSessions)* 100.00, 2), "%", end='\r', flush=True)
    dataFrame = pd.DataFrame.from_dict(data)
    # dataFrame.to_csv('basic_strategy_data.csv', index=False)

def count_strategy(currHand, dv, stratType): 
    # 0 = Stand
    # 1 = Hit
    # 2 = Double Down
    # 3 = Split

    # TODO implement decisions

    # numCards = len(currHand.hand)
    # hVal = sum(currHand.hand)
    # if (11 in currHand.hand and numCards == 2 and not(currHand.hand[0] == currHand.hand[1])):
    #     if (currHand.splitnum == 0):
    #         return SOFT_SOL[hVal - 13][dv - 2]
    #     else:
    #         return SOFT_SOL_SPLIT[hVal - 13][dv - 2]
    # elif (currHand.splitnum >= 1 and currHand.splitnum < MAX_SPLIT): # Already split
    #     if (numCards == 1): # Can't split, can double down
    #         return HARD_SOL[hVal - 4][dv-2]
    #     elif (numCards == 2 and currHand.hand[0] == currHand.hand[1]): # Can split, can't double down
    #         if (PAIR_SOL[currHand.hand[0] - 2][dv - 2] == 3): # Recommended split
    #             return PAIR_SOL[currHand.hand[0] - 2][dv - 2]
    #         else: # Recommended hit/stand no double down
    #             return np.where(HARD_SOL == 2, 1, HARD_SOL)[hVal - 4][dv-2]
    #     elif (not(hVal > 17 or hVal < 8)): # Can't split, can't double down
    #         return np.where(HARD_SOL == 2, 1, HARD_SOL)[hVal - 4][dv-2]
    #     else:
    #         return HARD_SOL[hVal - 4][dv-2]
    # elif (numCards == 2 and currHand.splitnum == 0 and currHand.hand[0] == currHand.hand[1] and PAIR_SOL[currHand.hand[0] - 2][dv - 2] == 3):
    #     return PAIR_SOL[currHand.hand[0] - 2][dv - 2]
    # else: # Can't split, can't double down
    #     return HARD_SOL[hVal - 4][dv-2]
    return 0

def hi_lo():
    # TODO implement this card counting system
    return 0

def hi_opt1():
    # TODO implement this card counting system
    return 0

def hi_opt2():
    # TODO implement this card counting system
    return 0

def knock_out():
    # TODO implement this card counting system
    return 0

def red_seven():
    # TODO implement this card counting system
    return 0

def omega2():
    # TODO implement this card counting system
    return 0

def ace_five():
    # TODO implement this card counting system
    return 0

def zen_count():
    # TODO implement this card counting system
    return 0

def halves():
    # TODO implement this card counting system
    return 0

def kiss():
    # TODO implement this card counting system
    return 0

def kiss2():
    # TODO implement this card counting system
    return 0

def kiss3():
    # TODO implement this card counting system
    return 0

def wong_halves():
    # TODO implement this card counting system
    return 0

def j_noir():
    # TODO implement this card counting system
    return 0

def silver_fox():
    # TODO implement this card counting system
    return 0

def unbalanced_zen2():
    # TODO implement this card counting system
    return 0

def revere_point_count():
    # TODO implement this card counting system
    return 0

def uston_advanced_point_count():
    # TODO implement this card counting system
    return 0

def canfield_expert_system():
    # TODO implement this card counting system
    return 0

def play_game():
    pVals = [Hand(0, 1.0, [hit()])]
    dVals = [hit()]
    pVals[0].hand.append(hit())
    dVals.append(hit())
    gameState = Game_State(pVals.copy(), dVals, pVals.copy())
    while (not(gameState.is_stack_empty())):
        currHand = gameState.pop_hand()
        decision = -1
        while (not(decision == 0 or decision == 2)):
            decision = count_strategy(currHand, gameState.dHand[0])
            update_game_state(gameState, currHand, decision)
            if (decision == 3 or decision == 1):
                currHand = gameState.pop_hand()
            if (sum(currHand.hand) > 21):
                break
    dVal = sum(gameState.dHand)
    if (dVal > 21):
        gameState.dHand[gameState.dHand.index(11)] = 1
        dVal = sum(gameState.dHand)
    while (dVal < 17):
        newCard = hit()
        if (dVal + newCard > 21 and newCard == 11):
            newCard = 1
        gameState.dHand.append(newCard)
        dVal = sum(gameState.dHand)
    evaluate_game_state(gameState)

def hit():
    global EXCLUDE
    if (len(EXCLUDE) > NUM_NORM_CARDS * SHUFFLE_AFTER * 13 + 1):
        EXCLUDE = []
    h = r.choice(list(set([x for x in range(1, NUM_NORM_CARDS * NUM_DECKS * 13 + 1)]) - set(EXCLUDE)))
    EXCLUDE.append(h)
    if (1 <= h <= NUM_NORM_CARDS * NUM_DECKS):
        return 2
    elif (NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 2):
        return 3
    elif (2 * NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 3):
        return 4
    elif (3 * NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 4):
        return 5
    elif (4 * NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 5):
        return 6
    elif (5 * NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 6):
        return 7
    elif (6 * NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 7):
        return 8
    elif (7 * NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 8):
        return 9
    elif (8 * NUM_NORM_CARDS * NUM_DECKS + 1 <= h <= NUM_NORM_CARDS * NUM_DECKS * 12):
        return 10
    else:
        return 11

def to_string(cVal):
    cvs = ''
    fMap = {0:'10', 1:'J', 2:'Q', 3:'K'}
    if (cVal == 11 or cVal == 1):
        cvs = 'A'
    elif (cVal == 10):
        cvs = fMap[r.randint(0,3)]
    else:
        cvs = str(cVal)
    return cvs

def print_hand(hand):
    hString = ""
    for i in range(len(hand)):
        hString = hString + to_string(hand[i]) + "   "
    return hString

def update_game_state(currGameState, currHand, decision):
    if (not(decision == 3)):
        newCard = hit()
        if (sum(currHand.hand) + newCard > 21 and newCard == 11):
            newCard = 1
    if (decision == 1):
        currHand.hand.append(newCard)
        currGameState.push_hand(currHand)
    elif (decision == 2):
        currHand.hand.append(newCard)
        currHand.betSize += currHand.betSize
    elif (decision == 3):
        sHand1 = Hand(currHand.splitnum + 1, currHand.betSize, [currHand.hand[0]])
        sHand2 = Hand(currHand.splitnum + 1, currHand.betSize, [currHand.hand[1]])
        currGameState.pHands += [sHand1, sHand2]
        currGameState.pHands.remove(currHand)
        currGameState.push_hand(sHand1)
        currGameState.push_hand(sHand2)

def evaluate_game_state(gameState):
    global WINS
    global LOSSES
    global PUSHES

    i = 1
    dealerHand = ""
    dTot = sum(gameState.dHand)
    for card in gameState.dHand:
        dealerHand += to_string(card) + "  "
    # print("\n    Dealer Hand: ", dealerHand[:len(dealerHand)-2])
    for h in gameState.pHands:
        handTotal = sum(h.hand)
        handStr = ""
        for card in h.hand:
            handStr += to_string(card) + "  "
        if (handTotal == 21 and 11 in h.hand and 10 in h.hand):
            WINS += h.betSize * 1.5
        elif (handTotal > 21):
            # print("\n    Bet: ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Bust")
            LOSSES += h.betSize
        elif (handTotal > dTot or dTot > 21):
            # print("\n    Bet: ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Win")
            WINS += h.betSize
        elif (handTotal == dTot):
            # print("\n    Bet: ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Push")
            PUSHES += h.betSize
        else:
            # print("\n    Bet: ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Loss")
            LOSSES += h.betSize
        i += 1

# pHands = [hand1, hand2, etc], player hands
# dHand = [dealer hand], dealer hand
# hStack = [(splitnum, [hand]), (splitnum2, [hand2]), ...etc], hands with actions left
class Game_State:
    def __init__(self, pHands, dHand, hStack):
        self.pHands = pHands
        self.dHand = dHand
        self.hStack = hStack

    def push_hand(self, hand):
        self.hStack.append(hand)

    def pop_hand(self):
        return self.hStack.pop()

    def is_stack_empty(self):
        return len(self.hStack) == 0

    def print(self):
        pHandStr = " " + str([hand.print() for hand in self.pHands]) + ","
        hStackStr = " " + str([hand.print() for hand in self.hStack]) + ","
        print('player hands: ', pHandStr[:len(pHandStr)-1])
        print('dealer hand: ', self.dHand)
        print('hands with actions left: ', hStackStr[:len(hStackStr)-1])

class Hand:
    def __init__(self, splitnum, betSize, hand):
        self.splitnum = splitnum
        self.betSize = betSize
        self.hand = hand
    
    def print(self):
        print('splitnum: ', self.splitnum, 'bet size: ', self.betSize, 'hand: ', self.hand)

if __name__ == "__main__":
    main()