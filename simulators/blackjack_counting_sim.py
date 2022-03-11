# blackjack_counting_sim.py - Tu Nguyen 2022
#
# ----------------------------------
#
# This file defines and simulates the game of Blackjack using counting
# strategy the resulting data is converted to a dataframe and 
# subsequently stored as a created csv file.
#

# Imports
import random as r
import math
import numpy as np
import pandas as pd


##################### Settings #####################
NUM_DECKS = 6 # Number of decks in shoe
SHUFFLE_AFTER = 5 # Where the deck is cut to be reshuffled
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

# #                                                        2    3    4    5    6    7    8     9    10     J     Q     K     A
# NAME_TO_COUNT_VECTOR = {'hi_lo'                     : [ 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,  0.0, -1.0, -1.0, -1.0, -1.0, -1.0],
#                         'hi_opt1'                   : [ 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,  0.0, -1.0, -1.0, -1.0, -1.0,  0.0],
#                         'hi_opt2'                   : [ 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.0,  0.0, -2.0, -2.0, -2.0, -2.0,  0.0],
#                         'omega2'                    : [ 1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 0.0, -1.0, -2.0, -2.0, -2.0, -2.0,  0.0],
#                         'zen_count'                 : [ 1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 0.0,  0.0, -2.0, -2.0, -2.0, -2.0, -1.0],
#                         'halves'                    : [ 0.5, 1.0, 1.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -1.0, -1.0, -1.0, -1.0],
#                         'wong_halves'               : [ 0.5, 1.0, 1.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -1.0, -1.0, -1.0, -1.0],
#                         'silver_fox'                : [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
#                         'revere_point_count'        : [ 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 0.0,  0.0, -2.0, -2.0, -2.0, -2.0, -2.0],
#                         'canfield_expert'           : [ 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, -1.0, -1.0, -1.0,  0.0]}

# count system to corresponding index
CSYS_NAME = ['hi_lo', 'hi_opt1', 'hi_opt2',
             'omega2', 'zen_count',
             'halves', 'wong_halves', 'silver_fox', 
             'revere_point_count','canfield_expert'] 

# card val for each system, [[2s],...,[As]], index = corresponding count system, rows = cval on each card 
# based on system, columns = all cval for system
CVAL_TRANSPOSE =   [[ 1.0, 0.0, 1.0,  1.0, 1.0, 0.5, 0.5, 1.0,  1.0, 0.0],
                    [ 1.0, 1.0, 1.0,  1.0, 1.0, 1.0, 1.0, 1.0,  2.0, 1.0],
                    [ 1.0, 1.0, 2.0,  2.0, 2.0, 1.0, 1.0, 1.0,  2.0, 1.0],
                    [ 1.0, 1.0, 2.0,  2.0, 2.0, 1.5, 1.5, 1.0,  2.0, 1.0],
                    [ 1.0, 1.0, 1.0,  2.0, 2.0, 1.0, 1.0, 1.0,  2.0, 1.0],
                    [ 0.0, 0.0, 1.0,  1.0, 1.0, 0.5, 0.5, 1.0,  1.0, 1.0],
                    [ 0.0, 0.0, 0.0,  0.0, 0.0, 0.0, 0.0, 0.0,  0.0, 0.0],
                    [ 0.0, 0.0, 0.0, -1.0, 0.0,-0.5,-0.5,-1.0,  0.0,-1.0],
                    [-1.0,-1.0,-2.0, -2.0,-2.0,-1.0,-1.0,-1.0, -2.0,-1.0],
                    [-1.0,-1.0,-2.0, -2.0,-2.0,-1.0,-1.0,-1.0, -2.0,-1.0],
                    [-1.0,-1.0,-2.0, -2.0,-2.0,-1.0,-1.0,-1.0, -2.0,-1.0],
                    [-1.0,-1.0,-2.0, -2.0,-2.0,-1.0,-1.0,-1.0, -2.0,-1.0],
                    [-1.0, 0.0, 0.0,  0.0,-1.0,-1.0,-1.0,-1.0, -2.0, 0.0]]

# Running count for the card counting system
CSYS_RUN_C = 0.0
# Remaining decks in shoe
REM_DECKS = 6

