import random as r
import time
import numpy as np

EXCLUDE = []
DAS = True
SURR = False
NUM_DECKS = 8
SHUFFLE_AFTER = 4
NUM_NORM_CARDS = 4

SURR_SOL =  np.array([[0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]])

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

PAIR_SOL =  np.array([[0,0,3,3,3,3,0,0,0,0],
                    [0,0,3,3,3,3,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [0,3,3,3,3,0,0,0,0,0],
                    [3,3,3,3,3,3,0,0,0,0],
                    [3,3,3,3,3,3,3,3,3,3],
                    [3,3,3,3,3,0,3,3,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [3,3,3,3,3,3,3,3,3,3]])


def main():
    intro_options()
    while (True):
        time.sleep(1) 
        play_game()

def optimal_solution(pv1, pv2, dv): 
    # 0 = Stand
    # 1 = Hit
    # 2 = Double Down
    # 3 = Split
    # 4 = SURRender
    
    if (SURR):
        SURR_SOL[0][8] = 4
        for i in range(7,10):
            SURR_SOL[1][i] = 4

    pv = pv1 + pv2

    if (SURR and not(pv1 == pv2) and (pv == 16 or pv == 15) 
            and (dv == 9 or dv == 10 or (dv == 11 and pv == 16))):
        if (pv == 16):
            return SURR_SOL[1][dv -2]
        else:
            return SURR_SOL[0][8]
    else:
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

        if (DAS):
            PAIR_SOL[4][0] = 3
            for i in range(3,5):
                PAIR_SOL[4][i] = 3
            for i in range(0,2):
                PAIR_SOL[1][i] = 3
            for i in range(0,2):
                PAIR_SOL[0][i] = 3
        if (not(PAIR_SOL[pv1 - 2][dv - 2] == 3)):
            return optimal_solution(pv, 0, dv)
        return PAIR_SOL[pv1 - 2][dv - 2]

def play_game():
    pVals = {0:[(0,[hit()])]}
    dVals = [hit()]
    pVals[0][0][1].append(hit())
    dVals.append(hit())
    gameState = Game_State(pVals, dVals, pVals[0].copy())
    while (not(gameState.is_stack_empty())):
        currHand = gameState.pop_hand()
        splitable = len(currHand[1]) == 2 and currHand[1][0] == currHand[1][1] 
        decision = ""
        if (decision == ""):
            prompt(gameState, currHand, splitable)
        while (not(decision == '0' or decision == '2' or decision == '4' or (decision == '1' and currHand[0]>0 and currHand[1][0] == 11) or sum(currHand[1]) > 21)):
            dec_args = ["str(input())",
                        "not(checked_input == '0' or checked_input == '1' or checked_input == '2' or checked_input == '3' or checked_input == '4')",
                        "print('    Invalid Input, Choose Decision: ', end='')"]
            decision = validate_decision(currHand, splitable, dec_args)
            update_game_state(gameState, currHand, decision)
            if (not(decision == '0' or decision == '4')):
                currHand = gameState.pop_hand()
                splitable = len(currHand[1]) == 2 and currHand[1][0] == currHand[1][1]
            if (not(decision == '0' or decision == '2' or decision == '4' or (decision == '1' and currHand[0]>0 and currHand[1][0] == 11) or sum(currHand[1]) > 21)):
                prompt(gameState, currHand, splitable)
    while (sum(gameState.dHand) < 17):
        gameState.dHand.append(hit())
    evaluate_game_state(gameState, sum(gameState.dHand))

def intro_options():
    global DAS
    global SURR
    global NUM_DECKS
    global SHUFFLE_AFTER

    print("__________________________________________________________________________\n")
    print("    Select Game Options")
    print("__________________________________________________________________________\n")

    print("    Default settings (yes or no): ", end ='')
    def_arg = ["str(input()).lower()", "not(checked_input == 'yes' or checked_input == 'no')",
                 "print('    Invalid Input, (yes or no): ', end='')"]
    default_in = validate_input(str(input()).lower(), def_arg[0], def_arg[1], def_arg[2])
    
    if (default_in == 'no'):
        print("    Double on split (yes or no): ", end ='')
        das_arg = ["str(input()).lower()", "not(checked_input == 'yes' or checked_input == 'no')",
                     "print('    Invalid Input, (yes or no): ', end='')"]
        das_in = validate_input(str(input()).lower(), das_arg[0], das_arg[1], das_arg[2])
        DAS = das_in == 'yes'

        print("    Surrender allowed (yes or no): ", end ='')
        surr_arg = ["str(input()).lower()", "not(checked_input == 'yes' or checked_input == 'no')",
                     "print('    Invalid Input, (yes or no): ', end='')"]
        surr_in = validate_input(str(input()).lower(), surr_arg[0], surr_arg[1], surr_arg[2])
        SURR = surr_in == 'yes'

        print("    Number of decks: ", end ='')
        num_decks_arg = ["str(input())", "not(checked_input.isnumeric())",
                         "print('    Invalid Input, (Integers Only): ', end='')"]
        num_decks_in = validate_input(str(input()), num_decks_arg[0], num_decks_arg[1], num_decks_arg[2])
        NUM_DECKS = int(num_decks_in)

        print("    Shuffle after N decks: ", end ='')
        shuffle_after_in = str(input())
        while (not(shuffle_after_in.isnumeric()) or int(shuffle_after_in) > NUM_DECKS):
            if (not(shuffle_after_in.isnumeric())):
                print("    Invalid Input, (Integers Only): ", end='')
            elif (int(shuffle_after_in) > NUM_DECKS):
                print("    Invalid Input, (Must be lower or equal to number of decks): ", end='')
            shuffle_after_in = str(input())
        SHUFFLE_AFTER = int(shuffle_after_in)

def prompt(gameState, currHand, splitable):
    print("\n"*100,"__________________________________________________________________________\n")
    print("    Double on split: ", DAS)
    print("    Surrender: ", SURR)
    print("    Number of decks: ", NUM_DECKS)
    print("    Shuffle after N decks: ", SHUFFLE_AFTER)
    print("__________________________________________________________________________\n")
    print("    Dealer card shown: ", to_string(gameState.dHand[0]), "\n")
    i = 1
    for k in gameState.pHands:
        for pHand in gameState.pHands[k]:
            print("    Player hand", i, ": ", print_hand(pHand[1]), "\n")
            i += 1 
    options = "    0 = Stand | 1 = Hit | 2 = Double Down | 3 = Split | 4 = Surrender\n"
    print_options(currHand, splitable, options)
    print("    Choose Decision for hand", gameState.pHands[currHand[0]].index(currHand) + 1, ": ", end ='')

def hit():
    global EXCLUDE
    if (len(EXCLUDE) > NUM_NORM_CARDS * SHUFFLE_AFTER * 13 + 1):
        EXCLUDE = []
    num = r.randint(1, NUM_NORM_CARDS * NUM_DECKS * 13 + 1)
    EXCLUDE.append(num)
    h = r.choice(list(set([x for x in range(1, NUM_NORM_CARDS * NUM_DECKS * 13 + 1)]) - set(EXCLUDE)))
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

def print_options(currHand, splitable, options):
    if (len(currHand[1]) == 2 and splitable): # Two cards identical cards in hand
        if (SURR): # Split available, surrender available, double down available
            print(options)
        else: # Split available, surrender unavailable
            if (currHand[0]>0): # Split available, surrender unavailable, double down unavailable
                print(options[:23], options[42:53], "\n")
            else: # Split available, surrender unavailable, double down available
                print(options[:53], "\n")
    elif (len(currHand[1]) == 1): # One card in hand
        if (SURR): # Surrender available, split unavailable
            if (DAS and currHand[0]>0): # Surrender available, double down available on DAS, split unavailable
                print(options[:41], options[53:])
            else: # Surrender available, double down unavailable, split unavailable
                print(options[:23], options[53:])
        else:
            if (not(DAS) and currHand[0]>0): # Surrender unavailable, double down unavailable, split unavailable
                print(options[:23],"\n")
            else: # Surrender unavailable, double down available, split unavailable
                print(options[:41],"\n")
    else: # Two distinct cards in hand or more than two cards
        if (SURR): # Surrender availiable, split unavailable
            if (currHand[0]==0): # Surrender availiable, split unavailable, double down available
                print(options[:41], options[53:])
            else: # Surrender availiable, split unavailable, double down unavailable
                print(options[:23], options[53:])
        else: # Surrender unavailable, split unavailable
            if (currHand[0]==0 and len(currHand[1]) == 2): # Surrender unavailable, split unavailable, double down available
                print(options[:41],"\n")
            else: # Surrender unavailable, split unavailable, double down unavailable
                print(options[:23],"\n")

def validate_decision(currHand, splitable, dec_args):
    decision = ''
    if (len(currHand[1]) == 2 and splitable): # Two cards identical cards in hand
        if (SURR): # Split available, surrender available, double down available
            decision = validate_input(str(input()), dec_args[0], dec_args[1], dec_args[2])
        else: # Split available, surrender unavailable
            if (currHand[0]>0): # Split available, surrender unavailable, double down unavailable
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:48] + dec_args[1][72:96] + ')', dec_args[2])
            else: # Split available, surrender unavailable, double down available
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:96] + ')', dec_args[2])
    elif (len(currHand[1]) == 1): # One card in hand
        if (SURR): # Surrender available, split unavailable
            if (DAS and currHand[0]>0): # Surrender available, double down available on DAS, split unavailable
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:72] + dec_args[1][96:], dec_args[2])
            else: # Surrender available, double down unavailable, split unavailable
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:48] + dec_args[1][96:], dec_args[2])
        else:
            if (not(DAS) and currHand[0]>0): # Surrender unavailable, double down unavailable, split unavailable
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:48] + ')', dec_args[2])
            else: # Surrender unavailable, double down available, split unavailable
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:72] + ')', dec_args[2])
    else: # Two distinct cards in hand or more than two cards
        if (SURR): # Surrender availiable, split unavailable
            if (currHand[0]==0): # Surrender availiable, split unavailable, double down available
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:72] + dec_args[1][96:], dec_args[2])
            else: # Surrender availiable, split unavailable, double down unavailable
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:48] + dec_args[1][96:], dec_args[2])
        else: # Surrender unavailable, split unavailable
            if (currHand[0]==0 and len(currHand[1]) == 2): # Surrender unavailable, split unavailable, double down available
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:72] + ')', dec_args[2])
            else: # Surrender unavailable, split unavailable, double down unavailable
                decision = validate_input(str(input()), dec_args[0], dec_args[1][:48] + ')', dec_args[2])
    return decision

