import hashlib
import os
from datetime import datetime


PREFIJO='SH_'
TIMEOUT = os.getenv('TIMEOUT', 60)

def hashIt(msg,token):
    "Returns signed dictionary"
    res = {}
    now = str(datetime.now())

    res['date'] = now
    res['message'] = msg
    todo = now + msg + token
    r = hashlib.sha256(todo.encode())
    res['token'] = r.hexdigest()
    return res

def verifyHash(date, message, signed, key): 
    # key: the key sent by the user
    # token: the token extracted from env file
    todo = date + message + key 

    #TODO: verifica que el tiempo actual con el de la llamada mp sobrepase TIMEOUT
    signed_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()
    seconds = (now - signed_date).seconds
    
    if seconds > int(os.getenv('TIMEOUT')): 
        return False

    r = hashlib.sha256(todo.encode())
    computed_token = r.hexdigest()
    
    return computed_token == signed

def chkCall(call):
    cmd = os.getenv(f"{PREFIJO}{str(call).upper()}")
    if not cmd: raise CustomError("Call not found")
    if not os.path.exists(cmd): raise CustomError("Script not found")
    return cmd

def format_output(raw_string):
    # Decode bytes literal to string
    decoded_string = raw_string.decode('utf-8')

    # Replace escaped characters
    decoded_string = decoded_string.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')

    # Replace non-ASCII character
    decoded_string = decoded_string.replace('El número', 'El número')

    return decoded_string
            


class CustomError(Exception): 
    # para crear errores con texto customizado
    def __init__(self, message): 

        self.message = message
        super().__init__(self.message)


