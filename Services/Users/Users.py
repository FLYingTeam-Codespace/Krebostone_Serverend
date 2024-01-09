
import os
import json
import Services.Token.Token as Token

USER_DB_FILE = os.path.join(os.getcwd(), "Data", "users.json")

def preloadCheck():
    if os.path.exists(os.path.join(os.getcwd(), "Data", "users.json")):
        return True
    else:
        return False
    pass

def login(username, password):
    with open(USER_DB_FILE, 'r') as db:
        dbContent = json.load(db)
        if username in dbContent.keys():
            if dbContent[username]["password"] == password and dbContent[username]["enabled"]:
                token = Token.generateToken(username, password)
                return (True, token)
            else:
                return (False)
        else:
            return (False)
        
def loginWithToken(token):
    if Token.verifyToken(token):
        return True
    else:
        return False
    pass