from dataclasses import dataclass
import random as r
import numpy as np
import pandas as pd

EXCLUDE = []
NUM_DECKS = 8
SHUFFLE_AFTER = 7
NUM_NORM_CARDS = 4
MAX_SPLIT = 3

HARD_SOL =        np.array([[1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

HARD_SOL_D =      np.array([[1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,2,2,2,2,1,1,1,1,1],
                            [2,2,2,2,2,2,2,2,1,1],
                            [2,2,2,2,2,2,2,2,2,2],
                            [1,1,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,1,1,1,1,1],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

SOFT_SOL =        np.array([[1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [0,0,0,0,0,0,0,1,1,1],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

SOFT_SOL_D =      np.array([[1,1,1,2,2,1,1,1,1,1],
                            [1,1,1,2,2,1,1,1,1,1],
                            [1,1,2,2,2,1,1,1,1,1],
                            [1,1,2,2,2,1,1,1,1,1],
                            [1,2,2,2,2,1,1,1,1,1],
                            [2,2,2,2,2,0,0,1,1,1],
                            [0,0,0,0,2,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

PAIR_SOL =        np.array([[3,3,3,3,3,3,0,0,0,0],
                            [3,3,3,3,3,3,0,0,0,0],
                            [0,0,0,3,3,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [3,3,3,3,3,0,0,0,0,0],
                            [3,3,3,3,3,3,0,0,0,0],
                            [3,3,3,3,3,3,3,3,3,3],
                            [3,3,3,3,3,0,3,3,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

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
    global BWIN
    global GWIN
    i = 1
    sessionid = 1
    totalSessions = 10000
    numsim = 1000
    # data = {'Session ID':[], 'Games Simulated in Session':[], 'Avg Bet (Xbase)':[], 'Session Winrate (W/L Xbase)': [], 'Amount won (Xbase)':[], 'Amount loss (Xbase)':[], 'Amount push (Xbase)':[], 'Net Gain/Loss (Xbase)': []}
    while (sessionid <= totalSessions):
        while (i <= numsim):
            play_game()
            i += 1
        i = 1
        # data['Session ID'].append(sessionid)
        # data['Games Simulated in Session'].append(numsim)
        # data['Avg Bet (Xbase)'].append((WINS+LOSSES+PUSHES)/float(numsim))
        # data['Session Winrate (W/L Xbase)'].append((WINS)/(WINS+LOSSES) * 100.0)
        # data['Amount won (Xbase)'].append(WINS)
        # data['Amount loss (Xbase)'].append(LOSSES)
        # data['Amount push (Xbase)'].append(PUSHES)
        # data['Net Gain/Loss (Xbase)'].append(WINS - LOSSES)
        print("BWIN :", BWIN)
        print("GWIN :", GWIN)
        print("WINS :", WINS)
        print("LOSSES :", LOSSES)
        print("PUSHES :", PUSHES)
        print("W/R :", float(WINS)/float(WINS+LOSSES) * 100.0, "%")
        BWIN = 0
        GWIN = 0
        # WINS = 0.0
        # LOSSES = 0.0
        # PUSHES = 0.0
        sessionid += 1
    #     print('Percent Done: ', round(float(sessionid)/float(totalSessions)* 100.00, 2), "%", end='\r', flush=True)
    # dataFrame = pd.DataFrame.from_dict(data)
    # dataFrame.to_csv('basic_strategy_data.csv', index=False)
    # curr = hit()
    # bj = 0
    # draws = 1
    # while (True):
    #     prev = curr
    #     curr = hit()
    #     draws += 1
    #     if (curr == 11):
    #         bj += 1
    #         print('Draw %: ', round(float(bj)/float(draws)* 100.00, 3), "% Simnum: ", draws, end='\r\r\r\r\r\r', flush=True)
        # if ((prev == 10 and curr == 11) or (prev == 11 and curr == 10)):
        #     bj += 1
        # print('Blackjack %: ', round(((float(bj)/float(draws)) - ((float(bj)/float(draws))*(float(bj)/float(draws))))* 100.00, 3), "% Simnum: ", draws, end='\r\r\r\r\r\r', flush=True)


# Classifiers:
    # blackjack - ace and any 10 value card
    # aces - two or More aces in the hand
    # hard - hard hand
    # harddouble - hard hand that can double down
    # soft - hand with an ace
    # softdouble - hand with an ace that can be doubled down
    # pair - hand with two of the same card
    # bust - hand with value over 21
def basic_strategy(currHand, dHand): 
    # 0 = Stand
    # 1 = Hit
    # 2 = Double Down
    # 3 = Split

    classifier = currHand.classifier
    hVal = sum(currHand.hand)
    if (hVal > 21 and not(11 in currHand.hand)):
        return 0
    if (11 in dHand and 10 in dHand and len(dHand) == 2):
        if (currHand.classifier == 'blackjack'):
            currHand.classifier = 'sadjack'
        return 0
    if (classifier == 'blackjack'):
        return 0
    elif (classifier == 'splitace' or classifier == 'hardsplitace' or classifier == 'softsplitace'):
        if (classifier == 'splitace'):
            return HARD_SOL_D[8][dHand[0] - 2]
        elif (classifier == 'softsplitace'):
            return SOFT_SOL_D[hVal - 13][dHand[0] - 2]
        else:
            return SOFT_SOL[hVal - 13][dHand[0] - 2]
    elif (classifier == 'aces'):
        if (currHand.splitnum < MAX_SPLIT):
            return 3
        else:
            return 0
    elif (classifier == 'pair'):
        if (PAIR_SOL[currHand.hand[0] - 2][dHand[0] - 2] == 3):
            return PAIR_SOL[currHand.hand[0] - 2][dHand[0] - 2]
        else:
            return HARD_SOL_D[hVal - 4][dHand[0] - 2]
    elif (classifier == 'softdouble'):
        return SOFT_SOL_D[hVal - 13][dHand[0] - 2]
    elif (classifier == 'soft'):
        return SOFT_SOL[hVal - 13][dHand[0] - 2]
    elif (classifier == 'harddouble'):
        return HARD_SOL_D[hVal - 4][dHand[0] - 2]
    else:
        return HARD_SOL[hVal - 4][dHand[0] - 2]

def play_game():
    nc1 = hit()
    nc2 = hit()
    nc3 = hit()
    nc4 = hit()
    pVals = [Hand(0, 1.0, [nc1])]
    dVals = [nc2]
    pVals[0].hand.append(nc3) 
    dVals.append(nc4)
    pVals[0].classify()
    gameState = Game_State(pVals.copy(), dVals.copy(), pVals.copy())
    while (not(gameState.is_stack_empty())):
        currHand = gameState.pop_hand()
        decision = -1
        while (not(decision == 0 or decision == 2)):
            decision = basic_strategy(currHand, gameState.dHand)
            update_game_state(gameState, currHand, decision)
            if (decision == 3 or decision == 1):
                currHand = gameState.pop_hand()
    gameState.dealer_draw()
    gameState.evaluate_game_state()

def hit():
    global EXCLUDE
    totEachCard = NUM_NORM_CARDS * NUM_DECKS
    if (len(EXCLUDE) == NUM_NORM_CARDS * SHUFFLE_AFTER * 13):
        EXCLUDE = []
    h = r.choice(list(set([x for x in range(1, totEachCard * 13 + 1)]) - set(EXCLUDE)))
    EXCLUDE.append(h)
    if   (0  * totEachCard  < h <= totEachCard * 1 ):
        return 2
    elif (1  * totEachCard  < h <= totEachCard * 2 ):
        return 3
    elif (2  * totEachCard  < h <= totEachCard * 3 ):
        return 4
    elif (3  * totEachCard  < h <= totEachCard * 4 ):
        return 5
    elif (4  * totEachCard  < h <= totEachCard * 5 ):
        return 6
    elif (5  * totEachCard  < h <= totEachCard * 6 ):
        return 7
    elif (6  * totEachCard  < h <= totEachCard * 7 ):
        return 8
    elif (7  * totEachCard  < h <= totEachCard * 8 ):
        return 9
    elif (8  * totEachCard  < h <= totEachCard * 9 ):
        return 10
    elif (9  * totEachCard  < h <= totEachCard * 10):
        return 10
    elif (10 * totEachCard  < h <= totEachCard * 11):
        return 10
    elif (11 * totEachCard  < h <= totEachCard * 12):
        return 10
    elif (12 * totEachCard  < h <= totEachCard * 13):
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
    if (decision == 1 or decision == 2):
        nc = hit()
    if (decision == 1):
        currHand.hand.append(nc)
        while (sum(currHand.hand) > 21 and 11 in currHand.hand):
            if (not(11 in currHand.hand)):
                break
            currHand.hand[currHand.hand.index(11)] = 1
        currHand.classify()
        if (not(currHand.classifier == 'splitace' and currHand.classifier == 'softsplitace' and currHand.classifier == 'hardsplitace')):
            currGameState.push_hand(currHand)
    elif (decision == 2):
        currHand.hand.append(nc)
        while (sum(currHand.hand) > 21 and 11 in currHand.hand):
            if (not(11 in currHand.hand)):
                break
            currHand.hand[currHand.hand.index(11)] = 1
        currHand.classify()
        currHand.betSize = 2.0 * currHand.betSize
    elif (decision == 3):
        nc1 = hit()
        nc2 = hit()
        sHand1 = Hand(currHand.splitnum + 1, currHand.betSize, [currHand.hand[0], nc1])
        sHand1.classify()
        sHand2 = Hand(currHand.splitnum + 1, currHand.betSize, [currHand.hand[1], nc2])
        sHand2.classify()
        currGameState.pHands.append(sHand1)
        currGameState.pHands.append(sHand2)
        currGameState.pHands.remove(currHand)
        currGameState.push_hand(sHand1)
        currGameState.push_hand(sHand2)

# def evaluate_game_state(gameState):
#     global WINS
#     global LOSSES
#     global PUSHES
#     i = 1
#     dealerHand = ""
#     dTot = sum(gameState.dHand)
#     for card in gameState.dHand:
#         dealerHand += to_string(card) + "  "
#     # print("\n    Dealer Hand: ", dealerHand[:len(dealerHand)-2])
#     for h in gameState.pHands:
#         handTotal = sum(h.hand)
#         handStr = ""
#         for card in h.hand:
#             handStr += to_string(card) + "  "
#         if (h.classifier == 'sadjack'):
#             # print("\n    Dealer Hand: ", dealerHand[:len(dealerHand)-2])
#             # print("\n    Payout: ", -1.0 * h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Dealer Black Jack")
#             PUSHES += h.betSize
#             SJ += 1
#         elif (h.classifier == 'blackjack'):
#             # print("\n    Dealer Hand: ", dealerHand[:len(dealerHand)-2])
#             # print("\n    Payout: ",h.betSize * 1.5," Hand", i,"(", handStr[:len(handStr)-2],"): Blackjack")
#             WINS += h.betSize * 1.5
#             BJ += 1
#         elif (h.classifier == 'bust'):
#             # print("\n    Payout: ",-1.0 * h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Bust")
#             PBUST += 1
#             LOSSES += h.betSize
#         elif (handTotal == dTot):
#             # print("\n    Payout: ", 0.0," Hand", i,"(", handStr[:len(handStr)-2],"): Push")
#             PUSHES += h.betSize
#         elif (handTotal < dTot and dTot < 22):
#             # print("\n    Payout: ",-1.0 * h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Loss")
#             LOSSES += h.betSize
#         elif (handTotal > dTot):
#             # print("\n    Dealer Hand: ", dealerHand[:len(dealerHand)-2])
#             # print("\n    Payout: ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Win")
#             WINS += h.betSize
#         elif (handTotal < 22 and dTot > 21):
#             WINS += h.betSize
#         i += 1

BWIN = 0
GWIN = 0
# pHands = [hand1, hand2, etc], player hands
# dHand = [dealer hand], dealer hand
# hStack = [(splitnum, [hand]), (splitnum2, [hand2]), ...etc], hands with actions left
class Game_State:
    def __init__(self, pHands, dHand, hStack):
        self.pHands = pHands
        self.dHand = dHand
        self.hStack = hStack

    def evaluate_game_state(self):
        global WINS
        global LOSSES
        global PUSHES
        global BWIN
        global GWIN
        for h in self.pHands:
            handTotal = sum(h.hand)
            dTot = sum(self.dHand)
            if (11 in self.dHand and 10 in self.dHand and len(self.dHand) == 2):
                if (h.classifier == 'sadjack'):
                    BWIN += 1
                    PUSHES += h.betSize
                else:
                    LOSSES += h.betSize
            elif (h.classifier == 'blackjack'):
                GWIN += 1
                WINS += h.betSize * 1.5
            elif (handTotal == dTot):
                if (handTotal > 21):
                    LOSSES += h.betSize
                else:
                    PUSHES += h.betSize
            elif ((handTotal < 22 and handTotal > dTot and dTot < 22) or (handTotal < 22 and dTot > 21)):
                WINS += h.betSize
            else:
                LOSSES += h.betSize

    def dealer_draw(self):
        while (sum(self.dHand) > 21 and 11 in self.dHand):
            if (not(11 in self.dHand)):
                break
            self.dHand[self.dHand.index(11)] = 1
        while (sum(self.dHand) < 17):
            c = hit()
            if (c + sum(self.dHand) > 21 and c == 11):
                c = 1
            self.dHand.append(c)
            while (sum(self.dHand) > 21 and 11 in self.dHand):
                if (not(11 in self.dHand)):
                    break
                self.dHand[self.dHand.index(11)] = 1

    def push_hand(self, hand):
        self.hStack.append(hand)

    def pop_hand(self):
        return self.hStack.pop()

    def is_stack_empty(self):
        return len(self.hStack) == 0

    def print(self):
        pHandStr = [hand.print() for hand in self.pHands]
        hStackStr = [hand.print() for hand in self.hStack]
        print('player hands: ', self.pHands)
        print('dealer hand: ', self.dHand)
        print('hands with actions left: ', self.hStack)

class Hand:
    def __init__(self, splitnum, betSize, hand):
        self.splitnum = splitnum
        self.betSize = betSize
        self.hand = hand
        self.classifier = None
    
    # Classifiers:
        # blackjack - ace and any 10 value card
        # aces - two aces in the hand
        # splitace - an hand with an ace that has been split
        # hard - hard hand
        # harddouble - hard hand that can double down
        # soft - hand with an ace
        # softdouble - hand with an ace that can be doubled down
        # pair - hand with two of the same card
    def classify(self):
        hVal = sum(self.hand)
        hSize = len(self.hand)
        if (11 in self.hand or 1 in self.hand):
            if (len(self.hand) == self.hand.count(11) + self.hand.count(1)):
                if (hSize == 2):
                    if (self.splitnum < MAX_SPLIT):
                        self.classifier = 'aces'
                    else:
                        self.classifier = 'splitace'
                else:
                    self.classifier =  'hard'
            elif (hSize == 2):
                if (10 in self.hand and 11 in self.hand and self.splitnum == 0):
                    self.classifier =  'blackjack'
                else:
                    if (self.splitnum == 0):
                        self.classifier = 'softdouble'
                    else:
                        self.classifier = 'softsplitace'
            else:
                if (self.splitnum == 0):
                    if (hVal < 22):
                        self.classifier = 'soft'
                    else:
                        self.classifier = 'hard'
                else:
                    self.classifier = 'hardsplitace'
        elif (hSize == 2):
            if (self.hand[0] == self.hand[1] and self.splitnum < MAX_SPLIT):
                self.classifier =  'pair'
            else: 
                self.classifier =  'harddouble'
        else:
            self.classifier = 'hard'


    def print(self):
        print('splitnum: ', self.splitnum, 'bet size: ', self.betSize, 'hand: ', self.hand, 'classifier: ', self.classifier)

if __name__ == "__main__":
    main()