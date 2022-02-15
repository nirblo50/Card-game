import socket, pickle
from game import Game_status_type

#SERVER_IP = 'localhost'
SERVER_IP = "139.162.181.110"
PORT = 5555
MAX_MSG_LENGTH = 1024


class Client:
    """
    This class is a client that can connect to a server and communicate with it
    """
    def __init__(self) -> None:
        self.__my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """
        Makes a connection with the server
        """
        self.__my_socket.connect((SERVER_IP, PORT))

    def send(self, data: str) -> None:
        """
        Sends data to the server
        """
        self.__my_socket.send(data.encode())

    def receive_data(self) -> Game_status_type:
        """
        Receives data from the server
        """
        rec_data = pickle.loads(self.__my_socket.recv(MAX_MSG_LENGTH))
        return rec_data

    def close(self) -> None:
        """
        Disconnects from the server
        """
        self.__my_socket.close()


if __name__ == '__main__':
    my_client = Client()
    my_client.connect()
    while True:
        my_data = input("enter: ")
        my_client.send(my_data)
        rec = my_client.receive_data()
        print(rec.hand)
