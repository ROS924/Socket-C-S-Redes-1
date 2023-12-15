# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:45:14 2023

@author: Saulo
"""
"""CLIENT -> PROXY -> SERVER  """
import socket
import json

def start_proxy(lista:list, port_client=4444, port_server=8888 ):
    proxy_socket_with_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    my_ip = '192.168.0.2' # mudar para os ips de verdade

    host = '0.0.0.0'  # Listen on all available interfaces
    client_ip = '192.168.0.1' # mudar para os ips de verdade

    # escutar conexão com cliente
    proxy_socket_with_client.bind((client_ip, port_client))
    proxy_socket_with_client.listen(1)
    print(f"Proxy listening on {client_ip}:{port_client}")

    # escutar conexão com servidores
    proxy_socket_with_server.bind((host, port_server))
    proxy_socket_with_server.listen(1) 
    print(f"Proxy listening on {host}:{port_server}")

    while True:
        try:
            # aceitar conexão com cliente
            client_socket, client_address = proxy_socket_with_client.accept()
            print(f"Connection from Server: {client_address}")

            # receber mensagem do cliente no formato string
            msg = client_socket.recv(2048).decode()
            print("Mensagem recebida do cliente: ", msg)

            # transformar mensagem do farmato string para json
            jason = json.loads(msg)
            
            # verifica qual o tipo de mensagem recebida e dá o tratamento adequado

            if jason["tipo"] == "recover": # comando para recuperar um arquivo de um servidor e enviá-lo de volta ao cliente

                recovered_file = recover_file(jason["conteudo"]) # string contendo o nome do arquivo a ser recuperado
                # recover_file pede o mesmo arquivo a um servidor que tenha este arquivo
                
                # enviar arquivo de volta ao cliente
                with open(recovered_file, 'rb') as file:
                    for data in file.readlienes():
                        client_socket.send(data)


            # lista.append(client_address[0]) usar com o servidor
            print(client_address)
            client_socket.close()
        except KeyboardInterrupt:
            break

    proxy_socket_with_client.close()
    #proxy_socket_with_servers.close()



def receive_file(client_socket:socket.socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            file.write(data)

def send_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '192.168.1.2'  # Replace with the actual server IP address
    server_port = 5555  # Use the same port number as in the server

    client_socket.connect((server_host, server_port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()

# Precisa ser adaptada para o proxy
""" def recover_file(filename:str):
    # iniciar conexão
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # preparar mensagem
    msg = "{\"tipo\":\"recover\",\"conteudo\":\"" + filename + "\"}"

    # conexão com o proxy
    client_socket.connect((proxy_ip, port))

    # enviar mensagem
    client_socket.send(msg.encode())

    # receber arquivo como resposta
    with open(filename, 'wb') as file:
        while 1:
            data = client_socket.recv(1000000)

            if not data:
                break

            file.write(data) """

if __name__ == "__main__":
    lista = []
    start_proxy(8888, 4444, lista)
