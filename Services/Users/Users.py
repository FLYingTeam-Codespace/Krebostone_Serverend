
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
            if (dbContent[username]["password"] == password or dbContent[username]["password"] == "default") and dbContent[username]["enabled"]:
                token = Token.generateToken(username, password, dbContent[username]["id"])
                returnValue = (True, token, False)
                if dbContent[username]["password"] == "default":
                    returnValue[2] = True
                return returnValue
            else:
                return (False, None)
        else:
            return (False, None)
        
def loginWithToken(token):
    if Token.verifyToken(token):
        return True
    else:
        return False
    pass

def changePassword(username, newPassword):
    with open(USER_DB_FILE, 'r') as db:
        dbContent = json.load(db)
        if username in dbContent.keys():
            dbContent[username]["password"] = newPassword
            with open(USER_DB_FILE, 'w') as db:
                json.dump(dbContent, db)
            # Generate new token
            token = Token.generateToken(username, newPassword)
            return (True, token)
        else:
            return (False, None)
        
def getUserInfo(username):
    with open(USER_DB_FILE, 'r') as db:
        dbContent = json.load(db)
        if username in dbContent.keys():
            del dbContent[username]["password"]
            return dbContent[username]
        else:
            return None
    pass

def changeNickname(username, newNickname):
    with open(USER_DB_FILE, 'r') as db:
        dbContent = json.load(db)
        if username in dbContent.keys():
            dbContent[username]["nickname"] = newNickname
            with open(USER_DB_FILE, 'w') as db:
                json.dump(dbContent, db)
            return True
        else:
            return False
    pass

def getUserInfoWithID(uuid):
    with open(USER_DB_FILE, 'r') as db:
        dbContent = json.load(db)
        for i in dbContent.keys():
            if dbContent[i]["id"] == uuid:
                del dbContent[i]["password"]
                return dbContent[i]
        return None
    pass