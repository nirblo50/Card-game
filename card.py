CARD_TYPES = {"Clubs": "Black", "Spades": "Black", "Diamonds": "Red",
              "Hearts": "Red"}
CARD_VALUES = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
               "9": 9, "10": 10, "J": 10,
               "Q": 11, "K": 12}


class Card:
    def __init__(self, value, _type, color):
        self.__value = value
        self.__type = _type
        self.__color = color

    @property
    def value(self):
        return self.__value

    @property
    def real_value(self):
        return CARD_VALUES[self.__value]

    @property
    def type(self):
        return self.__type

    @property
    def color(self):
        return self.__color

    def __eq__(self, other):
        if isinstance(other, Card):
            return other.type == self.__type and other.value == self.__value \
                   and other.color == self.__color
        return False

    def __repr__(self):
        return f"({self.__value}, {self.__type}, {self.__color})"

    def __str__(self):
        return f"({self.__value}, {self.__type}, {self.__color})"
