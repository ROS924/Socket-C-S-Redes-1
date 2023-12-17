import socket


# Declare global variables used accross modules

broadcast_address = '192.168.1.255'  #Broadcast address of your subnet

port_b = 6666 # Proxy UDP port number used for broadcast connections 
port_p = 5555 # Proxy TCP port number
port_s = 4444 # Server TCP port number
port_c = 3333 # Client TCP port number


def start_server(port:int):
    # This function starts the server. it listens on all interfaces on specified port.
    
    host = '0.0.0.0'  # Listen on all available interfaces

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5) #receives as parameter the number of possible queued connections

    print(f"Host listening on {host}:{port}")

    return server_socket


def send_message(message, address, port):
    # Send the connect message to server port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    client_socket.send(message.encode('utf-8')) 
    client_socket.close()
