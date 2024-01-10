
import os
import logger
import config
import subprocess
import threading
import colorama
import json

__log = logger.Logger("MCServer|CORE", True)
__config = config.Config()
minecraftServerProcess:subprocess.Popen = None
minecraftServerThread:threading.Thread = None
serverIsRunning = False
serverIsBooting = False

preloadCheckPoints = {
    "minecraft_server": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "server.jar")),
    "minecraft_saves_folder": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "world")),
    "minecraft_mods_folder": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "mods")),
    "minecraft_mods_config_folder": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "config")),
}

def getServerStatus():
    global serverIsRunning
    global serverIsBooting
    if serverIsBooting == True:
        return "booting"
    elif serverIsRunning == True:
        return "running"
    else:
        return "stopped"

def preloadCheck():
    __log.printinfo("Checking minecraft server and its libraries...")
    locationList = preloadCheckPoints.keys()
    successCounter = 0
    # Iterate to enable
    for i in locationList:
        # Check is folder or file
        if os.path.isfile(preloadCheckPoints[i][1]) and os.path.exists(preloadCheckPoints[i][1]):
            preloadCheckPoints[i] = (True, preloadCheckPoints[i][1])
            successCounter += 1
        elif os.path.isdir(preloadCheckPoints[i][1]) and os.path.exists(preloadCheckPoints[i][1]):
            preloadCheckPoints[i] = (True, preloadCheckPoints[i][1])
            successCounter += 1
        else:
            __log.printerror(f"Cannot find {preloadCheckPoints[i][1]}, services related to this module will be disabled.")
            preloadCheckPoints[i] = (False, preloadCheckPoints[i][1])
            # return False

    __log.printinfo(f"Preload check completed, {successCounter}/{len(locationList)} modules are enabled. Continuing to main program...")
    return True
    pass

def keepAlive():
    global minecraftServerProcess
    global serverIsRunning
    global serverIsBooting
    output = minecraftServerProcess.stdout.readline()
    while output:
        if output.strip().find('For help, type "help"'.encode()) != -1:
            # End the mark of server booting
            serverIsBooting = False
        __log.printinfo(output.strip(), color=colorama.Fore.CYAN)
        output = minecraftServerProcess.stdout.readline()
    serverIsRunning = False

def startMinecraftServer():
    global minecraftServerProcess
    global serverIsRunning
    global minecraftServerThread
    global serverIsBooting
    if serverIsRunning == True:
        __log.printerror("Minecraft server is already running.")
        return False
    if preloadCheckPoints["minecraft_server"][0] == False:
        __log.printerror("Minecraft server is not installed, cannot start.")
        return False
    
    try:
        __log.printinfo("Starting minecraft server...")
        minecraftServerProcess = subprocess.Popen(["java", "-Xms"+__config.getConfigFileContent("server")["minMem"], "-Xmx"+__config.getConfigFileContent("server")["minMem"], "-jar", preloadCheckPoints["minecraft_server"][1], "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=__config.getConfigFileContent("minecraft_server_location"))
        minecraftServerThread = threading.Thread(target=keepAlive) # Keep the server running in the background
        minecraftServerThread.start() # Start the thread
        serverIsRunning = True
        serverIsBooting = True
        return True
    except Exception as e:
        __log.printerror(f"Failed to start minecraft server, error: {e}")
        serverIsRunning = False
        return False
    
def stopMinecraftServer():
    global minecraftServerProcess
    global serverIsRunning
    __log.printinfo("Stopping minecraft server...")
    minecraftServerProcess.stdin.write("stop\n".encode())
    minecraftServerProcess.stdin.flush()
    serverIsRunning = False
    
def issueCommand(command):
    global minecraftServerProcess
    global serverIsRunning
    global serverIsBooting
    if serverIsRunning == False or serverIsBooting == True:
        __log.printerror("Minecraft server is not running.")
        return False
    __log.printinfo(f"Issuing command: {command}")
    minecraftServerProcess.stdin.write(f"{command}\n".encode())
    minecraftServerProcess.stdin.flush()
    return True

# Whitelist checker
def checkWhitelist(username):
    # Read the whitelist.json file
    with open(os.path.join(__config.getConfigFileContent("minecraft_server_location"), "whitelist.json"), "r") as f:
        whitelist = json.load(f)
        for i in whitelist:
            if i["name"] == username:
                return True
    return False
    pass

def addWhitelist(username):
    return issueCommand(f"whitelist add {username}")
    pass

def removeWhitelist(username):
    return issueCommand(f"whitelist remove {username}")
    pass