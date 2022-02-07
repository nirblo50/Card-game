class Player:
    def __init__(self, name, hand):
        self.__name = name
        self.__hand = hand
        self.__score = 0

    @property
    def name(self):
        return self.__name

    @property
    def score(self):
        return self.__score

    @property
    def hand(self):
        return self.__hand

    def update_hand(self, hand):
        self.__hand = hand

