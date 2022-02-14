from card import Card
from functools import reduce
from typing import List


class Hand:
    def __init__(self) -> None:
        """
        Creates an empty hand
        """
        self.__hand: List[Card] = []

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the hand
        """
        self.__hand.append(card)

    def remove_card(self, card_index: int) -> Card:
        """
        Remove a certain card from the hand
        :param card_index: The index of the card to remove
        """
        return self.__hand.pop(card_index)

    def replace_card(self, card_index: int, card: Card) -> None:
        """
        Replace the card in a given index with another
        """
        self.__hand[card_index] = card

    def card_in(self, card_index: int) -> Card:
        return self.__hand[card_index]

    def hand_value(self) -> int:
        """
        :return: The sum value of all the cards in the hand
        """
        return reduce(lambda x, y: x + y.real_value, self.__hand, 0)

    @property
    def cards(self) -> List[Card]:
        """
        :return: A copy of the cards in the hand
        """
        return self.__hand[:]

    def __len__(self) -> int:
        return len(self.__hand)

    def __iter__(self) -> iter:
        return iter(self.__hand[:])

    def __repr__(self) -> str:
        return str(self.__hand)

    def __str__(self) -> str:
        return str(self.__hand)


if __name__ == '__main__':
    pass
