from deck import Deck
from player import Player
from states import States as S
import random as r
import numpy as np


names = ["Ava", "Liam", "Maya", "Noah", "Zoe", "Ethan", "Priya", "Kai", "Isla", "Diego"]
starting_chips = 1000
players = [Player(starting_chips, r.choice(names)) for i in range(4)]
running = True

while running:
    # reset deck + hands
    deck = Deck()
    board = []
    for p in players:
        p._hand = []
        p._amount_in_pot = 0
        p._sceen_cards = []
        p._folded = False
    s = S(deck, players, board)

    # pre-flop
    s.deal()
    for i in players:
        print(i._hand)

    # flop
    s.print_status()
    s.deal_flop()
    s.run_betting_round()

    # turn
    s.print_status()
    s.deal_turn()
    s.run_betting_round()

    # river
    s.print_status()
    s.deal_river()
    s.run_betting_round()
    

    print(f"Total pot: {s._pot}")
    
    # keep playing?
    asking = True
    while asking:
        cont = input("Would you like to keep playing? (Y/N): ")
        if cont.upper() == "Y":
            asking = False
        elif cont.upper() == "N":
            running = False
            asking = False
        else:
            print("Input was no recognized please try again.")