import socket

def send_connect_message():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.5'  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "CONNECT"
    client_socket.send(message.encode('utf-8'))

    client_socket.close()

def send_upload_message(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.5'  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "FILE:"+filename
    client_socket.send(message.encode('utf-8'))

    client_socket.close()

def send_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.5'  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()

if __name__ == "__main__":
    # Choose one of the following options based on your needs:

    # Option 1: Connect to the server
    # send_connect_message()

    # Option 2: Send a file
    send_upload_message("teste.txt")
    send_file("teste.txt")
