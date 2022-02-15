from typing import Any, Tuple, List
from hand import Hand
from card import Card


class Player:
    def __init__(self, name: Any, hand: Hand):
        self.name: Any = name
        self.hand: Hand = hand
        self.can_see_deck_card: bool = False
        self.asked_to_finish: bool = False
        self.turn_style: Tuple[str, List[int]] = None, None   # (type, [cards index])
