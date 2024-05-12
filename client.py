# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

key = input("Enter key: ")
option = input("Version or pull: ").encode()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    option = option + ','.encode()
    s.sendall(option.upper())
    s.sendall(key.encode())
    data = s.recv(1024)

print(f"Received {data!r}")