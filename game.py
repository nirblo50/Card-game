from hand import Hand
from player import Player
from deck import Deck
from card import Card
from typing import Any, Union, Dict, List, Tuple

MAX_PLAYERS = 2
MIN_PLAYERS = 2
START_CARDS_NUM = 4

Game_status_type = Dict[str, Union[str, int, Card, Hand]]


class Game:
    def __init__(self, game_id) -> None:
        self.__game_id: int = game_id
        self.__players: Dict[Any, Player] = {}
        self.__deck: Deck = Deck()
        self.__garbage: List[Card] = []
        self.__turn: int = 0
        self.__has_started = False
        self.__game_won = False

    def start(self) -> None:
        """
        Starts the game
        """
        self.__has_started = True
        self.__deck.initialize()
        self.__deck.shuffle()
        self.__garbage.append(self.__deck.pop_card())
        self.deal_cards()

    def deal_cards(self) -> None:
        """
        Deal each player the starting cards
        """
        for _ in range(START_CARDS_NUM):
            for player in self.__players.values():
                card = self.__deck.pop_card()
                player.hand.add_card(card)

    def add_player(self, player_name: Any) -> None:
        """
        Add a player to the game
        :param player_name: The name of the new player
        """
        player = Player(player_name, Hand())
        self.__players[player_name] = player

    def remove_player(self, player_name: Any) -> None:
        """
        Remove a player from the game
        :param player_name: The player to remove
        """
        self.__players.pop(player_name)

        if len(self.__players) < MIN_PLAYERS:
            self.__has_started = False
            self.empty_hands()

    def empty_hands(self) -> None:
        """
        Empty all the player's hands and game data
        """
        for player in self.__players.values():
            player.hand = Hand()
            player.can_see_deck_card = False
            player.score = 0

    def player_make_action(self, player_name: Any,
                           action: str) -> Game_status_type:
        """
        Handles the actions from the player
        :param player_name: The name of the player that did the action
        :param action: The action itself
        :return: Card if needed or None
        """
        player_index = self.player_name_to_index(player_name)
        current_player = self.__players[player_name]

        if self.__game_won:
            return self.handle_game_won(current_player)

        if not self.has_started():
            return "Game did not start yet"

        # If This is not this player's turn
        if player_index is not self.__turn:
            return self.get_game_status(current_player)

        elif action == "Try my luck":
            current_player.asked_to_finish = True

        elif action == "Show top card from deck":
            current_player.can_see_deck_card = True
            return self.get_game_status(current_player)

        elif action.startswith("Throw card from hand"):
            if current_player.can_see_deck_card:
                card_index = int(action[-1])
                self.take_from_deck_and_throw(current_player, card_index)

        elif action == "Throw card from deck":
            if current_player.can_see_deck_card:
                self.__garbage.append(self.__deck.pop_card())
        else:
            return self.get_game_status(current_player)

        current_player.can_see_deck_card = False
        self.next_turn()
        return self.get_game_status(current_player)

    def take_from_deck_and_throw(self, current_player: Any,
                                 card_index: int) -> None:
        """
        Take the top card from the deck and throw a specific card instead
        :param current_player: The player doing the action
        :param card_index: The card to throw from the hand
        """
        card_to_throw = current_player.hand.card_in(card_index)
        self.__garbage.append(card_to_throw)
        current_player.hand.replace_card(card_index, self.__deck.pop_card())

    def handle_game_won(self, current_player: Player) -> str:
        """
        Check who won and return the score to the player
        :param current_player: The player that asked the score
        :return: Str code with the score
        """
        winner, hand_value = self.check_who_won()
        if current_player == winner:
            return "End of Game|You win!"
        else:
            return "End of Game|You lose!"

    def check_who_won(self) -> Tuple[Player, int]:
        """
        Checks which player has won the game
        :return: Tuple with the player who won and his score (Winner, score)
        """
        max_player, max_score = None, None
        for player in self.__players.values():
            cur_hand_value = player.hand.hand_value()
            if max_player is None or cur_hand_value < max_score:
                max_player, max_score = player, cur_hand_value

        return max_player, max_score

    def player_name_to_index(self, player_name: Any) -> int:
        """
        :return: The index of the player
        """
        for index, name in enumerate(self.__players.keys()):
            if name == player_name:
                return index

    def player_index_to_name(self, index: int) -> Any:
        """
        Receive a player's index and return his name
        :param index: player's index
        :return: s
        """
        for cur_index, player in enumerate(self.__players.keys()):
            if cur_index == index:
                return player

    def throw_card(self, card: Card) -> None:
        """
        Throw a card to the garbage
        """
        self.__garbage.append(card)

    def next_turn(self) -> None:
        """
        Continue to the next turn
        """
        self.__turn += 1
        if self.__turn >= MAX_PLAYERS:
            self.__turn = 0

        cur_player_name = self.player_index_to_name(self.__turn)
        if self.__players[cur_player_name].asked_to_finish:
            self.__game_won = True

    def get_enemy(self, current_player: Player) -> Player:
        """
        Return the player object of the enemy if the player given
        :param player_name: The player to get his enemy
        """
        for player in self.__players.values():
            if player != current_player:
                return player

    def get_game_status(self, current_player: Player) -> Game_status_type:
        """
        Return a GameStatus object that is consist of:
        player's hand, enemy_num_cards, garbage_card, deck_card
        :param current_player: The player to send it's game status
        """
        game_status: Game_status_type = {}

        game_status["hand"] = current_player.hand
        game_status["enemy_num_cards"] = len(
            self.get_enemy(current_player).hand)
        game_status["garbage_card"] = self.garbage_top_card()
        game_status["asked_to_finish"] = current_player.asked_to_finish
        game_status["is_turn"] = self.__turn == self.player_name_to_index(
            current_player.name)

        if current_player.can_see_deck_card:
            game_status["deck_card"] = self.__deck.peek_top()
        else:
            game_status["deck_card"] = None
        return game_status

    @property
    def game_id(self) -> int:
        return self.__game_id

    @property
    def players(self) -> Dict[Any, Player]:
        return self.__players.copy()

    def get_turn(self) -> int:
        return self.__turn

    def has_started(self) -> bool:
        return self.__has_started

    def garbage_top_card(self) -> Card:
        return self.__garbage[-1]

    def is_full(self) -> bool:
        return len(self.__players) == MAX_PLAYERS

    def players_num(self) -> int:
        return len(self.__players)

    def name_to_index(self, name):
        return self.player_name_to_index(name)


if __name__ == '__main__':
    game = Game(1234)
    game.add_player("Nir")
    game.add_player("Hadar")
    game.start()

