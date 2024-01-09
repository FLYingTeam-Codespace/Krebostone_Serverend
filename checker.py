
# This fill will check everything that need for all the services.
# If check failed then the server will not be able to start.

import os
import logger
import importlib

__log = logger.Logger("checker", True)

def checkServicesRequirements():
    services = os.listdir(os.path.join(os.getcwd(), "Services"))
    __log.printinfo(f"Found {len(services)} services, checking requirements...")
    for i in services:
        serviceModule = importlib.import_module(f"Services.{i}.{i}")
        if serviceModule.preloadCheck() == False:
            __log.printerror(f"Service <{i}> failed to pass preload check, server will not be able to start.")
            return False
        else:
            __log.printinfo(f"Service <{i}> passed preload check.")
            continue
    __log.printinfo("All services passed preload check.")
    return True