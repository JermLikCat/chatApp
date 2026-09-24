import socket

serverSocket = socket.socket()

port = 6767

serverSocket.bind(('', port))
print(f"Socket binded to {port}!")

serverSocket.listen(2)
print("Socket is listening!")

message_list = []

while True:
    connection, addr = serverSocket.accept()
    print(f"Accepted connection from {addr}.")
    
