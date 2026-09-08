class Player():
    #inits
    def __init__(self, _starting_chips, _name, _amount_in_pot=0):
        self._hand = []
        self._chips = _starting_chips
        self._sceen_cards = []
        self._name = _name
        self._amount_in_pot = _amount_in_pot
        self._folded = False