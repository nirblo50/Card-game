class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
        self.score = 0
        self.can_see_deck_card = False
        self.asked_to_finish = False
