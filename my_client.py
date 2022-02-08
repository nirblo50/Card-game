import socket
import pickle

SERVER_IP = 'localhost'
PORT = 5555
MAX_MSG_LENGTH = 2048


class Client:
    def __init__(self):
        self.__my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.__my_socket.connect((SERVER_IP, PORT))

    def send(self, data):
        self.__my_socket.send(data.encode())

    def receive_data(self):
        rec_data = pickle.loads(self.__my_socket.recv(MAX_MSG_LENGTH))
        return rec_data

    def close(self):
        self.__my_socket.close()


if __name__ == '__main__':
    my_client = Client()
    my_client.connect()
    while True:
        my_data = input("enter: ")
        my_client.send(my_data)
        rec = my_client.receive_data()
        print(rec.hand)
