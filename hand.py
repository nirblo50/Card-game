from card import Card
from functools import reduce


class Hand:
    def __init__(self):
        """
        Creates an empty hand
        """
        self.__hand: list[Card] = []

    def add_card(self, card):
        """
        Adds a card to the hand
        """
        self.__hand.append(card)

    def remove_card(self, card_index: int):
        """
        Remove a certain card from the hand
        :param card: The card to remove
        """
        return self.__hand.pop(card_index)

    def hand_value(self):
        """
        :return: The sum value of all the cards in the hand
        """
        return reduce(lambda x, y: x + y.real_value, self.__hand, 0)

    @property
    def cards(self):
        """
        :return: A copy of the cards in the hand
        """
        return self.__hand[:]

    def __len__(self):
        return len(self.__hand)

    def __iter__(self):
        return iter(self.__hand[:])

    def __repr__(self):
        return str(self.__hand)

    def __str__(self):
        return str(self.__hand)


if __name__ == '__main__':
    hand = Hand()
    hand.add_card(Card("4", "Clubs", "Black"))
    hand.add_card(Card("5", "Hearts", "Red"))
    hand.add_card(Card("6", "Clubs", "Black"))
    hand.add_card(Card("7", "Hearts", "Red"))
