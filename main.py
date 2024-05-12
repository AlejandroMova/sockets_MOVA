# echo-server.py
import string
import socket
import secrets

def generate_key(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

key = generate_key()
print('Key generada: ', key)
while True: 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            while True:
                data = conn.recv(1024)
                response = data

                if not data:
                    print(f"Conexión con {addr} cerrada")
                    break

                data_list = data.decode().split(',')
                print('Recibido: ', data_list)
                
                if data_list[1] == key: 
                
                    if data_list[0] == 'VERSION': 
                        response = 'Revisando version'.encode()
                    elif data_list[0] == 'PULL':
                        response = 'Haciendo pull'.encode()
                else: 
                    response = 'Key incorrecta'.encode()
                conn.sendall(response)