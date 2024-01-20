
from flask import Blueprint, request
import response as resp
import Services.Token.Token as Token
import Services.Server.Server as Server
import Services.Users.Users as Users

router = Blueprint('server', __name__, url_prefix='/server')

@router.route('/getAll', methods=['POST'])
def getFullServerInfo():
    # Check user token first
    token = request.headers.get('Authorization')
    data = Token.parseToken(token)
    if data == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    # Return server info
    return resp.sendResponse(resp.SUCCESS, data=Server.getFullServerInfo())

@router.route('/set', methods=['POST'])
def setServerInfo():
    token = request.headers.get('Authorization')
    userInfo = Token.parseToken(token)
    if userInfo == None:
        return resp.sendResponse(resp.FORBIDDEN, "Invalid token")
    # Check user permission
    if not Users.getUserInfo(userInfo["username"])["admin"]:
        return resp.sendResponse(resp.FORBIDDEN, "Permission denied. Only admin can do this.")
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    result = Server.setServerInfo(key, value)
    if result:
        return resp.sendResponse(resp.SUCCESS, "Server info updated")
    else:
        return resp.sendResponse(resp.BAD_REQUEST, "Invalid key")
    
