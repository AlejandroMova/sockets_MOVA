# echo-server.py
import socket
from dotenv import load_dotenv
import os
import subprocess
from hash import hashIt
from hash import verifyHash, chkCall, CustomError
import json

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

                data_list = data.decode()
                print('Recibido: ', data_list)
                
                data = json.loads(data_list)
                
                date = data['date']
                msg = data['message']
                signed = data['token']

                # check if key was provided
           
                if verifyHash(date, msg, signed, os.getenv('KEY')):
                    try:          
                        # Verificamos existencia de comando
                        cmd = chkCall(str(msg).upper())
                        if not cmd==True: raise CustomError(cmd)
                        result = subprocess.run([os.getenv(msg)], capture_output=True, text=True)
                        response = str(result.stdout).encode()
                            
                    except Exception as e:
                        print(e)
                        response = str(e).encode()

                # si la contraseña es incorrecta 
                else: 
                    response = 'Key incorrecta'.encode()
                conn.sendall(response)

