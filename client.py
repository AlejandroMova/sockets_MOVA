# echo-client.py
from dotenv import load_dotenv
import socket
import os

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

load_dotenv()

key = os.getenv('KEY')
#key = input("Enter key: ")

option = ''
while True: 
    option = input("Version or pull: ").upper()

    if option == 'VERSION' or option == 'PULL': 
        break
    else: 
        print('Por favor introduce version of pull')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    option = option + ','
    s.sendall(option.encode())
    s.sendall(key.encode())
    data = s.recv(1024)

print(f"Recibido {data!r}")