
import os
import logger
import json
import uuid
import datetime

__log = logger.Logger("Bulletin", True)

def preloadCheck():
    if os.path.exists(os.path.join("Data", "bulletin.json")):
        __log.printinfo("Bulletin file found, loading...")
        return True
    else:
        __log.printerror("Bulletin file not found, services related to this module will be disabled.")
        return False
    
def getBulletin():
    try:
        with open(os.path.join("Data", "bulletin.json"), "r") as f:
            bulletin = json.load(f)
            return (True, bulletin)
    except:
        return (False, None)
    
def appendBulletin(title, content, userID):
    try:
        with open(os.path.join("Data", "bulletin.json"), "r") as f:
            bulletin = json.load(f)
            targetID = str(uuid.uuid4())
            bulletin.append({
                "id": targetID,
                "date": str(datetime.datetime.now()),
                "user": userID,
                "title": title,
                "content": content
            })
            with open(os.path.join("Data", "bulletin.json"), "w") as f:
                json.dump(bulletin, f)
            return (True, targetID)
    except:
        return (False, None)
    
def removeBulletin(targetID):
    try:
        with open(os.path.join("Data", "bulletin.json"), "r") as f:
            bulletin = json.load(f)
            for i in range(len(bulletin)):
                if bulletin[i]["id"] == targetID:
                    bulletin.pop(i)
                    break
            with open(os.path.join("Data", "bulletin.json"), "w") as f:
                json.dump(bulletin, f)
            return True
    except:
        return False