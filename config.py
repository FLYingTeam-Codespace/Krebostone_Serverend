import json
import logger
import json
import logger
import os

class Config:
    def __init__(self):
        self.configFileLocation = "config.json"
        self.__configFileContent = {}
        with open(self.configFileLocation, 'r') as configFile:
            self.__configFileContent = json.load(configFile)
        self.log = logger.Logger("config", True)
        pass

    def getConfigFileContent(self, configKey):
        # self.log.printinfo(f"Giving config key {configKey}")
        return self.__configFileContent[configKey]
    
    def setConfigFileContent(self, configKey, configValue):
        if configKey in self.__configFileContent.keys():
            self.__configFileContent[configKey] = configValue
            with open(self.configFileLocation, 'w') as configFile:
                json.dump(self.__configFileContent, configFile)
            return True
        return False
