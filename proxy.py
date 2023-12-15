import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 5555  # Choose a port number

    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    return server_socket

def receive_file(client_socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

def handle_connection(client_socket, source_addresses):
    # Receive the message containing the operation and filename
    message = client_socket.recv(1024).decode('utf-8')

    if message.startswith("CONNECT"):
        source_address = client_socket.getpeername()[0]
        source_addresses.append(source_address)
        print(f"Connected clients: {source_addresses}")
    elif message.startswith("FILE:"):
        filename = message.split(":")[1]
        filename = filename.split(".")[0]
        
        client_socket, client_address = server_socket.accept()
        receive_file(client_socket, filename+"-proxy.txt")
        print(f"Received file: {filename}")

if __name__ == "__main__":
    server_socket = start_server()
    source_addresses = []

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_connection(client_socket, source_addresses)

