CARD_TYPES: dict[str, str] = {"Clubs": "Black",
                              "Spades": "Black",
                              "Diamonds": "Red",
                              "Hearts": "Red"}
CARD_VALUES: dict[str, int] = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                               "7": 7, "8": 8, "9": 9, "10": 10, "J": 10,
                               "Q": 10, "K": 10}


class Card:
    """
    This class represents a simple game card with value, type and color
    """

    def __init__(self, value: str, _type: str, color: str) -> None:
        self.__value = value
        self.__type = _type
        self.__color = color

    @property
    def value(self) -> str:
        return self.__value

    @property
    def numerical_value(self) -> int:
        """
        Numerical value of the card (how many points the card is worth)
        """
        return CARD_VALUES[self.__value]

    @property
    def type(self) -> str:
        return self.__type

    @property
    def color(self) -> str:
        return self.__color

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return other.type == self.__type and other.value == self.__value and \
               other.color == self.__color

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"({self.__value}, {self.__type}, {self.__color})"
