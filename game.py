MAX_PLAYERS = 2


class Game:
    def __init__(self, game_id):
        self.__game_id: int = game_id
        self.__players = []     # list[(client_socket, client_address)]
        self.__data = ""

    def add_player(self, player):
        self.__players.append(player)

    def remove_player(self, player):
        self.__players.remove(player)

    def player_action(self, player, action):
        pass

    @property
    def game_id(self):
        return self.__game_id

    @property
    def players(self):
        return self.__players[:]

    @property
    def data(self):
        return self.__data

    def is_full(self):
        return len(self.__players) == MAX_PLAYERS

    def players_num(self):
        return len(self.__players)
