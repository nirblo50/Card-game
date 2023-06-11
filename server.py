import pickle
import random
import select
import socket
from typing import List, Tuple, Dict
from game_stuff.game import Game

MAX_MSG_LENGTH = 1024
SERVER_IP = ""  # Connect to a local available ip

SERVER_PORT = 3000
DISCONNECT_MESSAGE = ""


class GameServer:
    def __init__(self):
        self.connected_clients: List[socket.socket] = []
        self.clients_to_respond: List[Tuple[socket.socket, str]] = []
        self.games: Dict[int, Game] = {}
        self.client_to_games: Dict[socket.socket, int] = {}

    def setup_server(self) -> socket.socket:
        """
        Setting up the server and start listening for clients
        :return The server socket
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cur_server = socket.gethostbyname(socket.gethostname())
        print(f"Setting up server on {cur_server}...")
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen()
        print("Listening for clients...")
        return server_socket

    def disconnect_client(self, socket_to_remove: socket.socket, client_address: Tuple[str, str]) -> None:
        """
        Disconnect a client from the server
        :param socket_to_remove: The client to remove
        :param client_address: The client's address
        """
        print(client_address, "Connection closed", )
        self.connected_clients.remove(socket_to_remove)
        client_game_id = self.client_to_games[socket_to_remove]
        self.games[client_game_id].remove_player(socket_to_remove)
        self.client_to_games.pop(socket_to_remove)
        socket_to_remove.close()
        self.close_empty_game(client_game_id)

    def close_empty_game(self, game_id: int) -> None:
        """
        Close a game if there are no players in it
        :param game_id: the id of the game
        """
        if self.games[game_id].players_num() == 0:
            self.games.pop(game_id)
            print(f"~ Game {game_id} has been closed ~")

    def randomize_game_id(self) -> int:
        """
        :return: New original game id
        """
        game_id = random.randint(1000, 9999)
        while game_id in self.games.keys():
            game_id = random.randint(1000, 9999)
        return game_id

    def handle_new_client(self, client_socket: socket.socket, client_address: Tuple[str, str]) -> None:
        """
        Things to do when a new client is connected to the server:
        add it to an existing / new game
        :param client_socket: The new client socket
        :param client_address: The new client address
        """
        self.connected_clients.append(client_socket)
        for game_id, game in self.games.items():
            if not game.is_full():
                self.client_to_games[client_socket] = game_id
                game.add_player(client_socket)
                print("New client joined:", client_address, "game_id:", game_id)
                self.games[game_id].start()
                return

        # No game is available for connecting - Create a new one and add player
        game_id = self.randomize_game_id()
        self.client_to_games[client_socket] = game_id
        self.games[game_id] = Game(game_id)
        self.games[game_id].add_player(client_socket)
        print("New client joined:", client_address, "game_id:", game_id)

    def handle_client_rec_data(self, current_socket: socket.socket, client_address: Tuple[str, str]) -> None:
        """
        Handles receiving data from a client
        :param current_socket: The socket who sent the data
        :param client_address: The socket address who sent the data
        :return: None
        """
        try:  # If the client has been disconnected an error will pop
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == DISCONNECT_MESSAGE:  # Client wish to disconnect
                self.disconnect_client(current_socket, client_address)
            else:  # Client has sent data
                self.clients_to_respond.append((current_socket, data))
        except:  # Client probably suddenly disconnected
            self.disconnect_client(current_socket, client_address)

    def handle_player_action(self, player_socket: socket.socket, received_data: str) -> None:
        """
        Receive data/action from client and pass it to the game object
        :param player_socket: The player that sent the data
        :param received_data: The data that was sent
        """
        game_id = self.client_to_games[player_socket]
        status = self.games[game_id].player_make_action(player_socket, received_data)
        player_socket.send(pickle.dumps(status))

    def send_all_messages(self, ready_to_write: List[socket.socket]) -> None:
        """
        Go over all the messages that needed to be sent to the clients
        :param ready_to_write: The list of clients to send message
        """
        for client, msg in self.clients_to_respond:
            if client in ready_to_write:
                self.handle_player_action(client, msg)
                self.clients_to_respond.remove((client, msg))

    def main_loop(self) -> None:
        server_socket = self.setup_server()

        while True:
            ready_to_read, ready_to_write, in_error = select.select(
                [server_socket] + self.connected_clients, self.connected_clients, [])

            # Going over all the clients that want to connect or already connected
            for current_socket in ready_to_read:
                if current_socket is server_socket:  # New client to connect
                    client_socket, client_address = current_socket.accept()
                    self.handle_new_client(client_socket, client_address)
                else:  # Connected client sent new data
                    self.handle_client_rec_data(current_socket, client_address)
            self.send_all_messages(ready_to_write)


if __name__ == '__main__':
    game_server = GameServer()
    game_server.main_loop()
