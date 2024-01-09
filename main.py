
import logger
import preload
import config
import response as resp
from flask import Flask

__log = logger.Logger("main", True)
__config = config.Config()
app = Flask(__name__)

# Routers =====
@app.route("/getServerStatus")
def getServerStatus():
    return resp.sendResponse(resp.SUCCESS, "Server is running")

# =============
preload.preloadCheck()
if __name__ == "__main__":
    __log.printinfo("Starting main program...")
    
    # run the app
    app.run(debug=False, port=__config.getConfigFileContent("port"))
    pass