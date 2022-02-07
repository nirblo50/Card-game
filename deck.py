from card import Card, CARD_VALUES, CARD_TYPES
import random


class Deck:
    def __init__(self):
        """
        Creates an empty deck
        """
        self.__deck: list[Card] = []

    def initialize(self):
        """
        Creates a full deck from all the cards
        """
        for _value in CARD_VALUES:
            for _type, _color in CARD_TYPES.items():
                card = Card(_value, _type, _color)
                self.__deck.append(card)

    def shuffle(self):
        """
        Shuffles the deck randomly
        """
        random.shuffle(self.__deck)

    def add_card(self, card: Card):
        """
        Adds a card to the top of the deck
        :param card: Card type object to add to the deck
        """
        self.__deck.append(card)

    def pop_card(self):
        """
        Removes the top card from the deck and returns it
        :return: The top card in the deck (Card type)
        """
        return self.__deck.pop()

    def peek_top(self):
        """
        Returns the top card without removing it from the deck
        :return: The top card in the deck (Card type)
        """
        return self.__deck[-1]

    def __len__(self):
        return len(self.__deck)

    def __iter__(self):
        return iter(self.__deck)


if __name__ == '__main__':

    deck = Deck()
    deck.initialize()
    deck.shuffle()
