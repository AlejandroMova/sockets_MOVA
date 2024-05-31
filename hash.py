import hashlib
import datetime

def hashIt(msg,token):
    "Returns signed dictionary"
    res = {}
    now = str(datetime.datetime.now())

    res['date'] = now
    res['message'] = msg
    todo = now + msg + token
    r = hashlib.sha256(todo.encode())
    res['token'] = r.hexdigest()
    return res

def verifyHash(date, message, token, key): 
    # key: the key sent by the user
    # token: the token extracted from env file
    todo = date + message + token 
    r = hashlib.sha256(todo.encode())
    computed_token = r.hexdigest()
    
    return computed_token == key