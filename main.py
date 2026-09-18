from deck import Deck
from player import Player
from states import States as S
from hand_evaluator import HandEval as H
import random as r


names = ["Ava", "Liam", "Maya", "Noah", "Zoe", "Ethan", "Priya", "Kai", "Isla", "Diego"]
starting_chips = 1000
players = [Player(starting_chips, name) for name in r.sample(names, 4)]
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

    # showdown
    still_in = [p for p in players if not p._folded]

    if len(still_in) == 1:
        winners = still_in
        print(f"\n{winners[0]._name} wins {s._pot} chips, everyone else folded.")
    else:
        print("\n--- Showdown ---")
        e = H([p._hand for p in players], board, players)
        winners = e.show_down()

    # pay out the pot (odd chips go to the first winner)
    share = s._pot // len(winners)
    left_over = s._pot - (share * len(winners))
    for w in winners:
        w._chips += share
    winners[0]._chips += left_over

    s.print_status()

    # kick out anyone who ran out of chips
    for p in list(players):
        if p._chips <= 0:
            print(f"{p._name} is out of chips and leaves the table.")
            players.remove(p)

    if len(players) < 2:
        print(f"\n{players[0]._name} wins the game with {players[0]._chips} chips!")
        running = False
        break

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

print("Thanks for playing!")