def to_string(cVal):
    cvs = ''
    fMap = {0:'10', 1:'J', 2:'Q', 3:'K'}
    if (cVal == 11):
        cvs = 'A'
    elif (cVal == 10):
        cvs = fMap[r.randint(0,3)]
    else:
        cvs = str(cVal)
    return cvs

def validate_input(inp, inp_type, valOn, err_out):
    checked_input = inp
    while (eval(valOn)):
            eval(err_out)
            checked_input = eval(inp_type)
    return checked_input

def print_hand(hand):
    hString = ""
    for i in range(len(hand)):
        hString = hString + to_string(hand[i]) + "   "
    return hString

def update_game_state(currGameState, currHand, decision):
    if (decision == '1'):
        currHand[1].append(hit())
        currGameState.push_hand(currHand)
    elif (decision == '2'):
        currHand[1].append(hit())
        currGameState.push_hand(currHand)
    elif (decision == '3'):
        sHand1 = (currHand[0] + 1,[currHand[1][0]])
        sHand2 = (currHand[0] + 1,[currHand[1][1]])
        if (currHand[0] + 1 in currGameState.pHands):
            currGameState.pHands.update({currHand[0] + 1: currGameState.pHands[currHand[0] + 1] + [sHand1, sHand2]})
        else:
            currGameState.pHands.update({currHand[0] + 1: [sHand1, sHand2]})
        currGameState.push_hand(sHand1)
        currGameState.push_hand(sHand2)
        currGameState.pHands[currHand[0]].remove(currHand)

