import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555


def setup_server():
    """
    Setting up the server and start listening for clients
    :return The server socket
    """
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    return server_socket


def send_all_massages(ready_to_write, messages_to_send):
    """
    Go over all the massages that needed to be sent to the clients
    :param ready_to_write: The list of clients to send massage
    :param messages_to_send: The massage itself
    """
    for message in messages_to_send:
        current_socket, data = message
        if current_socket in ready_to_write:
            current_socket.send(data.encode())
            messages_to_send.remove(message)


def disconnect_client(connected_clients, socket_to_remove, client_address):
    print(client_address, "Connection closed", )
    connected_clients.remove(socket_to_remove)
    socket_to_remove.close()


def main_loop():
    connected_clients = []  # List of all the clients connected to the Server
    messages_to_send = []  # List of all the messages to send to the clients
    server_socket = setup_server()

    while True:
        ready_to_read, ready_to_write, in_error = select.select(
            [server_socket] + connected_clients, connected_clients, [])

        # Going over all the clients that want to connect or already connected
        for current_socket in ready_to_read:
            if current_socket is server_socket:  # New client to connect
                client_socket, client_address = current_socket.accept()
                print("New client joined:", client_address)
                connected_clients.append(client_socket)

            else:  # Connected client sent new data
                try:  # If the client has been disconnected an error will pop
                    data = current_socket.recv(MAX_MSG_LENGTH).decode()

                    if data == "":  # Client wish to disconnect
                        disconnect_client(connected_clients, current_socket,
                                          client_address)

                    else:  # Client has sent data
                        print(client_address, ":", data)
                        send_message = "**" + str(data) + "**"
                        messages_to_send.append((current_socket, send_message))

                except WindowsError:  # Client probably suddenly disconnected
                    disconnect_client(connected_clients, current_socket,
                                      client_address)

        send_all_massages(ready_to_write,messages_to_send)

if __name__ == '__main__':
    main_loop()
