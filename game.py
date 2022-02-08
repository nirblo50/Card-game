from hand import Hand
from player import Player
from deck import Deck
from card import Card

MAX_PLAYERS = 2
MIN_PLAYERS = 2
START_CARDS_NUM = 4


class Game:
    def __init__(self, game_id):
        self.__game_id: int = game_id
        self.__players: list[Player] = []
        self.__deck: Deck = Deck()
        self.__garbage: list[Card] = []
        self.__turn: int = 0
        self.__has_started = False
        self.__game_won = False

    def start(self):
        """
        Starts the game
        """
        self.__has_started = True
        self.__deck.initialize()
        self.__deck.shuffle()
        self.__garbage.append(self.__deck.pop_card())
        self.deal_cards()

    def deal_cards(self):
        """
        Deal each player the starting cards
        """
        for i in range(START_CARDS_NUM):
            for player in self.__players:
                card = self.__deck.pop_card()
                player.hand.add_card(card)

    def add_player(self, player_name):
        """
        Add a player to the game
        :param player_name: The name of the new player
        """
        player = Player(player_name, Hand())
        self.__players.append(player)

    def remove_player(self, player_name):
        """
        Remove a player from the game
        :param player_name: The player to remove
        """
        player_index = self.__player_name_to_index(player_name)
        self.__players.pop(player_index)

        if len(self.__players) < MIN_PLAYERS:
            self.__has_started = False
            self.empty_hands()

    def empty_hands(self):
        """
        Empty all the player's hands and game data
        """
        for player in self.__players:
            player.hand = Hand()
            player.can_see_deck_card = False
            player.score = 0

    def player_make_action(self, player_name, action: str):
        """
        Handles the actions from the player
        :param player_name: The name of the player that did the action
        :param action: The action itself
        :return: Card if needed or None
        """
        player_index = self.__player_name_to_index(player_name)
        current_player = self.__players[player_index]
        if self.__game_won:
            winner, hand_value = self.check_who_won()
            if current_player.name == winner:
                return "End of Game|You win!"
            else:
                return "End of Game|You lose!"

        # If This is not this player's turn
        if player_index is not self.__turn:
            return self.get_game_status(current_player)

        elif not self.has_started():
            return "Game did not start yet"

        elif action == "Try my luck":
            current_player.asked_to_finish = True

        elif action == "Show top card from deck":
            current_player.can_see_deck_card = True
            return self.get_game_status(current_player)

        elif action.startswith("Throw card from hand"):
            if current_player.can_see_deck_card:
                card_index = int(action[-1])
                self.take_from_deck_and_throw(current_player, card_index)

        elif action == ("Throw card from deck"):
            if current_player.can_see_deck_card:
                self.__garbage.append(self.__deck.pop_card())

        else:
            return self.get_game_status(current_player)

        current_player.can_see_deck_card = False
        self.next_turn()
        return self.get_game_status(current_player)

    def take_from_deck_and_throw(self, current_player, card_index):
        """
        Take the top card from the deck and throw a specific card instead
        :param player_index: The player doing the action
        :param card_index: The card to throw from the hand
        """
        card_to_throw = current_player.hand.card_in(card_index)
        self.__garbage.append(card_to_throw)
        current_player.hand.replace_card(card_index, self.__deck.pop_card())

    def __player_name_to_index(self, player_name):
        """
        :return: The index of the player
        """
        for index in range(len(self.__players)):
            if self.__players[index].name == player_name:
                return index

    def throw_card(self, card: Card):
        """
        Throw a card to the garbage
        """
        self.__garbage.append(card)

    def next_turn(self):
        """
        Continue to the next turn
        """
        self.__turn += 1
        if self.__turn >= MAX_PLAYERS:
            self.__turn = 0
        if self.__players[self.__turn].asked_to_finish:
            self.__game_won = True

    def check_who_won(self):
        winner = self.__players[0].name
        max_hand = self.__players[0].hand.hand_value()
        for player in self.__players:
            current_hand_sum = player.hand.hand_value()
            if current_hand_sum <= max_hand:
                winner, max_hand = player.name, current_hand_sum
        return winner, max_hand

    def get_game_status(self, current_player):
        """
        Return a GameStatus object that is consist of:
        player's hand, enemy_num_cards, garbage_card, deck_card
        :param player_name: The player to send it's game status
        """
        player_hand = current_player.hand
        enemy_num_cards = START_CARDS_NUM
        garbage_card = self.garbage_top_card()
        asked_to_finish = current_player.asked_to_finish
        is_turn = self.__turn == self.__player_name_to_index(current_player.name)

        if current_player.can_see_deck_card == True:
            deck_card = self.__deck.peek_top()
        else:
            deck_card = None
        return GameStatus(is_turn, player_hand, enemy_num_cards, asked_to_finish, garbage_card, deck_card)

    @property
    def game_id(self):
        return self.__game_id

    @property
    def players(self):
        return self.__players[:]

    def get_turn(self):
        return self.__turn

    def has_started(self):
        return self.__has_started

    def garbage_top_card(self):
        return self.__garbage[-1]

    def is_full(self):
        return len(self.__players) == MAX_PLAYERS

    def players_num(self):
        return len(self.__players)


class GameStatus:
    def __init__(self, is_turn, hand, enemy_num_cards,asked_to_finish, garbage_card=None, deck_card=None):
        self.hand = hand
        self.enemy_num_cards = enemy_num_cards
        self.garbage_card = garbage_card
        self.deck_card = deck_card
        self.asked_to_finish = asked_to_finish
        self.is_turn = is_turn

if __name__ == '__main__':
    game = Game(1234)
    game.add_player("Nir")
    game.add_player("Hadar")
    game.start()

    print(game.get_game_status("Nir").hand)
    print(game.get_game_status("Hadar").hand)
    print(game.garbage_top_card())

    game.player_make_action("Nir", "Show top card from deck")
    game.player_make_action("Nir", "Throw card from hand|0")

    print(game.get_game_status("Nir").hand)
    print(game.get_game_status("Hadar").hand)
    print(game.garbage_top_card())

