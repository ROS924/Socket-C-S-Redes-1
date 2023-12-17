import socket
import shutil

from utils import *


def send_broadcast_message():
    # Send the connect message to the broadcast address
    message = "CLIENT-FIND"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.sendto(message.encode('utf-8'), (broadcast_address, port_b))

    # Receive the response (assuming the server responds with its address)
    response, server_address = client_socket.recvfrom(1024)
    print(
        f"Received response from {server_address}: {response.decode('utf-8')}")

    client_socket.close()
    return server_address[0]


def send_status_message(destination_address):
    # Send the connect message
    message = "SERVER-STATUS"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((destination_address, port_p))
    client_socket.send(message.encode('utf-8'))
    client_socket, client_address = server_socket.accept()

    response = client_socket.recv(1024).decode('utf-8')

    client_socket.close()

    return response


def send_upload_message(filename, address, copies):
    # Send the connect message
    message = "FILE:"+filename+":"+copies
    send_message(message, address, port_p)


def send_recover_message(filename, address):
    message = "RECOVER:"+filename
    send_message(message, address, port_p)


def send_modify_message(filename, address, copies):
    message = "MODIFY:"+filename+":"+copies
    send_message(message, address, port_p)


def send_file(filename, destination_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((destination_address, port_p))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()


# receives socket. filename is so it can save a copy.
def recover_file(filename):
    client_socket, client_address = server_socket.accept()
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)  # reads the data in the file.
            if not data:
                break
            file.write(data)


def print_centered(text):
    terminal_width, _ = shutil.get_terminal_size()
    centered_text = text.center(terminal_width)
    print(centered_text)


if __name__ == "__main__":
    server_socket = start_server(port_c)  # starts client server
    proxy_address = send_broadcast_message()
    print("Successfully connected to proxy\n\n")

    print_centered(" *** Welcome to FileSync *** ")
    print_centered(" *** warning: this application is a prototype *** ")
    print("You can type commands on this application. If you're not sure what to do, type help.")
    while (True):
        user_input = input("FileSync>> ")

        if (user_input.startswith("help")):
            print("List of commands(use parameters without brackets):\n")
            print(
                "upload [filename with extension] [number of copies] --- uploads n copies of filename to random connected servers\n")
            print(
                "recover [filename with extension] --- recovers a copy of filename stored in a random connected server\n")
            print(
                "connected-servers --- displays the number and list of connected servers.\n")
            print(
                "modify [filename with extension] [number of copies] --- changes the number of copies in servers to given number\n")
            print("quit --- closes the application")
        elif (user_input.startswith("upload")):

            if (len(user_input.split()) < 2):
                print("missing parameter. If you're not sure what to do, type help.\n")
                continue

            filename = user_input.split()[1]
            copies = user_input.split()[2]

            if (isinstance(copies, int)):
                print("number of copies must be integer\n")
                continue

            max_copies = int(send_status_message(proxy_address).split()[2])

            if (int(copies) <= max_copies):
                send_upload_message(filename, proxy_address, copies)
                send_file(filename, proxy_address)
            else:
                print("Number of copies requested exceeds the number of servers.")
                print(
                    "You can check the number of connected servers by the 'connected-servers' command.")

        elif (user_input.startswith("recover")):
            if (len(user_input.split()) < 1):
                print("missing parameter. If you're not sure what to do, type help.\n")
                continue

            filename = user_input.split()[1]
            send_recover_message(filename, proxy_address)
            recover_file(filename.split(".")[0]+"-recovered.txt")

        elif (user_input.startswith("connected-servers")):
            status = send_status_message(proxy_address)
            print(status)

        elif (user_input.startswith("modify")):

            if (len(user_input.split()) < 2):
                print("missing parameter. If you're not sure what to do, type help.\n")
                continue

            filename = user_input.split()[1]
            copies = user_input.split()[2]

            if (isinstance(copies, int)):
                print("number of copies must be integer\n")
                continue

            max_copies = int(send_status_message(proxy_address).split()[2])

            send_modify_message(filename, proxy_address, copies)

            if (int(copies) <= max_copies):
                client_socket, client_address = server_socket.accept()
                response = client_socket.recv(1024).decode('utf-8')

                if (response.startswith("RESEND:")):
                    new_copies = response.split(":")[1]
                    send_file(filename, proxy_address)

            else:
                print("Number of copies requested exceeds the number of servers.")
                print(
                    "You can check the number of connected servers by the 'connected-servers' command.")

            client_socket.close()

            if (response.startswith("RESEND:")):
                copies = int(response.split(":")[1])

        elif (user_input.startswith("quit")):
            break
        else:
            print(f"{user_input} não é um comando reconhecido desta aplicação")
