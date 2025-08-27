import socket
import threading

def receive_messages(sock):
    while True:
        msg = sock.recv(1024)
        if not msg:
            break
        print("Server:", msg.decode())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

while True:
    msg = input("You (client): ")
    client.sendall(msg.encode())
