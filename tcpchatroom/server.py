# This is a simple chat server.
# It allows multiple clients to connect and send messages to each other.
# The server broadcasts each message to all connected clients.
# The server also keeps track of the nicknames of all connected clients.

import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# This function broadcasts a message to all connected clients.
def broadcast(message):
    for client in clients:
        client.send(message)

# This function handles each client connection.
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            break

# This function accepts new client connections.
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}") 

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f'{nickname} joined the chat !'.encode('ascii'))

        client.send('connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()

