import json
import logger
import os

__log = logger.Logger("UserAccessProvider", True)

ACCESSES_KEYS = {
    "start": "start",
    "stop": "stop",
    "restart": "restart",
    "commands": "commands",
    "backup": "backup",
    "invite": "invite",
    "uploadMods": "uploadMods",
    "uploadFiles": "uploadFiles",
    "downloadMods": "downloadMods",
    "downloadFiles": "downloadFiles",
}

def preloadCheck():
    return True

def checkInKeys(key):
    if key in ACCESSES_KEYS.keys():
        return True
    else:
        return False
    
def generateAccesses(username):
    with open(os.path.join("Services", "users.json"), "r") as f:
        data = json.load(f)
        if username in data.keys():
            for i in ACCESSES_KEYS.keys():
                if i not in data[username]["access"].keys():
                    data[username]["access"][i] = False
        else:
            data[username] = {
                "access": {}
            }
            for i in ACCESSES_KEYS.keys():
                data[username]["access"][i] = False
    
def getAccess(username, key):
    if checkInKeys(key):
        with open(os.path.join("Services", "users.json"), "r") as f:
            data = json.load(f)
            if username in data.keys():
                if key in data[username]["access"].keys():
                    return data[username]["access"][key]
                else:
                    return False
            else:
                return False
    else:
        __log.printerror(f"An error occured while reading users accesses. Key {key} is not in the key list.")
        return False
    
def getFullAccess(username):
    returnValue = {}
    for i in ACCESSES_KEYS.keys():
        returnValue[i] = getAccess(username, i)
    return returnValue

def setAccess(username, key, value):
    if checkInKeys(key):
        with open(os.path.join("Services", "users.json"), "r") as f:
            data = json.load(f)
            if username in data.keys():
                data[username]["access"][key] = value
            else:
                data[username] = {
                    "access": {
                        key: value
                    }
                }
        with open(os.path.join("Services", "users.json"), "w") as f:
            json.dump(data, f, indent=4)
    else:
        __log.printerror(f"An error occured while reading users accesses. Key {key} is not in the key list.")
        return False