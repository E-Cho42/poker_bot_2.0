class HandEval:
    RANK_MAP = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    HAND_NAMES = {
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "Pair",
        0: "High Card"
    }

    def __init__(self, hands, board, players):
        self.hands = hands
        self.board = board
        self.players = players

    def hand_high_card(self, hand):
        """Returns the numerical rank of the highest card in hand."""
        return max(self.RANK_MAP[card[0]] for card in hand)

    def get_counts(self, hand):
        """Returns {rank_value: how many times it appears} across hand + board."""
        full_hand = hand + self.board
        counts = {}
        for card in full_hand:
            value = self.RANK_MAP[card[0]]
            counts[value] = counts.get(value, 0) + 1
        return counts

    def flush_suit(self, hand):
        """Returns the suit that makes a flush, or None."""
        full_hand = hand + self.board
        suits = [card[1] for card in full_hand]
        for s in set(suits):
            if suits.count(s) >= 5:
                return s
        return None

    def has_flush(self, hand):
        """Checks if hand + board makes a 5-card flush."""
        return self.flush_suit(hand) is not None

    def flush_ranks(self, hand):
        """Returns the ranks of the flush suit, highest first."""
        suit = self.flush_suit(hand)
        if suit is None:
            return []
        full_hand = hand + self.board
        return sorted((self.RANK_MAP[c[0]] for c in full_hand if c[1] == suit), reverse=True)

    def straight_high(self, ranks):
        """Given a set of rank values, returns (True, top card) if 5 run in a row."""
        ranks = set(ranks)

        # Ace can act as 1 (low) or 14 (high)
        if 14 in ranks:
            ranks.add(1)

        sorted_ranks = sorted(ranks)
        consecutive = 0
        max_straight_rank = 0

        for i in range(len(sorted_ranks)):
            if i > 0 and sorted_ranks[i] == sorted_ranks[i - 1] + 1:
                consecutive += 1
            else:
                consecutive = 1

            if consecutive >= 5:
                max_straight_rank = sorted_ranks[i]

        if max_straight_rank > 0:
            return True, max_straight_rank
        return False, None

    def has_straight(self, hand):
        """Checks for a 5-card straight (including Ace-low wheel)."""
        full_hand = hand + self.board
        return self.straight_high(self.RANK_MAP[card[0]] for card in full_hand)

    def has_straight_flush(self, hand):
        """Checks for a straight made entirely of the flush suit."""
        suit = self.flush_suit(hand)
        if suit is None:
            return False, None
        full_hand = hand + self.board
        return self.straight_high(self.RANK_MAP[c[0]] for c in full_hand if c[1] == suit)

    def has_pair(self, hand):
        """Checks for a pair. Returns the highest one."""
        pairs = sorted([v for v, c in self.get_counts(hand).items() if c == 2], reverse=True)
        if pairs:
            return True, pairs[0]
        return False, None

    def has_two_pair(self, hand):
        """Checks for two pair. Returns the top two pair ranks."""
        pairs = sorted([v for v, c in self.get_counts(hand).items() if c == 2], reverse=True)
        if len(pairs) >= 2:
            return True, pairs[:2]
        return False, None

    def has_trips(self, hand):
        """Checks for three of a kind."""
        trips = sorted([v for v, c in self.get_counts(hand).items() if c == 3], reverse=True)
        if trips:
            return True, trips[0]
        return False, None

    def has_quads(self, hand):
        """Checks for four of a kind."""
        quads = sorted([v for v, c in self.get_counts(hand).items() if c == 4], reverse=True)
        if quads:
            return True, quads[0]
        return False, None

    def has_full_house(self, hand):
        """Checks for a full house. Returns [trip rank, pair rank]."""
        counts = self.get_counts(hand)
        trips = sorted([v for v, c in counts.items() if c == 3], reverse=True)
        pairs = sorted([v for v, c in counts.items() if c == 2], reverse=True)

        if not trips:
            return False, None

        # a second set of trips can be used as the pair
        options = pairs + trips[1:]
        if options:
            return True, [trips[0], max(options)]
        return False, None

    def kickers(self, hand, used, amount):
        """Highest cards not already part of the made hand, used for tie breaks."""
        full_hand = hand + self.board
        left = sorted((self.RANK_MAP[c[0]] for c in full_hand
                       if self.RANK_MAP[c[0]] not in used), reverse=True)
        return left[:amount]

    def best_hand(self, hand):
        """Returns (category, tie breakers) so two hands can be compared with > and ==."""
        is_sf, sf_high = self.has_straight_flush(hand)
        if is_sf:
            return 8, [sf_high]

        is_quads, quad_rank = self.has_quads(hand)
        if is_quads:
            return 7, [quad_rank] + self.kickers(hand, {quad_rank}, 1)

        is_boat, boat = self.has_full_house(hand)
        if is_boat:
            return 6, boat

        if self.has_flush(hand):
            return 5, self.flush_ranks(hand)[:5]

        is_straight, straight_high = self.has_straight(hand)
        if is_straight:
            return 4, [straight_high]

        is_trips, trip_rank = self.has_trips(hand)
        if is_trips:
            return 3, [trip_rank] + self.kickers(hand, {trip_rank}, 2)

        is_two_pair, two_pair = self.has_two_pair(hand)
        if is_two_pair:
            return 2, two_pair + self.kickers(hand, set(two_pair), 1)

        is_pair, pair_rank = self.has_pair(hand)
        if is_pair:
            return 1, [pair_rank] + self.kickers(hand, {pair_rank}, 3)

        return 0, self.kickers(hand, set(), 5)

    def hand_name(self, score):
        """Turns a best_hand score into something printable."""
        return self.HAND_NAMES[score[0]]

    def find_winners(self):
        """Compares every player still in the hand. Returns (winners, best score)."""
        best = None
        winners = []

        for p in self.players:
            if p._folded:
                continue

            score = self.best_hand(p._hand)

            if best is None or score > best:
                best = score
                winners = [p]
            elif score == best:
                winners.append(p)

        return winners, best

    def show_down(self):
        """Prints everyone's hand, then the winner(s), and splits the pot evenly."""
        for p in self.players:
            if p._folded:
                continue
            score = self.best_hand(p._hand)
            print(f"{p._name} shows {p._hand[0]}, {p._hand[1]} - {self.hand_name(score)}")

        winners, best = self.find_winners()

        if len(winners) == 1:
            print(f"{winners[0]._name} wins with {self.hand_name(best)}!")
        else:
            tied = ", ".join(w._name for w in winners)
            print(f"Split pot between {tied} with {self.hand_name(best)}!")

        return winners