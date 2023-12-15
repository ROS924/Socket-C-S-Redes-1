import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 4444  # Choose a port number

    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    return server_socket
    
def send_connect_message():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.5'  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    # Send the connect message
    message = "CONNECT"
    client_socket.send(message.encode('utf-8'))

    client_socket.close()

def receive_file(client_socket, filename):
    
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

def handle_connection(client_socket):
    # Receive the message containing the operation and filename
    message = client_socket.recv(1024).decode('utf-8')
    print(message)
    filename = message.split(".")[0]
        
    client_socket, client_address = server_socket.accept()
    receive_file(client_socket, filename+"-server.txt")
    print(f"Received file: {filename}")

if __name__ == "__main__":
    server_socket = start_server()
    send_connect_message()
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_connection(client_socket)

