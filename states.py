# imports:
from deck import Deck
from player import Player


class States():
    #inits
    def __init__(self, _deck, _players, _board):
        self._deck = _deck
        self._players = _players
        self._board = _board
        self._pot = 0

    #print status: who's still in + chip counts
    def print_status(self):
        print("\n--- Table status ---")
        for p in self._players:
            status = "folded" if p._folded else "in"
            print(f"{p._name}: {p._chips} chips ({status})")
        print("--------------------\n")

    #deal func
    def deal(self):
        for i in range(2):
            for p in self._players:
                p._hand.append(self._deck.draw())

        return self._deck, self._players

    #deal_flop fuc
    def deal_flop(self):
        flop = [self._deck.draw() for i in range(3)]
        self._board.append(flop[0])
        self._board.append(flop[1])
        self._board.append(flop[2])
        print(f"Flop came: {flop[0]}, {flop[1]}, {flop[2]}")

        for p in self._players:
            p._sceen_cards.append(flop[0])
            p._sceen_cards.append(flop[1])
            p._sceen_cards.append(flop[2])

        return self._deck, self._players, self._board

    #deal turn function
    def deal_turn(self):
        turn = self._deck.draw()
        self._board.append(turn)
        print(f'Turn came {turn}. \nBoard is now: {self._board[0]}, {self._board[1]}, {self._board[2]}, {self._board[3]}')

        for p in self._players:
            p._sceen_cards.append(turn)

        return self._deck, self._players, self._board

    #deal river funtion
    def deal_river(self):
        river = self._deck.draw()
        self._board.append(river)
        print(f'River came {river}. \nBoard is now: {self._board[0]}, {self._board[1]}, {self._board[2]}, {self._board[3]}, {self._board[4]}')

        for p in self._players:
            p._sceen_cards.append(river)

        return self._deck, self._players, self._board

    #runs a full betting round for one street (resets bets, loops until settled)
    def run_betting_round(self):
        for p in self._players:
            p._amount_in_pot = 0

        cur_bet = 0
        first_round = True
        betting = True

        while betting:
            active = [pc for pc in self._players if not pc._folded]

            if len(active) <= 1:
                betting = False
                break

            amounts_in = [pc._amount_in_pot for pc in active]
            all_equal = all(x == amounts_in[0] for x in amounts_in)

            if all_equal and not first_round:
                betting = False
                break

            for p in range(len(self._players)):
                cur_bet = self.post_flop_action(p, cur_bet)

            first_round = False
        self._pot += sum(p._amount_in_pot for p in self._players)

    #post flop action:
    def post_flop_action(self, p, _cur_bet):
        if self._players[p]._folded:
            return _cur_bet

        player = self._players[p]
        print(f'Your Hand is: {player._hand[0]}, {player._hand[1]}, you have: {player._chips} chips left.')

        if _cur_bet == 0:
            asking = True
            while asking:
                cob = input(f"({player._name}) would you like to check or bet? (C/B): ")
                if cob.upper() == "C":
                    print(f"{player._name} checks.")
                    asking = False
                    return _cur_bet
                elif cob.upper() == "B":
                    bet = input(f"({player._name}) how much would you like to bet?: ")
                    try:
                        bet = int(bet)
                        if bet > player._chips:
                            print("Bet was not accepted please try again, insufficient chips")
                            continue
                        player._chips -= bet
                    except:
                        print("Bet was not accepted please try again")
                        continue
                    print(f"{player._name} bets {bet}.")
                    _cur_bet = bet
                    player._amount_in_pot += bet
                    asking = False
                else:
                    print("Input was no recognized please try again.")

        else:
            asking = True
            while asking:
                to_call = _cur_bet - player._amount_in_pot

                if to_call == 0:
                    return _cur_bet

                cfr = input(f"({player._name}) the current bet is {_cur_bet}, you need {to_call} to call. Raise, call, or fold? (R/C/F): ")
                if cfr.upper() == "F":
                    print(f"{player._name} has folded")
                    player._folded = True
                    asking = False
                elif cfr.upper() == "C":
                    if player._chips - to_call >= 0:
                        player._chips -= to_call
                        player._amount_in_pot += to_call
                        print(f"{player._name} has called")
                    else:
                        print("Not enough chips to call, please try again.")
                        continue
                    asking = False
                elif cfr.upper() == "R":
                    raise_amt = input(f"({player._name}) how much would you like to raise to?: ")
                    try:
                        raise_amt = int(raise_amt)
                    except:
                        print("Raise was not accepted, please enter a number.")
                        continue

                    if raise_amt <= _cur_bet:
                        print(f"Raise must be more than the current bet of {_cur_bet}.")
                        continue

                    additional = raise_amt - player._amount_in_pot
                    if additional > player._chips:
                        print("Raise was not accepted, insufficient chips.")
                        continue

                    player._chips -= additional
                    player._amount_in_pot = raise_amt
                    _cur_bet = raise_amt
                    print(f"{player._name} raises to {raise_amt}.")
                    asking = False
                else:
                    print("Input was no recognized please try again.")

        return _cur_bet