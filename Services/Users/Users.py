
import os

def preloadCheck():
    if os.path.exists(os.path.join(os.getcwd(), "Data", "users.json")):
        return True
    else:
        return False
    pass