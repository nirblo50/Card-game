from card import Card

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

    def hand_value(self):
        return sum(self.__hand, lambda x:)