#
# Data Columns
# 
# Session Id - + INT, 
# Cumulative Games - + INT
# Games Simulated in Session - + INT, 
# Lifetime Avg Bet (x(Base)) - + FLOAT, 
# Lifetime winrate (W/L x(Base)) - +% FLOAT, 
# Lifetime Amount won (x(Base)) - + FLOAT, 
# Lifetime Amount loss (x(Base)) - + FLOAT, 
# Lifetime Amount push (x(Base)) - + FLOAT,
# Lifetime Net Gain/Loss (x(Base)) - +/- FLOAT
# Session Avg Bet (x(Base)) - + FLOAT, 
# Session winrate (W/L x(Base)) - +% FLOAT, 
# Session Amount won (x(Base)) - + FLOAT, 
# Session Amount loss (x(Base)) - + FLOAT, 
# Session Amount push (x(Base)) - + FLOAT,
# Session Net Gain/Loss (x(Base)) - +/- FLOAT 
#
def main():
    global WINS
    global LOSSES
    global PUSHES
    global LIFETIME_WINS
    global LIFETIME_LOSSES
    global LIFETIME_PUSHES
    global GAMES_PLAYED
    totalSessions = 10000
    numsim = 1000
    for csys in range(len(CSYS_NAME)):
        data = {'Session ID':[], 'Cumulative Games': [], 'Games Simulated in Session':[],'Games Played in Session':[], 'Lifetime Avg Bet (Xbase)':[], 'Lifetime winrate (W/L x(Base))': [], 'Lifetime Amount won (Xbase)':[], 'Lifetime Amount loss (Xbase)':[], 'Lifetime Amount push (Xbase)':[], 'Lifetime Net Gain/Loss (Xbase)': [], 'Session Avg Bet (Xbase)':[], 'Session winrate (W/L x(Base))': [], 'Session Amount won (Xbase)':[], 'Session Amount loss (Xbase)':[], 'Session Amount push (Xbase)':[], 'Session Net Gain/Loss (Xbase)': []}
        sessionid = 1
        LIFETIME_WINS = 0.0
        LIFETIME_LOSSES = 0.0
        LIFETIME_PUSHES = 0.0
        while (sessionid <= totalSessions):
            i = 1
            while (i <= numsim):
                play_game(csys)
                i += 1
            data['Session ID'].append(sessionid)
            data['Cumulative Games'].append(sessionid * numsim)
            data['Games Simulated in Session'].append(numsim)
            data['Games Played in Session'].append(GAMES_PLAYED)
            data['Lifetime Avg Bet (Xbase)'].append(round((LIFETIME_WINS+LIFETIME_LOSSES+LIFETIME_PUSHES)/(float(numsim) * float(sessionid)), 3))
            data['Lifetime winrate (W/L x(Base))'].append(round((LIFETIME_WINS)/(LIFETIME_WINS+LIFETIME_LOSSES) * 100.0, 3))
            data['Lifetime Amount won (Xbase)'].append(round(LIFETIME_WINS, 3))
            data['Lifetime Amount loss (Xbase)'].append(round(LIFETIME_LOSSES, 3))
            data['Lifetime Amount push (Xbase)'].append(round(LIFETIME_PUSHES, 3))
            data['Lifetime Net Gain/Loss (Xbase)'].append(round(LIFETIME_WINS - LIFETIME_LOSSES, 3))
            data['Session Avg Bet (Xbase)'].append(round((WINS+LOSSES+PUSHES)/(float(numsim)), 3))
            data['Session winrate (W/L x(Base))'].append(round((WINS)/(WINS+LOSSES) * 100.0, 3))
            data['Session Amount won (Xbase)'].append(round(WINS, 3))
            data['Session Amount loss (Xbase)'].append(round(LOSSES, 3))
            data['Session Amount push (Xbase)'].append(round(PUSHES, 3))
            data['Session Net Gain/Loss (Xbase)'].append(round(WINS - LOSSES, 3))
            sessionid += 1
            WINS = 0.0
            LOSSES = 0.0
            PUSHES = 0.0
            GAMES_PLAYED = 0.0
            print('Percent Done: ', round(float(sessionid)/float(totalSessions)* 100.00, 2), "%", end='\r\r\r\r\r\r\r', flush=True)
        file = 'counting_'+ CSYS_NAME[csys] +'_data.csv'
        print(file)
        dataFrame = pd.DataFrame.from_dict(data)
        dataFrame.to_csv(file, index=False)

