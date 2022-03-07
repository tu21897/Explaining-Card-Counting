# blackjack_basic_sim.py - Tu Nguyen 2022
#
# ----------------------------------
#
# This file defines and simulates the game of Blackjack
# the resulting data is converted to a dataframe and subsequently
# stored as a created csv file.
#

# Imports
import random as r
import numpy as np
import pandas as pd


##################### Settings #####################
NUM_DECKS = 8 # Number of decks in shoe
SHUFFLE_AFTER = 7 # Where the deck is cut to be reshuffled
NUM_NORM_CARDS = 4 # Number of each card in a deck
MAX_SPLIT = 3 # Maximum number of splits allowed


EXCLUDE = [] # Cards Drawn

# Solution given a hard hand without double down
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

# Solution given a hard hand with double down
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

# Solution given a soft hand without double down
SOFT_SOL =        np.array([[1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1],
                            [0,0,0,0,0,0,0,1,1,1],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

# Solution given a soft hand with double down
SOFT_SOL_D =      np.array([[1,1,1,2,2,1,1,1,1,1],
                            [1,1,1,2,2,1,1,1,1,1],
                            [1,1,2,2,2,1,1,1,1,1],
                            [1,1,2,2,2,1,1,1,1,1],
                            [1,2,2,2,2,1,1,1,1,1],
                            [2,2,2,2,2,0,0,1,1,1],
                            [0,0,0,0,2,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

# Solution given a pair hand
PAIR_SOL =        np.array([[3,3,3,3,3,3,0,0,0,0],
                            [3,3,3,3,3,3,0,0,0,0],
                            [0,0,0,3,3,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0],
                            [3,3,3,3,3,0,0,0,0,0],
                            [3,3,3,3,3,3,0,0,0,0],
                            [3,3,3,3,3,3,3,3,3,3],
                            [3,3,3,3,3,0,3,3,0,0],
                            [0,0,0,0,0,0,0,0,0,0]])

WINS = 0.0 # Session Wins (x(Base)) 
LOSSES = 0.0 # Session Losses (x(Base)) 
PUSHES = 0.0 # Session Pushes (x(Base)) 
LIFETIME_WINS = 0.0 # Lifetime Wins (x(Base)) 
LIFETIME_LOSSES = 0.0 # Lifetime Losses (x(Base)) 
LIFETIME_PUSHES = 0.0 # Lifetime Pushes (x(Base)) 

#
# Data Columns
# 
# Session Id - + INT, 
# Number of games in session - + INT, 
# Avg Bet (x(Base)) - + FLOAT, 
# Lifetime winrate (W/L x(Base)) - +% FLOAT, 
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
    totalSessions = 100
    numsim = 1000
    data = {'Session ID':[], 'Cumulative Games': [], 'Games Simulated in Session':[], 'Lifetime Avg Bet (Xbase)':[], 'Lifetime winrate (W/L x(Base))': [], 'Lifetime Amount won (Xbase)':[], 'Lifetime Amount loss (Xbase)':[], 'Lifetime Amount push (Xbase)':[], 'Lifetime Net Gain/Loss (Xbase)': [], 'Session Avg Bet (Xbase)':[], 'Session winrate (W/L x(Base))': [], 'Session Amount won (Xbase)':[], 'Session Amount loss (Xbase)':[], 'Session Amount push (Xbase)':[], 'Session Net Gain/Loss (Xbase)': []}
    while (sessionid <= totalSessions):
        while (i <= numsim):
            play_game()
            i += 1
        i = 1
        data['Session ID'].append(sessionid)
        data['Cumulative Games'].append(sessionid * numsim)
        data['Games Simulated in Session'].append(numsim)
        data['Lifetime Avg Bet (Xbase)'].append(round((LIFETIME_WINS+LIFETIME_LOSSES+LIFETIME_PUSHES)/(float(numsim) * float(sessionid)), 3))
        data['Lifetime winrate (W/L x(Base))'].append(round((LIFETIME_WINS)/(LIFETIME_WINS+LIFETIME_LOSSES) * 100.0, 3))
        data['Lifetime Amount won (Xbase)'].append(LIFETIME_WINS)
        data['Lifetime Amount loss (Xbase)'].append(LIFETIME_LOSSES)
        data['Lifetime Amount push (Xbase)'].append(LIFETIME_PUSHES)
        data['Lifetime Net Gain/Loss (Xbase)'].append(LIFETIME_WINS - LIFETIME_LOSSES)
        data['Session Avg Bet (Xbase)'].append(round((WINS+LOSSES+PUSHES)/(float(numsim) * float(sessionid)), 3))
        data['Session winrate (W/L x(Base))'].append(round((WINS)/(WINS+LOSSES) * 100.0, 3))
        data['Session Amount won (Xbase)'].append(WINS)
        data['Session Amount loss (Xbase)'].append(LOSSES)
        data['Session Amount push (Xbase)'].append(PUSHES)
        data['Session Net Gain/Loss (Xbase)'].append(WINS - LOSSES)
        sessionid += 1
        WINS = 0.0
        LOSSES = 0.0
        PUSHES = 0.0
        print('Percent Done: ', round(float(sessionid)/float(totalSessions)* 100.00, 2), "%", end='\r', flush=True)
    dataFrame = pd.DataFrame.from_dict(data)
    dataFrame.to_csv('basic_strategy_data.csv', index=False)

# Returns the decision based on the current hand and the dealer shown card
# currHand - the hand the action is for
# dHand - the dealer's hand
#
# Classifiers:
        # blackjack - ace and any 10 value card
        # sadjack - both dealer and player have blackjack
        # aces - two aces in the hand
        # splitace - an hand with an ace that has been split
        # softsplitace - an hand with an ace that has been split 2 cards
        # hardsplitace - an hand with an ace that has been split more than 2 cards
        # hard - hard hand
        # harddouble - hard hand that can double down
        # soft - hand with an ace
        # softdouble - hand with an ace that can be doubled down
        # pair - splitable hand with two of the same card
# Decisions:
        # 0 = Stand
        # 1 = Hit
        # 2 = Double Down
        # 3 = Split
def basic_strategy(currHand, dHand): 
    classifier = currHand.classifier
    hVal = sum(currHand.hand)

    # Bust
    if (hVal > 21 and not(11 in currHand.hand)):
        return 0
    
    # Dealer Blackjack
    if (11 in dHand and 10 in dHand and len(dHand) == 2):
        if (currHand.classifier == 'blackjack'):
            currHand.classifier = 'sadjack'
        return 0
    
    # Base
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

# Simulates one game of basic strategy blackjack
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

# Draws a card without replacement, shuffles after SHUFFLE_AFTER amount of decks
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

# Applies given decision to gamestate
#
# currGameState - current state of the game
# currHand - current hand for the decision
# decision - the action applied to the current hand
def update_game_state(currGameState, currHand, decision):
    if (decision == 1 or decision == 2):
        nc = hit()
        currHand.hand.append(nc)
        while (sum(currHand.hand) > 21 and 11 in currHand.hand):
            if (not(11 in currHand.hand)):
                break
            currHand.hand[currHand.hand.index(11)] = 1
    if (decision == 1):
        currHand.classify()
        if (not(currHand.classifier == 'splitace' and currHand.classifier == 'softsplitace' and currHand.classifier == 'hardsplitace')):
            currGameState.push_hand(currHand)
    elif (decision == 2):
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

# Defines the state of the game
#
# pHands = [hand1, hand2, etc], player hands
# dHand = [dealer hand], dealer hand
# hStack = [hand1, hand2, ...etc], hands with actions left
class Game_State:
    def __init__(self, pHands, dHand, hStack):
        self.pHands = pHands
        self.dHand = dHand
        self.hStack = hStack

    # Evaluates the game state
    def evaluate_game_state(self):
        global WINS
        global LOSSES
        global PUSHES
        global LIFETIME_WINS
        global LIFETIME_LOSSES
        global LIFETIME_PUSHES
        for h in self.pHands:
            handTotal = sum(h.hand)
            dTot = sum(self.dHand)
            if (11 in self.dHand and 10 in self.dHand and len(self.dHand) == 2):
                if (h.classifier == 'sadjack'):
                    PUSHES += h.betSize
                    LIFETIME_PUSHES += h.betSize
                else:
                    LOSSES += h.betSize
                    LIFETIME_LOSSES += h.betSize
            elif (h.classifier == 'blackjack'):
                WINS += h.betSize * 1.5
                LIFETIME_WINS += h.betSize
            elif (handTotal == dTot):
                if (handTotal > 21):
                    LOSSES += h.betSize
                    LIFETIME_LOSSES += h.betSize
                else:
                    PUSHES += h.betSize
                    LIFETIME_PUSHES += h.betSize
            elif ((handTotal < 22 and handTotal > dTot and dTot < 22) or (handTotal < 22 and dTot > 21)):
                WINS += h.betSize
                LIFETIME_WINS += h.betSize
            else:
                LOSSES += h.betSize
                LIFETIME_LOSSES += h.betSize

    # Simulates the dealer's turn
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

    # Adds a hand to the available actions
    #
    # hand - the hand being added
    def push_hand(self, hand):
        self.hStack.append(hand)

    # Returns the next hand in the action stack
    def pop_hand(self):
        return self.hStack.pop()

    # Returns True if the stack is empty, False otherwise
    def is_stack_empty(self):
        return len(self.hStack) == 0

# Defines the structure of a hand
#
# splitnum - number of splits in current hand
# betSize - size of bet
# hand - list of cards in hand
# classifier - the type of hand
class Hand:
    def __init__(self, splitnum, betSize, hand):
        self.splitnum = splitnum
        self.betSize = betSize
        self.hand = hand
        self.classifier = None
    
    # Classifies a hand
    #
    # Classifiers:
        # blackjack - ace and any 10 value card
        # sadjack - both dealer and player have blackjack
        # aces - two aces in the hand
        # splitace - an hand with an ace that has been split
        # softsplitace - an hand with an ace that has been split 2 cards
        # hardsplitace - an hand with an ace that has been split more than 2 cards
        # hard - hard hand
        # harddouble - hard hand that can double down
        # soft - hand with an ace
        # softdouble - hand with an ace that can be doubled down
        # pair - splitable hand with two of the same card
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

if __name__ == "__main__":
    main()