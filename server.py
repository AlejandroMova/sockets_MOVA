# echo-server.py
import socket
from dotenv import load_dotenv
import os
import subprocess
from hash import hashIt
from hash import verifyHash

load_dotenv()

# variables de env
KEY = os.getenv('KEY')
HOST = os.getenv('SERVERS').split(',')[0] # Standard loopback interface address (localhost)
PORT = int(os.getenv("PORT"))  # Port to listen on (non-privileged ports are > 1023)
REPOSITORY = os.getenv('REPOSITORY')

# to continue receiving, even if a connection is closed
while True: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        HOST = HOST.strip('"')
        print(HOST)
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


                # get date from data_list
                date = eval(data_list[0] + "}")
                date = date['date']
                # get key from data_list 
                key = eval("{" + data_list[2])
                key = key['token']
                # get message from data_list
                msg = eval("{" + data_list[1] + "}")
                msg = msg['message']
                message = msg.upper()
                

                # check if key was provided
           
                if verifyHash(date, msg, os.getenv('KEY'), key):

                    # check commits 
                    if message == 'VERSION': 
                        print('Revisando version')
                        
                        try: 
               
                            result = subprocess.run(['git','log'], capture_output=True, text=True)
                            response = str(result.stdout).encode()
                        except Exception as e: 
                            response = str(e).encode()
                            print(e)
                            
                    # pull the repository
                    elif message == 'PULL':
                        response = 'Haciendo pull'.encode()
                        print('Haciendo pull')
                        try: 
                            # pull hacia el repositorio
                       
                            result = subprocess.run(['git', 'pull', REPOSITORY, 'main'], capture_output=True, text=True)
                            response = str(result.stdout).encode()
                            
                        except Exception as e:
                            print(e)
                            response = str(e).encode()

                # si la contraseña es incorrecta 
                else: 
                    response = 'Key incorrecta'.encode()
                conn.sendall(response)