GAMES_PLAYED = 0 # Games played in session
BASE = 1.0 # Base bet amount
# Simulates one game of counting strategy blackjack
# csys - the counting strategy
def play_game(csys):
    global GAMES_PLAYED
    bet = BASE
    trueCount = math.floor(CSYS_RUN_C/float(REM_DECKS))
    if (trueCount >= 2.0):
        GAMES_PLAYED += 1
        bet *= trueCount - 1.0
    else:
        bet *= 0.0
    nc1 = hit(csys)
    nc2 = hit(csys)
    nc3 = hit(csys)
    nc4 = hit(csys)
    pVals = [Hand(0, bet, [nc1])]
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
            update_game_state(gameState, currHand, decision, csys)
            if (decision == 3 or decision == 1):
                currHand = gameState.pop_hand()
    gameState.dealer_draw(csys)
    gameState.evaluate_game_state()

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

# Draws a card without replacement, shuffles after SHUFFLE_AFTER amount of decks
# csys - the card counting system to update
def hit(csys):
    global EXCLUDE
    global CSYS_RUN_C
    global REM_DECKS
    totEachCard = NUM_NORM_CARDS * NUM_DECKS
    if (len(EXCLUDE) >= NUM_NORM_CARDS * SHUFFLE_AFTER * 13):
        EXCLUDE = []
        CSYS_RUN_C = 0.0
    h = r.choice(list(set([x for x in range(1, totEachCard * 13)]) - set(EXCLUDE)))
    EXCLUDE.append(h)
    REM_DECKS = NUM_DECKS - math.floor(float(len(EXCLUDE))/float(NUM_NORM_CARDS * 13))
    if   (0  * totEachCard  < h <= totEachCard * 1 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[0][csys]
        return 2
    elif (1  * totEachCard  < h <= totEachCard * 2 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[1][csys]
        return 3
    elif (2  * totEachCard  < h <= totEachCard * 3 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[2][csys]
        return 4
    elif (3  * totEachCard  < h <= totEachCard * 4 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[3][csys]
        return 5
    elif (4  * totEachCard  < h <= totEachCard * 5 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[4][csys]
        return 6
    elif (5  * totEachCard  < h <= totEachCard * 6 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[5][csys]
        return 7
    elif (6  * totEachCard  < h <= totEachCard * 7 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[6][csys]
        return 8
    elif (7  * totEachCard  < h <= totEachCard * 8 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[7][csys]
        return 9
    elif (8  * totEachCard  < h <= totEachCard * 9 ):
        CSYS_RUN_C += CVAL_TRANSPOSE[8][csys]
        return 10
    elif (9  * totEachCard  < h <= totEachCard * 10):
        CSYS_RUN_C += CVAL_TRANSPOSE[9][csys]
        return 10
    elif (10 * totEachCard  < h <= totEachCard * 11):
        CSYS_RUN_C += CVAL_TRANSPOSE[10][csys]
        return 10
    elif (11 * totEachCard  < h <= totEachCard * 12):
        CSYS_RUN_C += CVAL_TRANSPOSE[11][csys]
        return 10
    else:
        CSYS_RUN_C += CVAL_TRANSPOSE[12][csys]
        return 11

# Applies given decision to gamestate
#
# currGameState - current state of the game
# currHand - current hand for the decision
# decision - the action applied to the current hand
def update_game_state(currGameState, currHand, decision, csys):
    if (decision == 1 or decision == 2):
        nc = hit(csys)
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
        nc1 = hit(csys)
        nc2 = hit(csys)
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
                LIFETIME_WINS += h.betSize * 1.5
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
    def dealer_draw(self, csys):
        while (sum(self.dHand) > 21 and 11 in self.dHand):
            if (not(11 in self.dHand)):
                break
            self.dHand[self.dHand.index(11)] = 1
        while (sum(self.dHand) < 17):
            c = hit(csys)
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