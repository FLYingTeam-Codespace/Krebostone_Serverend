
import jwt
import datetime

SECRET = "mysteriousSecret;)"

def preloadCheck():
    return True

def generateToken(username, password, uuid):
    payload = {
        "username": username,
        "password": password,
        "id": uuid,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token

def verifyToken(token):
    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
        return True
    except:
        return False
    
def parseToken(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None
    pass