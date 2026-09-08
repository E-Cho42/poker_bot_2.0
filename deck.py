#imports
import random as r 


class Deck:
    # init
    def __init__(self):
        _ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        _suits = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades
        self._deck = [rank + suit for rank in _ranks for suit in _suits]
        
    
    #draw 
    def draw(self):
        _card_i = r.randint(0,len(self._deck)-1)
        _card = self._deck[_card_i]
        self._deck.remove(_card)
        return _card
    
    def print_cards_left(self):
        print(f"cards left = {len(self._deck)}, cards in deck{self._deck}")
        
    