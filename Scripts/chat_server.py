import socket
import threading

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        msg = conn.recv(1024)
        if not msg:
            break
        print(f"{addr}: {msg.decode()}")
        reply = input("You (server): ")
        conn.sendall(reply.encode())
    conn.close()

# Set up server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen(1)

print("[SERVER STARTED] Waiting for connection...")
conn, addr = server.accept()
handle_client(conn, addr)
