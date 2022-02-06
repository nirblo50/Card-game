from card import Card
import random

CARD_TYPES = {"Clubs": "Black", "Spades": "Black", "Diamonds": "Red",
              "Hearts": "Red"}
CARD_VALUES = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10,
               "Q":11, "K":12}


class Deck:
    def __init__(self, card_types, card_values):
        """
        Creates an empty deck
        :param card_types: dict[key: any, value: int]
        :param card_values:
        """
        self.__card_types: dict[any, any] = card_types
        self.__card_values: dict[any, int] = card_values
        self.__deck: list[Card] = []

    def initialize(self):
        """
        Creates a full deck from all the cards
        """
        for _value in self.__card_values:
            for _type, _color in self.__card_types.items():
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


deck = Deck(CARD_TYPES, CARD_VALUES)
deck.initialize()
deck.shuffle()
for d in deck:
    print(d)