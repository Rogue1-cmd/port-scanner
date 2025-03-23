import socket 
import threading

nickname = input ("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# This function receives messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break
# This function sends messages to the server
#continuously prompts the user to input a message, prefixes it with their nickname, and sends it to the server via a socket connection
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread()
write_thread.start()
