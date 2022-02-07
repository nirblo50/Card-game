import socket

#SERVER_IP = socket.gethostbyname(socket.gethostname())
import time

SERVER_IP = 'localhost'
PORT = 5555

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((SERVER_IP, PORT))

while True:
    data = input("enter data: ")
    my_socket.send(data.encode())
    rec_data = my_socket.recv(1024).decode()
    print("server: ", rec_data)

my_socket.close()