# echo-server.py
import string
import socket
import secrets
import os

def generate_key(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

key = generate_key()
print('Generated key: ', key)
while True: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)

                if not data:
                    print(f"Connection with {addr} closed")
                    break

                data_list = data.decode().split(',')
                print(data_list)
                if data_list[1] == key: 
                    if data_list[0].upper() == 'VERSION': 
                        print('Revisando version')
                    elif data_list[0].upper() == 'PULL':
                        print('Haciendo pull')
                
                conn.sendall(data)