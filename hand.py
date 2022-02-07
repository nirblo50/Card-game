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

    def remove_card(self, card: Card):
        """
        Remove a certain card from the hand
        :param card: The card to remove
        """
        for index, my_card in enumerate(self.__hand):
            if my_card == card:
                self.__hand.pop(index)
                return

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
    pass