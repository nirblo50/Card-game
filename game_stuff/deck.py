from game_stuff.card import Card, CARD_VALUES, CARD_TYPES
import random
from typing import List


class Deck:
    """
    This class represents a game deck with cards
    """
    def __init__(self) -> None:
        """
        Creates an empty deck
        """
        self.__deck: List[Card] = []

    def initialize(self) -> None:
        """
        Creates a full deck from all the cards
        """
        self.__deck = []
        for _value in CARD_VALUES:
            for _type, _color in CARD_TYPES.items():
                card = Card(_value, _type, _color)
                self.__deck.append(card)

    def shuffle(self) -> None:
        """
        Shuffles the deck randomly
        """
        random.shuffle(self.__deck)

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the top of the deck
        :param card: Card type object to add to the deck
        """
        self.__deck.append(card)

    def pop_card(self) -> Card:
        """
        Removes the top card from the deck and returns it
        :return: The top card in the deck (Card type)
        """
        return self.__deck.pop()

    def peek_top(self) -> Card:
        """
        Returns the top card without removing it from the deck
        :return: The top card in the deck (Card type)
        """
        return self.__deck[-1]

    def __len__(self) -> int:
        return len(self.__deck)

    def __iter__(self) -> iter:
        return iter(self.__deck)
