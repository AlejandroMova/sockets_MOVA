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
    if not cmd: return "Call not found"
    if not os.path.exists(cmd): return "Script not found"
    return True

class CustomError(Exception): 
    # para crear errores con texto customizado
    def __init__(self, message): 

        self.message = message
        super().__init__(self.message)