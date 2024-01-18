
import os
import config
import logger

__config = config.Config()
__logger = logger.Logger("KrebostoneServerInfo")

def preloadCheck():
    return True

SERVER_INTO = {
    "name": __config.getConfigFileContent("server")["name"],
    "description": __config.getConfigFileContent("server")["description"],
    "port": __config.getConfigFileContent("server")["port"],
    "address": __config.getConfigFileContent("server")["address"],
    "core": __config.getConfigFileContent("server")["core"],
}

def getServerInfo(key):
    return SERVER_INTO[key]

def getFullServerInfo():
    return SERVER_INTO