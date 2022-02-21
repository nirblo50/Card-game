from typing import Any, Tuple, List, Union
from game_stuff.hand import Hand

Turn_style_type = Union[Tuple[str, List[int]], Tuple[None, None]]


class Player:
    """
    This class represents a player in 'Balouka card game'
    """
    def __init__(self, name: Any, hand: Hand) -> None:
        self.name: Any = name
        self.hand: Hand = hand
        self.can_see_deck_card: bool = False
        self.asked_to_finish: bool = False
        self.turn_style: Turn_style_type = None, None   # (turn_type, card_ind]
