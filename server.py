import socket
import os
from utils import *


def send_connect_message(proxy_address):
    message = "CONNECT"
    send_message(message, proxy_address, port_p)



def send_broadcast_message():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print("Socket created")

    # Send the connect message to the broadcast address
    message = "FIND"

    client_socket.sendto(message.encode('utf-8'), (broadcast_address, port_b))
    print("FIND message sent")

    # Receive the response (assuming the server responds with its address)
    response, server_address = client_socket.recvfrom(1024)
    print("FIND response received")
    print(
        f"Received response from {server_address}: {response.decode('utf-8')}")

    client_socket.close()
    print("Socket closed\n")
    return server_address


def receive_file(client_socket, filename):

    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)


def send_file(filename, destination_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((destination_address, port_p))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()


def handle_connection(client_socket, destination_address):
    # Receive the message containing the operation and filename
    message = client_socket.recv(1024).decode('utf-8')

    if message.startswith("RECOVER:"):
        print("RECOVER message received")
        filename = message.split(":")[1]
        filename = filename.split(".")[0]

        send_file(filename+"-proxy-server.txt", destination_address)
        print(f"Recovering file: {filename}")
        print("\nRelaying file to proxy...")

    elif message.startswith("MODIFY:"):
        filename = message.split(":")[1]
        if os.path.exists(filename):
            # Delete the file
            os.remove(filename)
            print(f"The file '{filename}' has been deleted.")
        else:
            print(f"The file '{filename}' does not exist on this server.")

    else:
        filename = message.split(".")[0]

        client_socket, client_address = server_socket.accept()
        receive_file(client_socket, filename+"-server.txt")
        print(f"Received file: {filename}")


if __name__ == "__main__":
    server_socket = start_server(port_s)

    print("Sending FIND message")
    proxy_address = send_broadcast_message()
    print("FIND message sent. Now connecting...")
    send_connect_message(proxy_address[0])
    print("CONNECT message sent")
    while True:
        print("waiting message")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_connection(client_socket, proxy_address[0])
