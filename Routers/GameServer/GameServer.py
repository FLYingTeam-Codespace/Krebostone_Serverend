from flask import Blueprint, request
import Services.GameServer.GameServer as GameServer
import Services.Users.Users as Users
import response as resp
import logger
import Services.Token.Token as Token
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

@router.route('/checkWhitelist', methods=['POST'])
def checkWhitelist():
    tokenBlocker()
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    username = Users.getUserInfo(data["username"])["nickname"]
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    if GameServer.checkWhitelist(username):
        return resp.sendResponse(resp.SUCCESS, "User is whitelisted", data=True)
    else:
        return resp.sendResponse(resp.FORBIDDEN, "User is not whitelisted", data=False)
    
    
@router.route('/addWhitelist', methods=['POST'])
def addWhitelist():
    tokenBlocker()
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    username = Users.getUserInfo(data["username"])["nickname"]
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    if GameServer.addWhitelist(username):
        return resp.sendResponse(resp.SUCCESS, "User added to whitelist")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Failed to add user to whitelist")
    pass

@router.route('/removeWhitelist', methods=['POST'])
def removeWhitelist():
    tokenBlocker()
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    username = Users.getUserInfo(data["username"])["nickname"]
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    if GameServer.removeWhitelist(username):
        return resp.sendResponse(resp.SUCCESS, "User removed from whitelist")
    else:
        return resp.sendResponse(resp.FORBIDDEN, "Failed to remove user from whitelist")
    pass