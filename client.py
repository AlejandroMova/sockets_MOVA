# echo-client.py
from dotenv import load_dotenv
import socket
import os, click, json
from hash import hashIt, chkCall

load_dotenv()

HOST = os.getenv('SERVERS').split(',')  # The server's hostname or IP address
PORT = int(os.getenv("PORT"))  # The port used by the server
TOKEN = os.getenv('KEY')

@click.command()
@click.option('--host', default='all', help='set hoat to connect at ')
@click.option('--port', default=0, help='port of connection')
@click.option('--call', default='', help='command to execute')
def main(host, port, call):
    
    if host == 'all': 
        host = HOST
    else: 
        host = [host]
 
    if not port: port=PORT
    cmd = chkCall(str(call).upper())
    if not cmd==True: click.echo(click.style(cmd, fg='red', bold=True))

    print(host)
    for h in host: 
        h = h.strip('"')
        print(h)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try: 
                s.connect((h, int(port)))
                msg = hashIt(token=TOKEN, msg=call)
                message = json.dumps(msg)
                s.sendall(message.encode())
                data = s.recv(1024)
                print(f"Recibido de servidor {PORT}: {data!r}")
            except:
                print(f'HOST: "{h}" did not connect')


if __name__ == '__main__':
    main()
