import os
import logger
import config

# Everything in this file will execute before the main program starts, mainly for checking whether met all of the requirements.
__log = logger.Logger("preload", True)
__config = config.Config()

preloadCheckPoints = {
    "minecraft_server_exists": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "server.jar")),
    "minecraft_start_script_exists": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "start.bat")),
    "minecraft_saves_folder_exists": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "world")),
    "minecraft_mods_exists": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "mods")),
    "minecraft_mods_config_folder_exists": (False, os.path.join(__config.getConfigFileContent("minecraft_server_location"), "config")),
}

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
            __log.printwarning(f"Cannot find {preloadCheckPoints[i][1]}, services related to this module will be disabled.")
            preloadCheckPoints[i] = (False, preloadCheckPoints[i][1])
    
    __log.printinfo(f"Preload check completed, {successCounter}/{len(locationList)} modules are enabled. Continuing to main program...")
            
    pass