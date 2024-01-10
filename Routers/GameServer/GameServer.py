from flask import Blueprint, request
import Services.GameServer.GameServer as GameServer
import response as resp
import logger
from Middlewares.AuthService import tokenBlocker

router = Blueprint('gameServer', __name__, url_prefix='/gameServer')

@router.route('/getServerStageInfo', methods=['POST'])
def getServerStageInfo():
    tokenBlocker()
    return resp.sendResponse(resp.SUCCESS, data={"stage": GameServer.getServerStatus()})

@router.route('/startServer', methods=['POST'])
def startServer():
    tokenBlocker()
    if GameServer.startMinecraftServer():
        return resp.sendResponse(resp.SUCCESS, "Server started")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Server is already running or not installed")

@router.route('/stopServer', methods=['POST'])
def stopServer():
    tokenBlocker()
    if GameServer.stopMinecraftServer():
        return resp.sendResponse(resp.SUCCESS, "Server stopped")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Server is already stopped")

@router.route('/issueCommand', methods=['POST'])
def issueCommand():
    tokenBlocker()
    cmd = request.get_json().get('command')
    if cmd == None:
        return resp.sendResponse(resp.FORBIDDEN, "No command provided")
    if GameServer.issueCommand(cmd):
        return resp.sendResponse(resp.SUCCESS, "Command issued")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Sending command failed.")
    pass