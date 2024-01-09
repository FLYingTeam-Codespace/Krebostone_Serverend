import datetime
import colorama

class Logger:
    
    def __init__(self, departmentName, writeToLoggerFile=False) -> None:
        self.departmentName = departmentName
        self.writeToLoggerFile = writeToLoggerFile
        self.info = "INFO",
        self.warning = "WARNING",
        self.error = "ERROR",
        self.debug = "DEBUG",
        
    def __printOut(self, message, level, color=colorama.Fore.WHITE):
        print(f"{color}[{datetime.datetime.today()}][{level}][{self.departmentName}] : {message}")
        
    def printinfo(self, message, color=colorama.Fore.WHITE):
        self.__printOut(message, self.info, color)
        
    def printwarning(self, message, color=colorama.Fore.YELLOW):
        self.__printOut(message, self.warning, color)
        
    def printerror(self, message, color=colorama.Fore.RED):
        self.__printOut(message, self.error, color)