def evaluate_game_state(gameState, dTot):
    print("\n"*100)
    print("__________________________________________________________________________\n")
    print("    Results")
    print("__________________________________________________________________________\n")
    i = 1
    dealerHand = ""
    for card in gameState.dHand:
        dealerHand += to_string(card) + "  "
    print("\n    Dealer Hand: ", dealerHand[:len(dealerHand)-2])
    for k in gameState.pHands:
        for pHand in gameState.pHands[k]:
            handTotal = sum(pHand[1])
            handStr = ""
            for card in pHand[1]:
                handStr += to_string(card) + "  "
            if (handTotal > 21):
                print("\n    Hand", i,"(", handStr[:len(handStr)-2],"): Bust")
            elif (handTotal > dTot or dTot > 21):
                print("\n    Hand", i,"(", handStr[:len(handStr)-2],"): Win")
            elif (handTotal == dTot):
                print("\n    Hand", i,"(", handStr[:len(handStr)-2],"): Push")
            else:
                print("\n    Hand", i,"(", handStr[:len(handStr)-2],"): Loss")
            i += 1
    print("\n__________________________________________________________________________\n")
    print("\n"*10)

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
        print('player hands: ', self.pHands)
        print('dealer hand: ', self.dHand)
        print('hands with actions left: ', self.hStack)

if __name__ == "__main__":
    main()