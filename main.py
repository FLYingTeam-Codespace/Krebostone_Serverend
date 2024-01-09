
import logger
import preload
import config
import response as resp
import checker
import sys
from flask import Flask

__log = logger.Logger("main", True)
__config = config.Config()
app = Flask(__name__)

# Preload check===
preload.preloadCheck()
if checker.checkServicesRequirements() == False:
    __log.printerror("Failed to pass preload check, exiting...")
    sys.exit(1)
app = checker.autoRegisterRouters(app)
# ================

# Routers =====
@app.route("/getServerStatus")
def getServerStatus():
    return resp.sendResponse(resp.SUCCESS, "Server is running")
# =============

if __name__ == "__main__":
    __log.printinfo("Starting main program...")
    
    # run the app
    app.run(debug=False, port=__config.getConfigFileContent("port"))
    pass