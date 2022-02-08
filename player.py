from typing import Any
from hand import Hand
class Player:
    def __init__(self, name: Any, hand: Hand):
        self.name: Any = name
        self.hand: Hand = hand
        self.can_see_deck_card: bool = False
        self.asked_to_finish: bool = False
