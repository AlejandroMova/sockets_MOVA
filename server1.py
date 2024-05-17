# echo-server.py
import string
import socket
import secrets
from dotenv import load_dotenv
import os
from github import Github
from github import Auth
import subprocess

load_dotenv()

# variables de env
access_token = os.getenv('TOKEN')
key = os.getenv('KEY')
repository = os.getenv('REPO')

def generate_key(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = int(os.getenv("PORTS").split(',')[0])  # Port to listen on (non-privileged ports are > 1023)

# para generar nueva key
# key = generate_key()
# print('Key generada: ', key)

# to continue receiving, even if a connection is closed
while True: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            # print la conexión
            print(f"Conectado por {addr}")
            while True:
                data = conn.recv(1024)
                response = data

                # si ya no hay más información, cierra la conexión
                if not data:
                    print(f"Conexión con {addr} cerrada")
                    break

                data_list = data.decode().split(',')
                print('Recibido: ', data_list)
                # check if key was provided
                if data_list[1] == key: 

                    # check commits 
                    if data_list[0] == 'VERSION': 
                        
                        try: 
                            
                            result = subprocess.run(['git', 'log'], capture_output=True, text=True)
                            response = str(result.stdout).encode()
                        except Exception as e: 
                            response = str(e).encode()
                            print(e)
                            
                    # pull the repository
                    elif data_list[0] == 'PULL':
                        response = 'Haciendo pull'.encode()
                        try: 
                            # pull hacia el repositorio
                            result = subprocess.run(['git', 'pull', repository, 'main'], capture_output=True, text=True)
                            response = str(result.stdout).encode()
                            
                        except Exception as e:
                            print(e)
                            response = str(e).encode()

                # si la contraseña es incorrecta 
                else: 
                    response = 'Key incorrecta'.encode()
                conn.sendall(response)