# echo-client.py
from dotenv import load_dotenv
import socket
import os
import sys
import selectors
import types

sel = selectors.DefaultSelector()

load_dotenv()

HOST = "127.0.0.1"  # The server's hostname or IP address
PORTS = os.getenv("PORTS").split(',')  # The port used by the server

key = os.getenv('KEY')
#key = input("Enter key: ")

option = ''
while True: 
    option = input("Version or pull: ").upper()

    if option == 'VERSION' or option == 'PULL': 
        break
    else: 
        print('Por favor introduce version o pull')

message = option.encode() + b',' + key.encode()
for PORT in PORTS: 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, int(PORT)))
        s.sendall(message)
        data = s.recv(1024)

    print(f"Recibido de servidor {PORT}: {data!r}")