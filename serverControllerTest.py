
import os
import logger
import Services.GameServer.GameServer as GameServer
import threading

__log = logger.Logger("Test", True)

def keppAndPrintServer():
    output = GameServer.minecraftServerProcess.stdout.readline()
    while output:
        __log.printinfo(output.strip())
        output = GameServer.minecraftServerProcess.stdout.readline()

if __name__ == "__main__":
    __log.printinfo("Starting test program...")
    GameServer.preloadCheck()
    GameServer.startMinecraftServer()
    
    # Create a thread to keep the server alive
    t = threading.Thread(target=keppAndPrintServer)
    t.start()
    
    while True:
        command = input()
        GameServer.minecraftServerProcess.stdin.write(f"{command}\n".encode())
        GameServer.minecraftServerProcess.stdin.flush()


        
        