class Card:
    def __init__(self, value, type, color):
        self.__value = value
        self.__type = type
        self.__color = color

    @property
    def value(self):
        return self.__value

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

