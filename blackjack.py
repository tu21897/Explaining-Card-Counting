from pickle import GLOBAL
import random as r
import time
import numpy as np

EXCLUDE = []
NUM_DECKS = 8
SHUFFLE_AFTER = 6
NUM_NORM_CARDS = 4

HARD_SOL =  np.array([[1,1,1,1,1,1,1,1,1,1],
                    [1,2,2,2,2,1,1,1,1,1],
                    [2,2,2,2,2,2,2,2,1,1],
                    [2,2,2,2,2,2,2,2,2,2],
                    [1,1,0,0,0,1,1,1,1,1],
                    [0,0,0,0,0,1,1,1,1,1],
                    [0,0,0,0,0,1,1,1,1,1],
                    [0,0,0,0,0,1,1,1,1,1],
                    [0,0,0,0,0,1,1,1,1,1],
                    [0,0,0,0,0,0,0,0,0,0]])

SOFT_SOL =  np.array([[1,1,1,2,2,1,1,1,1,1],
                    [1,1,1,2,2,1,1,1,1,1],
                    [1,1,2,2,2,1,1,1,1,1],
                    [1,1,2,2,2,1,1,1,1,1],
                    [1,2,2,2,2,1,1,1,1,1],
                    [2,2,2,2,2,0,0,1,1,1],
                    [0,0,0,0,2,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]])

PAIR_SOL =  np.array([[3,3,3,3,3,3,0,0,0,0],
                    [3,3,3,3,3,3,0,0,0,0],
                    [0,0,0,3,3,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [3,3,3,3,3,0,0,0,0,0],
                    [3,3,3,3,3,3,0,0,0,0],
                    [3,3,3,3,3,3,3,3,3,3],
                    [3,3,3,3,3,0,3,3,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [3,3,3,3,3,3,3,3,3,3]])

WINS = 0.0
LOSSES = 0.0
PUSHES = 0.0
GAMES = 0.0

def main():
    i = 1
    while (i <= 1000):
        print("----------------------- Game", i, "-----------------------")
        play_game()
        i += 1
    print("Wins :", WINS)
    print("Losses :", LOSSES)
    print("Pushes :", PUSHES)
    print("# Games in terms of bets :", GAMES)
    print("Winrate :", WINS/(WINS+ LOSSES) * 100.0, "%")

def basic_strategy(pv1, pv2, dv): 
    # 0 = Stand
    # 1 = Hit
    # 2 = Double Down
    # 3 = Split

    pv = pv1 + pv2

    if (pv1 == 10 and pv2 == 10):
        return 0
    if (not(pv2 == 11 and pv1 == 11) and not(pv1 == pv2)):
        if (pv < 9):
            return 1
        elif (pv > 17):
            return 0
        return HARD_SOL[pv - 8][dv-2]
    if (not(pv1 == pv2) and (pv1 == 11 or pv2 == 11) and not(pv == 21)):
        return SOFT_SOL[pv-13][dv-2]
    if (not(PAIR_SOL[pv1 - 2][dv - 2] == 3)):
        return basic_strategy(pv, 0, dv)
    return PAIR_SOL[pv1 - 2][dv - 2]

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
            if (len(currHand.hand) > 2 or len(currHand.hand) == 1 or currHand.splitnum > 2):
                decision = basic_strategy(sum(currHand.hand), 0, gameState.dHand[0])
            else:
                decision = basic_strategy(currHand.hand[0], currHand.hand[1], gameState.dHand[0])
            update_game_state(gameState, currHand, decision)
            if (not(decision == 0 or decision == 2)):
                currHand = gameState.pop_hand()
    dVal = sum(gameState.dHand)
    while (dVal < 17):
        gameState.dHand.append(hit())
        dVal = sum(gameState.dHand)
        if (dVal > 21 and 11 in gameState.dHand):
            gameState.dHand[gameState.dHand.index(11)] = 1
            dVal = sum(gameState.dHand)
    evaluate_game_state(gameState, dVal)

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

def evaluate_game_state(gameState, dTot):
    global WINS
    global LOSSES
    global PUSHES
    global GAMES

    i = 1
    dealerHand = ""
    for card in gameState.dHand:
        dealerHand += to_string(card) + "  "
    print("\n    Dealer Hand: ", dealerHand[:len(dealerHand)-2])
    for h in gameState.pHands:
        handTotal = sum(h.hand)
        handStr = ""
        for card in h.hand:
            handStr += to_string(card) + "  "
        if (handTotal > 21):
            print("\n    ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Bust")
            LOSSES += h.betSize
            GAMES += h.betSize
        elif (handTotal > dTot or dTot > 21):
            print("\n    ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Win")
            WINS += h.betSize
            GAMES += h.betSize
        elif (handTotal == dTot):
            print("\n    ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Push")
            PUSHES += h.betSize
            GAMES += h.betSize
        else:
            print("\n    ",h.betSize," Hand", i,"(", handStr[:len(handStr)-2],"): Loss")
            LOSSES += h.betSize
            GAMES += h.betSize
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